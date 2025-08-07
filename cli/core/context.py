#!/usr/bin/env python3
"""
File: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/core/context.py
Project: ContextKeeper v3
Purpose: CLI context management and state handling
Dependencies: api_client, config loader
Dependents: All CLI commands
Created: 2025-08-06
Modified: 2025-08-06

PLANNING CONTEXT:
- Centralised state management for CLI operations
- Holds API client instance, configuration, and session state
- Thread-safe for concurrent operations
- Supports both interactive and command-line modes

TODO FROM PLANNING:
- [x] CLIContext class with state management
- [x] Configuration loading from .env and defaults
- [x] Session management for current project
- [ ] Add persistent state saving to ~/.contextkeeper/cli_state.json
"""

import os
import json
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import logging

# === NAVIGATION ===
# Next: [./api_client.py] - Uses this context for API calls
# Parent: [../cli.py] - Main CLI entry point creates context

logger = logging.getLogger(__name__)


@dataclass
class ProjectState:
    """Current project state in CLI session"""
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    project_path: Optional[str] = None
    last_indexed: Optional[datetime] = None
    collection_name: Optional[str] = None
    
    def is_focused(self) -> bool:
        """Check if a project is currently focused"""
        return self.project_id is not None


@dataclass
class CLIConfig:
    """CLI configuration from environment and defaults"""
    api_url: str = "http://localhost:5556"
    api_timeout: int = 30
    max_retries: int = 3
    verify_ssl: bool = False
    debug_mode: bool = False
    output_format: str = "json"  # json, table, yaml
    colour_output: bool = True
    interactive_mode: bool = True
    log_level: str = "INFO"
    
    # Paths
    cache_dir: Path = field(default_factory=lambda: Path.home() / ".contextkeeper" / "cache")
    state_file: Path = field(default_factory=lambda: Path.home() / ".contextkeeper" / "cli_state.json")
    config_file: Path = field(default_factory=lambda: Path.home() / ".contextkeeper" / "config.json")
    
    @classmethod
    def from_env(cls) -> 'CLIConfig':
        """Load configuration from environment variables"""
        config = cls()
        
        # API settings
        config.api_url = os.getenv('RAG_AGENT_URL', config.api_url)
        config.api_timeout = int(os.getenv('CLI_TIMEOUT', config.api_timeout))
        config.max_retries = int(os.getenv('CLI_MAX_RETRIES', config.max_retries))
        
        # Output settings
        config.debug_mode = os.getenv('DEBUG', '0') == '1'
        config.output_format = os.getenv('CLI_OUTPUT_FORMAT', config.output_format)
        config.colour_output = os.getenv('CLI_COLOUR', '1') == '1'
        config.interactive_mode = os.getenv('CLI_INTERACTIVE', '1') == '1'
        
        # Logging
        config.log_level = os.getenv('LOG_LEVEL', config.log_level)
        
        return config
    
    def save(self) -> None:
        """Save configuration to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump({
                'api_url': self.api_url,
                'api_timeout': self.api_timeout,
                'max_retries': self.max_retries,
                'output_format': self.output_format,
                'colour_output': self.colour_output,
                'interactive_mode': self.interactive_mode,
                'log_level': self.log_level
            }, f, indent=2)
    
    @classmethod
    def load(cls) -> 'CLIConfig':
        """Load configuration from file, falling back to env"""
        config_file = Path.home() / ".contextkeeper" / "config.json"
        if config_file.exists():
            try:
                with open(config_file) as f:
                    data = json.load(f)
                    config = cls()
                    for key, value in data.items():
                        if hasattr(config, key):
                            setattr(config, key, value)
                    return config
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}")
        
        return cls.from_env()


class CLIContext:
    """
    Central context manager for CLI operations
    
    Manages:
    - API client instance
    - Current project state
    - Configuration
    - Session history
    - Thread safety
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern for global context"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialise CLI context"""
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self.config = CLIConfig.load()
            self.project = ProjectState()
            self.api_client = None  # Lazy loaded
            self.session_history: List[Dict[str, Any]] = []
            self._state_lock = threading.Lock()
            
            # Setup logging
            logging.basicConfig(
                level=getattr(logging, self.config.log_level),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Load persisted state
            self._load_state()
    
    def get_api_client(self):
        """Get or create API client instance"""
        if self.api_client is None:
            from .api_client import ContextKeeperAPI
            self.api_client = ContextKeeperAPI(
                base_url=self.config.api_url,
                timeout=self.config.api_timeout,
                max_retries=self.config.max_retries,
                verify_ssl=self.config.verify_ssl
            )
        return self.api_client
    
    def set_project(self, project_id: str, project_name: str = None, 
                   project_path: str = None) -> None:
        """Set the current focused project"""
        with self._state_lock:
            self.project.project_id = project_id
            self.project.project_name = project_name
            self.project.project_path = project_path
            self.project.collection_name = f"project_{project_id}"
            self._save_state()
            
            logger.info(f"Focused on project: {project_id} ({project_name})")
    
    def clear_project(self) -> None:
        """Clear current project focus"""
        with self._state_lock:
            self.project = ProjectState()
            self._save_state()
            logger.info("Cleared project focus")
    
    def add_to_history(self, command: str, result: Any) -> None:
        """Add command to session history"""
        with self._state_lock:
            self.session_history.append({
                'timestamp': datetime.now().isoformat(),
                'command': command,
                'project_id': self.project.project_id,
                'success': result is not None
            })
            
            # Keep only last 100 commands
            if len(self.session_history) > 100:
                self.session_history = self.session_history[-100:]
    
    def _load_state(self) -> None:
        """Load persisted CLI state"""
        if self.config.state_file.exists():
            try:
                with open(self.config.state_file) as f:
                    state = json.load(f)
                    
                    # Restore project state
                    if 'project' in state:
                        p = state['project']
                        self.project.project_id = p.get('project_id')
                        self.project.project_name = p.get('project_name')
                        self.project.project_path = p.get('project_path')
                        self.project.collection_name = p.get('collection_name')
                        if p.get('last_indexed'):
                            self.project.last_indexed = datetime.fromisoformat(p['last_indexed'])
                    
                    # Restore history
                    if 'history' in state:
                        self.session_history = state['history'][-50:]  # Keep recent
                        
                    logger.debug(f"Loaded CLI state from {self.config.state_file}")
            except Exception as e:
                logger.warning(f"Failed to load state: {e}")
    
    def _save_state(self) -> None:
        """Save CLI state to disk"""
        try:
            self.config.state_file.parent.mkdir(parents=True, exist_ok=True)
            
            state = {
                'project': {
                    'project_id': self.project.project_id,
                    'project_name': self.project.project_name,
                    'project_path': self.project.project_path,
                    'collection_name': self.project.collection_name,
                    'last_indexed': self.project.last_indexed.isoformat() if self.project.last_indexed else None
                },
                'history': self.session_history[-50:],  # Save recent history
                'saved_at': datetime.now().isoformat()
            }
            
            with open(self.config.state_file, 'w') as f:
                json.dump(state, f, indent=2)
                
            logger.debug(f"Saved CLI state to {self.config.state_file}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get current context summary for display"""
        return {
            'api_url': self.config.api_url,
            'current_project': {
                'id': self.project.project_id,
                'name': self.project.project_name,
                'path': self.project.project_path,
                'focused': self.project.is_focused()
            },
            'session': {
                'commands_run': len(self.session_history),
                'last_command': self.session_history[-1] if self.session_history else None
            },
            'config': {
                'output_format': self.config.output_format,
                'interactive': self.config.interactive_mode,
                'debug': self.config.debug_mode
            }
        }
    
    def reset(self) -> None:
        """Reset context to defaults"""
        with self._state_lock:
            self.project = ProjectState()
            self.session_history = []
            self.api_client = None
            self._save_state()
            logger.info("Context reset to defaults")


# Global context instance
def get_context() -> CLIContext:
    """Get the global CLI context instance"""
    return CLIContext()