#!/usr/bin/env python3
"""
Enhanced Multi-Project RAG Agent
Tracks development context across multiple projects with terminal monitoring
"""

import os
import json
import asyncio
import logging
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import psutil
import sqlite3

class ProjectStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused" 
    ARCHIVED = "archived"
    FOCUSED = "focused"  # Currently in focus

@dataclass
class ProjectSession:
    project_id: str
    name: str
    root_path: str
    status: ProjectStatus
    watch_dirs: List[str]
    focused_terminals: List[int] = None  # Terminal PIDs
    created_at: str = None
    last_active: str = None
    objectives: List[str] = None
    decisions: List[Dict] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.last_active is None:
            self.last_active = datetime.now().isoformat()
        if self.objectives is None:
            self.objectives = []
        if self.decisions is None:
            self.decisions = []
        if self.focused_terminals is None:
            self.focused_terminals = []

@dataclass 
class TerminalActivity:
    pid: int
    working_dir: str
    command: str
    timestamp: str
    project_id: Optional[str] = None
    is_focused: bool = False

class TerminalMonitor:
    """Monitors terminal activity and correlates with projects"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
        self.monitored_pids: Set[int] = set()
        
    def init_database(self):
        """Initialize SQLite database for terminal activity"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS terminal_activity (
                id INTEGER PRIMARY KEY,
                pid INTEGER,
                working_dir TEXT,
                command TEXT,
                timestamp TEXT,
                project_id TEXT,
                is_focused BOOLEAN DEFAULT FALSE
            )
        """)
        conn.commit()
        conn.close()
    
    def get_active_terminals(self) -> List[TerminalActivity]:
        """Get all currently active terminal sessions"""
        activities = []
        
        try:
            # Get all terminal processes (bash, zsh, etc.)
            for proc in psutil.process_iter(['pid', 'name', 'cwd']):
                try:
                    if proc.info['name'] in ['bash', 'zsh', 'fish', 'sh', 'Terminal']:
                        pid = proc.info['pid']
                        cwd = proc.info['cwd'] or "unknown"
                        
                        # Get recent command history if possible
                        command = self._get_recent_command(pid, cwd)
                        
                        activity = TerminalActivity(
                            pid=pid,
                            working_dir=cwd,
                            command=command,
                            timestamp=datetime.now().isoformat()
                        )
                        activities.append(activity)
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            logging.error(f"Error monitoring terminals: {e}")
            
        return activities
    
    def _get_recent_command(self, pid: int, cwd: str) -> str:
        """Try to get the most recent command from terminal history"""
        try:
            # Try to read from shell history files
            history_files = [
                os.path.expanduser("~/.zsh_history"),
                os.path.expanduser("~/.bash_history"),
                os.path.expanduser("~/.history")
            ]
            
            for hist_file in history_files:
                if os.path.exists(hist_file):
                    with open(hist_file, 'r', errors='ignore') as f:
                        lines = f.readlines()
                        if lines:
                            # Get last few commands and filter by working directory context
                            recent_commands = [line.strip() for line in lines[-10:]]
                            # In a real implementation, you'd want more sophisticated parsing
                            return recent_commands[-1] if recent_commands else "unknown"
            
            return "no_history_available"
            
        except Exception as e:
            logging.debug(f"Could not read command history: {e}")
            return "unknown"
    
    def log_activity(self, activity: TerminalActivity):
        """Log terminal activity to database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO terminal_activity 
            (pid, working_dir, command, timestamp, project_id, is_focused)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            activity.pid, activity.working_dir, activity.command,
            activity.timestamp, activity.project_id, activity.is_focused
        ))
        conn.commit()
        conn.close()
    
    def get_recent_activity(self, project_id: str = None, hours: int = 24) -> List[TerminalActivity]:
        """Get recent terminal activity, optionally filtered by project"""
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        if project_id:
            cursor = conn.execute("""
                SELECT pid, working_dir, command, timestamp, project_id, is_focused
                FROM terminal_activity 
                WHERE project_id = ? AND timestamp > ?
                ORDER BY timestamp DESC
            """, (project_id, since))
        else:
            cursor = conn.execute("""
                SELECT pid, working_dir, command, timestamp, project_id, is_focused
                FROM terminal_activity 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
            """, (since,))
        
        activities = []
        for row in cursor.fetchall():
            activities.append(TerminalActivity(
                pid=row[0], working_dir=row[1], command=row[2],
                timestamp=row[3], project_id=row[4], is_focused=bool(row[5])
            ))
        
        conn.close()
        return activities

class ProjectManager:
    """Manages multiple project sessions and their lifecycles"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.projects: Dict[str, ProjectSession] = {}
        self.active_project_id: Optional[str] = None
        self.load_projects()
    
    def load_projects(self):
        """Load project configurations from disk"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                for proj_data in data.get('projects', []):
                    session = ProjectSession(**proj_data)
                    self.projects[session.project_id] = session
                self.active_project_id = data.get('active_project_id')
    
    def save_projects(self):
        """Persist project configurations to disk"""
        data = {
            'projects': [asdict(project) for project in self.projects.values()],
            'active_project_id': self.active_project_id
        }
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_project(self, name: str, root_path: str, watch_dirs: List[str] = None) -> str:
        """Create a new project session"""
        project_id = f"proj_{int(time.time())}"
        
        if watch_dirs is None:
            watch_dirs = [root_path]
            
        session = ProjectSession(
            project_id=project_id,
            name=name,
            root_path=root_path,
            status=ProjectStatus.ACTIVE,
            watch_dirs=watch_dirs
        )
        
        self.projects[project_id] = session
        if self.active_project_id is None:
            self.active_project_id = project_id
            
        self.save_projects()
        return project_id
    
    def set_project_status(self, project_id: str, status: ProjectStatus):
        """Change project status (active/paused/archived/focused)"""
        if project_id in self.projects:
            self.projects[project_id].status = status
            self.projects[project_id].last_active = datetime.now().isoformat()
            
            # If setting to focused, unfocus others
            if status == ProjectStatus.FOCUSED:
                for pid, proj in self.projects.items():
                    if pid != project_id and proj.status == ProjectStatus.FOCUSED:
                        proj.status = ProjectStatus.ACTIVE
                        
            self.save_projects()
    
    def add_objective(self, project_id: str, objective: str):
        """Add an objective to a project"""
        if project_id in self.projects:
            self.projects[project_id].objectives.append({
                'text': objective,
                'timestamp': datetime.now().isoformat(),
                'completed': False
            })
            self.save_projects()
    
    def mark_objective_complete(self, project_id: str, objective_index: int):
        """Mark an objective as completed"""
        if project_id in self.projects:
            objectives = self.projects[project_id].objectives
            if 0 <= objective_index < len(objectives):
                objectives[objective_index]['completed'] = True
                objectives[objective_index]['completed_at'] = datetime.now().isoformat()
                self.save_projects()
    
    def add_decision(self, project_id: str, decision: str, context: str = "", importance: str = "normal"):
        """Record a project decision"""
        if project_id in self.projects:
            self.projects[project_id].decisions.append({
                'decision': decision,
                'context': context,
                'importance': importance,
                'timestamp': datetime.now().isoformat()
            })
            self.save_projects()
    
    def focus_terminals(self, project_id: str, terminal_pids: List[int]):
        """Set focused terminals for a project"""
        if project_id in self.projects:
            self.projects[project_id].focused_terminals = terminal_pids
            self.save_projects()
    
    def get_focused_projects(self) -> List[ProjectSession]:
        """Get all projects with focused status"""
        return [proj for proj in self.projects.values() 
                if proj.status == ProjectStatus.FOCUSED]
    
    def get_active_projects(self) -> List[ProjectSession]:
        """Get all active (non-paused, non-archived) projects"""
        return [proj for proj in self.projects.values() 
                if proj.status in [ProjectStatus.ACTIVE, ProjectStatus.FOCUSED]]

class EnhancedRAGAgent:
    """Enhanced RAG agent with multi-project and terminal monitoring"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.project_manager = ProjectManager(config.get('projects_config', './projects.json'))
        self.terminal_monitor = TerminalMonitor(config.get('terminal_db', './terminal_activity.db'))
        self.monitoring_active = False
        
        # Initialize existing RAG components (from your original code)
        # self.embedder = ...
        # self.db = ...
        # self.collection = ...
    
    async def start_monitoring(self):
        """Start monitoring terminal activity and correlating with projects"""
        self.monitoring_active = True
        
        while self.monitoring_active:
            try:
                # Get current terminal activities
                activities = self.terminal_monitor.get_active_terminals()
                
                # Correlate with projects
                for activity in activities:
                    project_id = self._correlate_activity_to_project(activity)
                    activity.project_id = project_id
                    
                    # Check if this terminal is focused for any project
                    activity.is_focused = self._is_terminal_focused(activity.pid)
                    
                    # Log the activity
                    self.terminal_monitor.log_activity(activity)
                
                # Update project last_active timestamps
                self._update_project_activity()
                
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
            except Exception as e:
                logging.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    def _correlate_activity_to_project(self, activity: TerminalActivity) -> Optional[str]:
        """Determine which project this terminal activity belongs to"""
        working_dir = activity.working_dir
        
        # Check if working directory is within any project's watch directories
        for project_id, project in self.project_manager.projects.items():
            if project.status == ProjectStatus.ARCHIVED:
                continue
                
            # Check if current working directory is within project paths
            for watch_dir in project.watch_dirs:
                if working_dir.startswith(watch_dir):
                    return project_id
            
            # Also check project root
            if working_dir.startswith(project.root_path):
                return project_id
        
        return None
    
    def _is_terminal_focused(self, pid: int) -> bool:
        """Check if this terminal PID is focused for any project"""
        for project in self.project_manager.projects.values():
            if pid in project.focused_terminals:
                return True
        return False
    
    def _update_project_activity(self):
        """Update last_active timestamps for projects with recent activity"""
        recent_activities = self.terminal_monitor.get_recent_activity(hours=1)
        active_projects = set()
        
        for activity in recent_activities:
            if activity.project_id:
                active_projects.add(activity.project_id)
        
        # Update timestamps
        current_time = datetime.now().isoformat()
        for project_id in active_projects:
            if project_id in self.project_manager.projects:
                self.project_manager.projects[project_id].last_active = current_time
        
        self.project_manager.save_projects()
    
    async def get_project_context(self, project_id: str = None) -> Dict[str, Any]:
        """Get comprehensive project context for AI agents"""
        if project_id is None:
            # Get focused projects or active project
            focused = self.project_manager.get_focused_projects()
            if focused:
                project_id = focused[0].project_id
            elif self.project_manager.active_project_id:
                project_id = self.project_manager.active_project_id
            else:
                return {"error": "No active project"}
        
        project = self.project_manager.projects.get(project_id)
        if not project:
            return {"error": f"Project {project_id} not found"}
        
        # Get recent terminal activity
        recent_activity = self.terminal_monitor.get_recent_activity(project_id, hours=8)
        
        # Get focused terminal activity if any
        focused_activity = [a for a in recent_activity if a.is_focused]
        
        # Check for objective drift (this would need more sophisticated logic)
        drift_analysis = self._analyze_objective_drift(project, recent_activity)
        
        return {
            'project': asdict(project),
            'recent_commands': [
                {
                    'command': a.command,
                    'working_dir': a.working_dir,
                    'timestamp': a.timestamp,
                    'is_focused': a.is_focused
                } for a in recent_activity[-10:]  # Last 10 commands
            ],
            'focused_terminal_activity': [
                {
                    'command': a.command,
                    'working_dir': a.working_dir, 
                    'timestamp': a.timestamp
                } for a in focused_activity[-5:]  # Last 5 focused commands
            ],
            'objectives_status': {
                'total': len(project.objectives),
                'completed': len([o for o in project.objectives if o.get('completed', False)]),
                'current': [o for o in project.objectives if not o.get('completed', False)]
            },
            'recent_decisions': project.decisions[-5:],  # Last 5 decisions
            'drift_analysis': drift_analysis
        }
    
    def _analyze_objective_drift(self, project: ProjectSession, activities: List[TerminalActivity]) -> Dict[str, Any]:
        """Analyze if recent activity aligns with project objectives"""
        # This is a simplified version - you'd want more sophisticated NLP analysis
        current_objectives = [o['text'] for o in project.objectives if not o.get('completed', False)]
        
        if not current_objectives:
            return {"status": "no_active_objectives"}
        
        # Simple keyword matching for drift detection
        objective_keywords = set()
        for obj in current_objectives:
            objective_keywords.update(obj.lower().split())
        
        recent_commands = [a.command.lower() for a in activities[-20:]]  # Last 20 commands
        command_keywords = set()
        for cmd in recent_commands:
            command_keywords.update(cmd.split())
        
        # Calculate overlap
        overlap = len(objective_keywords.intersection(command_keywords))
        total_obj_keywords = len(objective_keywords)
        
        alignment_score = overlap / total_obj_keywords if total_obj_keywords > 0 else 0
        
        return {
            "alignment_score": alignment_score,
            "status": "aligned" if alignment_score > 0.3 else "potential_drift",
            "current_objectives": current_objectives,
            "recent_focus": list(command_keywords)[-10:]  # Recent focus areas
        }

# CLI Extensions for the enhanced agent
class EnhancedRAGCLI:
    """Enhanced CLI with project management commands"""
    
    def __init__(self, agent: EnhancedRAGAgent):
        self.agent = agent
    
    async def handle_command(self, command: str, args: List[str]):
        """Handle enhanced CLI commands"""
        
        if command == "projects":
            await self._handle_projects_command(args)
        elif command == "focus":
            await self._handle_focus_command(args)
        elif command == "objectives":
            await self._handle_objectives_command(args)
        elif command == "terminals":
            await self._handle_terminals_command(args)
        elif command == "context":
            await self._handle_context_command(args)
        elif command == "drift":
            await self._handle_drift_command(args)
    
    async def _handle_projects_command(self, args: List[str]):
        """Handle project management commands"""
        if not args or args[0] == "list":
            projects = self.agent.project_manager.projects
            print("\n📁 Projects:")
            for pid, proj in projects.items():
                status_icon = {
                    ProjectStatus.ACTIVE: "🟢",
                    ProjectStatus.PAUSED: "⏸️",
                    ProjectStatus.ARCHIVED: "📦",
                    ProjectStatus.FOCUSED: "🎯"
                }[proj.status]
                print(f"  {status_icon} {proj.name} ({pid})")
                print(f"     Path: {proj.root_path}")
                print(f"     Status: {proj.status.value}")
                print(f"     Objectives: {len([o for o in proj.objectives if not o.get('completed', False)])}")
        
        elif args[0] == "create":
            name = args[1] if len(args) > 1 else input("Project name: ")
            root_path = args[2] if len(args) > 2 else input("Root path: ")
            project_id = self.agent.project_manager.create_project(name, root_path)
            print(f"✅ Created project: {name} ({project_id})")
        
        elif args[0] == "pause":
            project_id = args[1] if len(args) > 1 else input("Project ID: ")
            self.agent.project_manager.set_project_status(project_id, ProjectStatus.PAUSED)
            print(f"⏸️ Paused project: {project_id}")
        
        elif args[0] == "resume":
            project_id = args[1] if len(args) > 1 else input("Project ID: ")
            self.agent.project_manager.set_project_status(project_id, ProjectStatus.ACTIVE)
            print(f"▶️ Resumed project: {project_id}")
        
        elif args[0] == "archive":
            project_id = args[1] if len(args) > 1 else input("Project ID: ")
            self.agent.project_manager.set_project_status(project_id, ProjectStatus.ARCHIVED)
            print(f"📦 Archived project: {project_id}")
    
    async def _handle_focus_command(self, args: List[str]):
        """Handle focus management"""
        if not args:
            focused = self.agent.project_manager.get_focused_projects()
            if focused:
                print(f"🎯 Currently focused: {focused[0].name}")
            else:
                print("No projects currently focused")
        else:
            project_id = args[0]
            self.agent.project_manager.set_project_status(project_id, ProjectStatus.FOCUSED)
            print(f"🎯 Focused on project: {project_id}")
    
    async def _handle_context_command(self, args: List[str]):
        """Get project context for AI agents"""
        project_id = args[0] if args else None
        context = await self.agent.get_project_context(project_id)
        
        if "error" in context:
            print(f"❌ {context['error']}")
            return
        
        print(f"\n🎯 Project: {context['project']['name']}")
        print(f"📍 Status: {context['project']['status']}")
        print(f"🎯 Objectives: {context['objectives_status']['completed']}/{context['objectives_status']['total']} completed")
        
        if context['recent_commands']:
            print(f"\n💻 Recent Commands:")
            for cmd in context['recent_commands'][-5:]:
                focus_indicator = "🎯" if cmd['is_focused'] else "  "
                print(f"  {focus_indicator} {cmd['command'][:60]}...")
        
        drift = context['drift_analysis']
        if drift['status'] == 'potential_drift':
            print(f"\n⚠️ Potential objective drift detected (alignment: {drift['alignment_score']:.2f})")

# Example usage and integration points
if __name__ == "__main__":
    # This would be integrated with your existing rag_agent.py
    pass