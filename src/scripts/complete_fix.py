#!/usr/bin/env python3
"""
Complete fix for missing add_decision and add_objective methods
"""

def main():
    import re
    
    # Read the file content
    with open('/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/rag_agent.py', 'r') as f:
        content = f.read()
    
    # Create the replacement
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
    
    # Replace the malformed method with the proper methods
    if malformed_method in content:
        new_content = content.replace(malformed_method, proper_methods)
        
        # Write the fixed file
        with open('/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/rag_agent.py', 'w') as f:
            f.write(new_content)
        
        print("✅ Successfully fixed rag_agent.py!")
        print("✅ Replaced malformed interactive_mode method with proper add_decision and add_objective methods")
        
        # Verify the fix
        if "def add_decision(self, decision: str" in new_content:
            print("✅ add_decision method successfully added")
        if "def add_objective(self, title: str" in new_content:
            print("✅ add_objective method successfully added")
        if "async def interactive_mode(self):" in new_content and "if decision_obj and project_id" in new_content:
            # Check if it's the remaining one in RAGCLI class
            parts = new_content.split("async def interactive_mode(self):")
            if len(parts) == 2 and '"Interactive query mode"' in parts[1]:
                print("✅ Malformed method removed, valid interactive_mode method remains in RAGCLI class")
            else:
                print("⚠️  Check interactive_mode methods manually")
        
        return True
    else:
        print("❌ Malformed method not found for replacement")
        print("Searching for similar patterns...")
        
        # Try a more flexible search
        pattern = r'async def interactive_mode\(self\):\s+if decision_obj.*?return decision_obj'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            print(f"✅ Found similar pattern: {match.group(0)[:100]}...")
            new_content = content.replace(match.group(0), proper_methods)
            
            with open('/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/rag_agent.py', 'w') as f:
                f.write(new_content)
            
            print("✅ Applied fix using regex matching")
            return True
        else:
            print("❌ Could not find the malformed method to fix")
            return False

if __name__ == "__main__":
    main()