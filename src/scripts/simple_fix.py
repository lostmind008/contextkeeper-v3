import subprocess
import sys

# Simple replacement using sed-like functionality
def apply_fix():
    """Apply targeted fix using string replacement"""
    
    print("Reading the file...")
    with open('/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/rag_agent.py', 'r') as f:
        content = f.read()
    
    print("Applying fix...")
    # We know the exact malformed content from our investigation
    bad_content = '''    async def interactive_mode(self):
        
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
    
    good_content = '''    def add_decision(self, decision: str, reasoning: str = "", project_id: str = None, tags: List[str] = None) -> Optional[Any]:
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
    
    if bad_content in content:
        print("✅ Found malformed method, replacing...")
        new_content = content.replace(bad_content, good_content)
        
        with open('/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/rag_agent.py', 'w') as f:
            f.write(new_content)
        
        print("✅ Fix applied successfully!")
        return True
    else:
        print("❌ Malformed method not found")
        return False

if __name__ == "__main__":
    apply_fix()