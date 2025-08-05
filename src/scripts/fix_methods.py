#!/usr/bin/env python3
"""
Fix missing add_decision and add_objective methods in rag_agent.py
"""

import re

def fix_rag_agent():
    """Fix the malformed interactive_mode method and add proper methods"""
    
    # Read the current file
    with open('rag_agent.py', 'r') as f:
        content = f.read()
    
    # The malformed method to replace
    malformed_method = '''    async def interactive_mode(self):
        
        if decision_obj and project_id in self.collections:
            # Create content for embedding
            content = f"PROJECT DECISION: {decision}"
            if reasoning:
                content += f"\\nREASONING: {reasoning}"
            if tags:
                content += f"\\nTAGS: {', '.join(tags)}"
            content += f"\\nDATE: {decision_obj.timestamp}"
            
            # Store decision (ChromaDB will handle embeddings)
            self.collections[project_id].add(
                ids=[decision_obj.id],
                documents=[content],
                metadatas=[{
                    'type': 'decision',
                    'project_id': project_id,
                    'tags': tags or [],
                    'date': decision_obj.timestamp
                }]
            )
            
            logger.info(f"Added decision to project {project_id}: {decision[:50]}...")
        
        return decision_obj'''
    
    # The proper methods to add
    proper_methods = '''    def add_decision(self, decision: str, reasoning: str = "", project_id: str = None, tags: List[str] = None) -> Optional[Any]:
        """Add a decision to a project with embedding/search functionality"""
        try:
            # Use focused project if no project_id provided
            if project_id is None:
                project_id = self.project_manager.focused_project_id
                if not project_id:
                    logger.error("No project specified and no focused project available")
                    return None
            
            # Validate project exists
            if project_id not in self.project_manager.projects:
                logger.error(f"Project {project_id} not found")
                return None
            
            # Use project manager to create and persist the decision
            decision_obj = self.project_manager.add_decision(
                project_id=project_id,
                decision=decision,
                reasoning=reasoning,
                tags=tags or []
            )
            
            if decision_obj and project_id in self.collections:
                # Create content for embedding
                content = f"PROJECT DECISION: {decision}"
                if reasoning:
                    content += f"\\nREASONING: {reasoning}"
                if tags:
                    content += f"\\nTAGS: {', '.join(tags)}"
                content += f"\\nDATE: {decision_obj.timestamp}"
                
                # Store decision in ChromaDB for embedding/search functionality
                self.collections[project_id].add(
                    ids=[decision_obj.id],
                    documents=[content],
                    metadatas=[{
                        'type': 'decision',
                        'project_id': project_id,
                        'tags': tags or [],
                        'date': decision_obj.timestamp
                    }]
                )
                
                logger.info(f"Added decision to project {project_id}: {decision[:50]}...")
            
            return decision_obj
            
        except Exception as e:
            logger.error(f"Error adding decision: {e}")
            return None
    
    def add_objective(self, title: str, description: str = "", priority: str = "medium", project_id: str = None) -> Optional[Any]:
        """Add an objective to a project with embedding/search functionality"""
        try:
            # Use focused project if no project_id provided
            if project_id is None:
                project_id = self.project_manager.focused_project_id
                if not project_id:
                    logger.error("No project specified and no focused project available")
                    return None
            
            # Validate project exists
            if project_id not in self.project_manager.projects:
                logger.error(f"Project {project_id} not found")
                return None
            
            # Use project manager to create and persist the objective
            objective_obj = self.project_manager.add_objective(
                project_id=project_id,
                title=title,
                description=description,
                priority=priority
            )
            
            if objective_obj and project_id in self.collections:
                # Create content for embedding
                content = f"PROJECT OBJECTIVE: {title}"
                if description:
                    content += f"\\nDESCRIPTION: {description}"
                content += f"\\nPRIORITY: {priority}"
                content += f"\\nDATE: {objective_obj.created_at}"
                
                # Store objective in ChromaDB for embedding/search functionality
                self.collections[project_id].add(
                    ids=[objective_obj.id],
                    documents=[content],
                    metadatas=[{
                        'type': 'objective',
                        'project_id': project_id,
                        'priority': priority,
                        'date': objective_obj.created_at
                    }]
                )
                
                logger.info(f"Added objective to project {project_id}: {title}")
            
            return objective_obj
            
        except Exception as e:
            logger.error(f"Error adding objective: {e}")
            return None'''
    
    # Replace the malformed method with proper methods
    if malformed_method in content:
        content = content.replace(malformed_method, proper_methods)
        print("✅ Fixed malformed interactive_mode method")
    else:
        print("❌ Malformed method not found - checking for alternatives...")
        # Try to find it with regex for more flexible matching
        pattern = r'    async def interactive_mode\(self\):\s*\n\s*\n\s*if decision_obj and project_id.*?return decision_obj'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content.replace(match.group(0), proper_methods)
            print("✅ Fixed malformed method with regex matching")
        else:
            print("❌ Could not find malformed method to replace")
            return False
    
    # Write the fixed content
    with open('rag_agent.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed rag_agent.py with proper add_decision and add_objective methods")
    return True

if __name__ == "__main__":
    success = fix_rag_agent()
    if success:
        print("✅ All fixes applied successfully!")
    else:
        print("❌ Fix failed!")