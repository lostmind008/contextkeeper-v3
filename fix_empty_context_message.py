#!/usr/bin/env python3
"""
Fix the poor quality error message when project knowledge base is empty.
This addresses the user's issue where they get unhelpful responses like:
"The provided context states that it is from the project 'proj_736df3fd80a4'"
"""

import re
import sys

def apply_fix():
    """Apply the fix to improve empty context error message"""
    
    print("🔧 Applying fix for empty context error message...")
    
    file_path = '/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/rag_agent.py'
    
    try:
        # Read the file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find the problematic section
        old_pattern = r'''        if not raw_results\['results'\]:
            return \{
                'question': question,
                'answer': f"I couldn't find relevant information in project \{project_id\}\.",
                'sources': \[\],
                'project_id': project_id
            \}'''
        
        new_code = '''        if not raw_results['results']:
            return {
                'question': question,
                'answer': f"""I couldn't find any indexed content for project {project_id}.

This usually means:
• The project hasn't been indexed yet, or
• The project has no compatible files, or  
• The indexing process failed

To fix this, please index your project with content:
./scripts/rag_cli_v2.sh projects ingest {project_id} /path/to/your/project

After indexing, try your question again.""",
                'sources': [],
                'project_id': project_id,
                'suggestion': 'index_project'
            }'''
        
        # Apply the fix
        new_content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)
        
        if new_content == content:
            print("❌ Pattern not found - checking alternative patterns...")
            
            # Try simpler pattern
            old_simple = 'f"I couldn\'t find relevant information in project {project_id}."'
            new_simple = '''f"""I couldn't find any indexed content for project {project_id}.

This usually means:
• The project hasn't been indexed yet, or
• The project has no compatible files, or  
• The indexing process failed

To fix this, please index your project with content:
./scripts/rag_cli_v2.sh projects ingest {project_id} /path/to/your/project

After indexing, try your question again."""'''
            
            new_content = content.replace(old_simple, new_simple)
            
            if new_content == content:
                print("❌ Could not find the target pattern to replace")
                print("💡 Manual fix required")
                return False
        
        # Write the updated content
        with open(file_path, 'w') as f:
            f.write(new_content)
            
        print("✅ Successfully applied fix to rag_agent.py")
        print("📝 Improved error message for empty knowledge bases")
        print()
        print("🧪 To test the fix:")
        print("1. Restart the service: python rag_agent.py start")
        print("2. Test with empty project: python run_diagnostics.py")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error applying fix: {e}")
        return False

def verify_fix():
    """Verify the fix was applied correctly"""
    print("🔍 Verifying fix was applied...")
    
    file_path = '/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/rag_agent.py'
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if the new message is present
        if "This usually means:" in content and "index your project with content:" in content:
            print("✅ Fix verified successfully")
            return True
        else:
            print("❌ Fix verification failed")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying fix: {e}")
        return False

def main():
    print("🚨 FIX: Empty Context Error Message Improvement")
    print("=" * 50)
    print("Addressing user issue: Poor quality responses from query_llm")
    print("Target: Better error messages when knowledge base is empty")
    print()
    
    # Apply the fix
    if apply_fix():
        print("=" * 50)
        if verify_fix():
            print("🎉 Fix completed successfully!")
            print()
            print("WHAT WAS CHANGED:")
            print("• Improved error message when project has no indexed content")
            print("• Added clear instructions for users on how to fix the issue")
            print("• Added suggestion field for future UI enhancements")
            print()
            print("NEXT STEPS:")
            print("1. Restart ContextKeeper service")
            print("2. Run diagnostics to test the fix")
            print("3. Guide user to index their project properly")
        else:
            print("⚠️ Fix applied but verification failed")
    else:
        print("❌ Fix application failed")
        print("Manual intervention required")

if __name__ == "__main__":
    main()