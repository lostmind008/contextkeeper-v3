#!/usr/bin/env python3
"""
Apply the isolation fix to rag_agent.py
This script patches the vulnerable query methods with secure versions
"""

import re
import shutil
from datetime import datetime

def apply_isolation_fix():
    # Read the original file
    with open('rag_agent.py', 'r') as f:
        content = f.read()
    
    # Create a backup with timestamp
    backup_name = f'rag_agent.py.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    shutil.copy('rag_agent.py', backup_name)
    print(f"✅ Created backup: {backup_name}")
    
    # Read the fixed query method
    fixed_query_method = '''    async def query(self, question: str, k: int = None, project_id: str = None) -> Dict[str, Any]:
        """Query the knowledge base with STRICT project filtering"""
        if k is None:
            k = self.config['max_results']
        
        # CRITICAL: Require project_id - fail closed, not open
        if project_id is None:
            focused_project = self.project_manager.get_focused_project()
            if focused_project:
                project_id = focused_project.project_id
            else:
                # FAIL CLOSED: No project = no results
                logger.warning(f"Query attempted without project_id: {question[:50]}...")
                return {
                    'query': question,
                    'error': 'No project context specified',
                    'results': [],
                    'timestamp': datetime.now().isoformat()
                }
        
        # Validate project exists and is accessible
        if project_id not in self.collections:
            logger.error(f"Query attempted for non-existent project: {project_id}")
            return {
                'query': question,
                'error': f'Project {project_id} not found',
                'results': [],
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Search ONLY the specified project - no cross-project contamination
            results = self.collections[project_id].query(
                query_texts=[question],
                n_results=k
            )
            
            # Format results with project context
            formatted_results = []
            if results and 'ids' in results and results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None,
                        'project_id': project_id  # Always include source project
                    })
            
            return {
                'query': question,
                'results': formatted_results,
                'project_id': project_id,  # Always include project context
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Query error in project {project_id}: {e}")
            return {
                'query': question,
                'error': str(e),
                'results': [],
                'project_id': project_id
            }'''
    
    # Find and replace the query method
    query_pattern = r'(    async def query\(self, question: str.*?(?=\n    async def|$))'
    match = re.search(query_pattern, content, re.DOTALL)
    
    if match:
        old_method = match.group(1)
        content = content.replace(old_method, fixed_query_method)
        print("✅ Replaced query method")
    else:
        print("❌ Could not find query method to replace")
        return False
    
    # Read and apply the fixed query_with_llm method
    fixed_query_with_llm = '''    async def query_with_llm(self, question: str, k: int = None, project_id: str = None) -> Dict[str, Any]:
        """Enhanced query with natural language response generation"""
        # CRITICAL: Enforce project_id requirement
        if project_id is None:
            focused_project = self.project_manager.get_focused_project()
            if focused_project:
                project_id = focused_project.project_id
            else:
                return {
                    'question': question,
                    'answer': "No project context specified. Please select a project first.",
                    'sources': [],
                    'error': 'No project context'
                }
        
        # Get raw RAG results using the fixed query method
        raw_results = await self.query(question, k, project_id)

        if raw_results.get('error'):
            return {
                'question': question,
                'answer': f"Error: {raw_results['error']}",
                'sources': [],
                'project_id': project_id
            }

        if not raw_results['results']:
            return {
                'question': question,
                'answer': f"I couldn't find relevant information in project {project_id}.",
                'sources': [],
                'project_id': project_id
            }

        # Prepare context for LLM
        context_chunks = []
        sources = []

        for result in raw_results['results'][:5]:  # Use top 5 results
            context_chunks.append(result['content'])
            sources.append(result['metadata'].get('file', 'Unknown'))

        context = "\\n\\n---\\n\\n".join(context_chunks)

        # Generate response using LLM
        try:
            response = self.client.generate_content(
                f\'\'\'Based on the following context from the project "{project_id}", answer this question: {question}

Context from the codebase:
{context}

Provide a helpful and accurate answer based solely on the given context. If the context doesn't contain enough information, say so.\'\'\'
            )

            return {
                'question': question,
                'answer': response.text,
                'sources': list(set(sources)),  # Unique sources
                'project_id': project_id,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return {
                'question': question,
                'answer': f"Error generating response: {str(e)}",
                'sources': sources,
                'project_id': project_id,
                'error': str(e)
            }'''
    
    # Find and replace query_with_llm method
    query_llm_pattern = r'(    async def query_with_llm\(self, question: str.*?(?=\n    async def|$))'
    match_llm = re.search(query_llm_pattern, content, re.DOTALL)
    
    if match_llm:
        old_llm_method = match_llm.group(1)
        content = content.replace(old_llm_method, fixed_query_with_llm)
        print("✅ Replaced query_with_llm method")
    else:
        print("❌ Could not find query_with_llm method to replace")
    
    # Write the fixed content back
    with open('rag_agent.py', 'w') as f:
        f.write(content)
    
    print("✅ Successfully applied isolation fixes to rag_agent.py")
    return True

if __name__ == "__main__":
    apply_isolation_fix()