"""
YouTube Analyzer Project - RAG Agent Integration Examples
Shows how to use the RAG agent during development
"""

import requests
import json
from datetime import datetime

class YouTubeAnalyzerRAG:
    """Helper class for YouTube Analyzer specific RAG queries"""
    
    def __init__(self, rag_url="http://localhost:5555"):
        self.rag_url = rag_url
    
    def query(self, question, k=5):
        """Query the RAG agent"""
        response = requests.post(
            f"{self.rag_url}/query",
            json={"question": question, "k": k}
        )
        return response.json()
    
    def add_decision(self, decision, context, importance="normal"):
        """Add a project decision"""
        response = requests.post(
            f"{self.rag_url}/decision",
            json={
                "decision": decision,
                "context": context,
                "importance": importance
            }
        )
        return response.json()
    
    def get_gemini_config(self):
        """Get latest Gemini configuration"""
        result = self.query(
            "Show the latest Gemini 2.5 configuration and initialization code using unified GenAI SDK"
        )
        return self._extract_code(result)
    
    def get_agent_code(self, agent_name):
        """Get code for a specific agent"""
        result = self.query(
            f"Show the {agent_name} agent implementation with CrewAI"
        )
        return self._extract_code(result)
    
    def get_api_keys_setup(self):
        """Get environment variables and API key setup"""
        result = self.query(
            "What environment variables and API keys are needed for the YouTube analyzer?"
        )
        return result
    
    def check_common_errors(self, error_message):
        """Check if an error has been encountered before"""
        result = self.query(
            f"Has this error been encountered before: {error_message}"
        )
        return result
    
    def _extract_code(self, result):
        """Extract code snippets from results"""
        code_snippets = []
        if 'results' in result:
            for r in result['results']:
                content = r['content']
                # Simple code detection
                if any(keyword in content for keyword in ['def ', 'class ', 'import ', 'from ']):
                    code_snippets.append({
                        'file': r['metadata'].get('file', 'Unknown'),
                        'code': content
                    })
        return code_snippets

# Example usage during development
if __name__ == "__main__":
    rag = YouTubeAnalyzerRAG()
    
    print("🔍 YouTube Analyzer RAG Integration Examples\n")
    
    # 1. When starting work for the day
    print("1. Morning Context Refresh:")
    print("-" * 50)
    
    morning_query = rag.query("What was I working on yesterday in the YouTube analyzer project?")
    if morning_query['results']:
        print(f"Recent work: {morning_query['results'][0]['content'][:200]}...")
    
    # 2. When you need to remember API setup
    print("\n2. API Configuration Check:")
    print("-" * 50)
    
    gemini_config = rag.get_gemini_config()
    if gemini_config:
        print(f"Found Gemini config in: {gemini_config[0]['file']}")
        print(f"Code snippet: {gemini_config[0]['code'][:200]}...")
    
    # 3. When you encounter an error
    print("\n3. Error Resolution Check:")
    print("-" * 50)
    
    error = "AttributeError: 'google.generativeai' has no attribute 'Client'"
    error_solution = rag.check_common_errors(error)
    if error_solution['results']:
        print(f"Found solution: {error_solution['results'][0]['content'][:200]}...")
    
    # 4. When making architecture decisions
    print("\n4. Recording Architecture Decision:")
    print("-" * 50)
    
    decision = rag.add_decision(
        decision="Using CrewAI for multi-agent orchestration instead of LangGraph",
        context="CrewAI has simpler API and better examples for our use case. Role-based agents fit YouTube analyzer workflow perfectly.",
        importance="high"
    )
    print("✅ Decision recorded for future reference")
    
    # 5. When you need to check what agents exist
    print("\n5. Existing Agents Query:")
    print("-" * 50)
    
    agents = rag.query("List all agents created for YouTube analyzer with their roles")
    if agents['results']:
        print("Found agents:")
        for r in agents['results'][:3]:
            if 'Agent' in r['content']:
                print(f"- {r['content'][:100]}...")

# Integration with Claude prompts
CLAUDE_PROMPT_TEMPLATE = """
You are helping with the YouTube Analyzer project. Before starting, I've queried our RAG knowledge base:

CONTEXT FROM RAG:
{rag_context}

CURRENT TASK: {task}

Rules:
1. Use the latest unified GenAI SDK (google-genai) as shown in context
2. Follow the existing agent patterns from our codebase
3. Reference any previous solutions to similar problems
4. Maintain consistency with project decisions

Now, please help with the task above.
"""

def create_claude_prompt(task, rag_helper):
    """Create a context-aware prompt for Claude"""
    # Gather relevant context
    contexts = []
    
    # Get recent decisions
    decisions = rag_helper.query("What are the recent architecture decisions?")
    if decisions['results']:
        contexts.append(f"Recent decisions: {decisions['results'][0]['content']}")
    
    # Get relevant code patterns
    patterns = rag_helper.query(f"Show code patterns related to: {task}")
    if patterns['results']:
        contexts.append(f"Relevant patterns: {patterns['results'][0]['content']}")
    
    # Combine context
    rag_context = "\n\n".join(contexts)
    
    return CLAUDE_PROMPT_TEMPLATE.format(
        rag_context=rag_context,
        task=task
    )

# Example: Creating a context-aware prompt
task = "Create the video splitter agent using FFmpeg"
prompt = create_claude_prompt(task, YouTubeAnalyzerRAG())
print(f"\n6. Context-Aware Claude Prompt:\n{'-' * 50}\n{prompt[:500]}...")
