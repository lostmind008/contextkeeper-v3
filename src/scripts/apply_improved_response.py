#!/usr/bin/env python3
"""
Apply Improved Empty Project Response
====================================

This script updates the rag_agent.py file to provide better responses
when a project has no meaningful content indexed.
"""

import re

def update_empty_project_response():
    """Update the empty project response in rag_agent.py"""
    
    # Read the current file
    with open('rag_agent.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the old response pattern
    old_pattern = r'''if not raw_results\['results'\]:
            return \{
                'question': question,
                'answer': f"""I couldn't find any indexed content for project \{project_id\}\.

This usually means:
• The project hasn't been indexed yet, or
• The project has no compatible files, or  
• The indexing process failed

To fix this, please index your project with content:
\./scripts/rag_cli_v2\.sh projects ingest \{project_id\} /path/to/your/project

After indexing, try your question again\.""",
                'sources': \[\],
                'project_id': project_id,
                'suggestion': 'index_project'
            \}'''
    
    # Define the new response
    new_response = '''if not raw_results['results']:
            return {
                'question': question,
                'answer': f"""I couldn't find any meaningful indexed content for project {project_id}.

This usually means:
• The project contains only binary/image data (like base64 encoded files), or
• The project has no text-based files (code, docs, configs), or
• The indexing process filtered out all content as non-meaningful

**Immediate Solutions:**

1. **Add meaningful content** to your project directory:
   - README.md with project description
   - Source code files (.py, .js, .md, etc.)
   - Configuration files (package.json, config files)
   - Documentation files

2. **Run the fix tool** I've prepared for you:
   ```bash
   python comprehensive_project_fix.py
   ```
   This will create sample meaningful content and test the results.

3. **Create a new project** with existing code:
   ```bash
   ./scripts/rag_cli_v2.sh projects create "My Project" /path/to/your/code
   ```

4. **Check project content**: Your project may contain only images/binary data which provides no searchable context.

The chat interface needs text-based content to provide meaningful responses about your project.""",
                'sources': [],
                'project_id': project_id,
                'suggestion': 'add_meaningful_content',
                'fix_available': True
            }'''
    
    # Find and replace the section
    # Look for the simpler pattern first
    old_simple = '''f"""I couldn't find any indexed content for project {project_id}.

This usually means:
• The project hasn't been indexed yet, or
• The project has no compatible files, or  
• The indexing process failed

To fix this, please index your project with content:
./scripts/rag_cli_v2.sh projects ingest {project_id} /path/to/your/project

After indexing, try your question again."""'''
    
    new_simple = '''f"""I couldn't find any meaningful indexed content for project {project_id}.

This usually means:
• The project contains only binary/image data (like base64 encoded files), or
• The project has no text-based files (code, docs, configs), or
• The indexing process filtered out all content as non-meaningful

**Immediate Solutions:**

1. **Add meaningful content** to your project directory:
   - README.md with project description
   - Source code files (.py, .js, .md, etc.)
   - Configuration files (package.json, config files)
   - Documentation files

2. **Run the fix tool** I've prepared for you:
   ```bash
   python comprehensive_project_fix.py
   ```
   This will create sample meaningful content and test the results.

3. **Create a new project** with existing code:
   ```bash
   ./scripts/rag_cli_v2.sh projects create "My Project" /path/to/your/code
   ```

4. **Check project content**: Your project may contain only images/binary data which provides no searchable context.

The chat interface needs text-based content to provide meaningful responses about your project."""'''
    
    if old_simple in content:
        print("✅ Found old response pattern, updating...")
        content = content.replace(old_simple, new_simple)
        
        # Also update the suggestion field
        content = content.replace("'suggestion': 'index_project'", "'suggestion': 'add_meaningful_content',\n                'fix_available': True")
        
        # Write the updated content back
        with open('rag_agent.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully updated rag_agent.py with improved empty project response")
        return True
    else:
        print("❌ Could not find the expected pattern in rag_agent.py")
        print("The file may have already been updated or the format has changed.")
        return False

if __name__ == "__main__":
    update_empty_project_response()