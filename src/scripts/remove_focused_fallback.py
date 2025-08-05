#!/usr/bin/env python3
"""
Remove focused project fallback to truly enforce "fail closed" behavior
"""

import re

def remove_focused_fallback():
    """Update query methods to remove focused project fallback"""
    
    # Read the current rag_agent.py
    with open('rag_agent.py', 'r') as f:
        content = f.read()
    
    # Fix 1: Update query method to truly fail closed
    query_fix = '''async def query(self, question: str, k: int = None, project_id: str = None) -> Dict[str, Any]:
        """Query the knowledge base with strict project isolation"""
        if k is None:
            k = self.config['default_k']
        
        # CRITICAL: Require project_id - fail closed, not open
        if project_id is None:
            # FAIL CLOSED: No project = no results
            logger.warning(f"Query attempted without project_id: {question[:50]}...")
            return {
                'query': question,
                'error': 'No project context specified. Please provide project_id.',
                'results': [],
                'timestamp': datetime.now().isoformat()
            }'''
    
    # Replace the query method implementation
    query_pattern = r'async def query\(self, question: str, k: int = None, project_id: str = None\) -> Dict\[str, Any\]:\s*\n.*?""".*?""".*?if k is None:.*?# CRITICAL: Require project_id - fail closed, not open.*?if project_id is None:.*?focused_project = self\.project_manager\.get_focused_project\(\).*?if focused_project:.*?project_id = focused_project\.project_id.*?else:.*?# FAIL CLOSED: No project = no results'
    
    content = re.sub(
        query_pattern,
        query_fix,
        content,
        flags=re.DOTALL
    )
    
    # Fix 2: Update query_with_llm method to truly fail closed
    query_llm_fix = '''async def query_with_llm(self, question: str, k: int = None, project_id: str = None) -> Dict[str, Any]:
        """Enhanced query with natural language response generation"""
        # CRITICAL: Enforce project_id requirement
        if project_id is None:
            return {
                'question': question,
                'error': 'No project context specified. Please provide project_id.',
                'answer': 'Cannot process query without project context.',
                'sources': [],
                'timestamp': datetime.now().isoformat()
            }'''
    
    # Replace the query_with_llm method implementation
    query_llm_pattern = r'async def query_with_llm\(self, question: str, k: int = None, project_id: str = None\) -> Dict\[str, Any\]:\s*\n.*?""".*?""".*?# CRITICAL: Enforce project_id requirement.*?if project_id is None:.*?focused_project = self\.project_manager\.get_focused_project\(\).*?if focused_project:.*?project_id = focused_project\.project_id.*?else:'
    
    content = re.sub(
        query_llm_pattern,
        query_llm_fix,
        content,
        flags=re.DOTALL
    )
    
    # Write the updated content
    with open('rag_agent.py', 'w') as f:
        f.write(content)
    
    print("✅ Removed focused project fallback from query methods")
    print("📝 Query methods now truly fail closed when no project_id is provided")
    
    return True

if __name__ == "__main__":
    remove_focused_fallback()