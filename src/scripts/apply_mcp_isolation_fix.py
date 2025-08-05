#!/usr/bin/env python3
"""
Apply the isolation fix to enhanced_mcp_server.js
This script patches the MCP server methods with project validation
"""

import re
import shutil
from datetime import datetime

def apply_mcp_isolation_fix():
    mcp_file = 'mcp-server/enhanced_mcp_server.js'
    
    # Create backup
    backup_name = f'mcp-server/enhanced_mcp_server.js.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    shutil.copy(mcp_file, backup_name)
    print(f"✅ Created backup: {backup_name}")
    
    # Read the current file
    with open(mcp_file, 'r') as f:
        content = f.read()
    
    # Read the fixed methods from the isolation fix file
    with open('PERPLEXITY_RESEARCH_PACKAGE/code_files/mcp_server_isolation_fix.js', 'r') as f:
        fix_content = f.read()
    
    # Extract the fixed intelligentSearch method
    intelligent_search_pattern = r'// Fix for intelligentSearch method.*?^}'
    match = re.search(intelligent_search_pattern, fix_content, re.DOTALL | re.MULTILINE)
    
    if match:
        fixed_intelligent_search = match.group(0)
        # Find and replace the intelligentSearch method in the original file
        original_pattern = r'async intelligentSearch\(args\) \{.*?^\s{2}\}'
        content = re.sub(original_pattern, fixed_intelligent_search[46:], content, flags=re.DOTALL | re.MULTILINE)
        print("✅ Updated intelligentSearch method")
    
    # Extract the fixed getDevelopmentContext method
    get_context_pattern = r'// Fix for getDevelopmentContext method.*?^}'
    match = re.search(get_context_pattern, fix_content, re.DOTALL | re.MULTILINE)
    
    if match:
        fixed_get_context = match.group(0)
        # Find and replace the getDevelopmentContext method
        original_pattern = r'async getDevelopmentContext\(args\) \{.*?^\s{2}\}'
        content = re.sub(original_pattern, fixed_get_context[40:], content, flags=re.DOTALL | re.MULTILINE)
        print("✅ Updated getDevelopmentContext method")
    
    # Extract and add the helper method
    helper_pattern = r'// Add helper method.*?^}'
    match = re.search(helper_pattern, fix_content, re.DOTALL | re.MULTILINE)
    
    if match:
        helper_method = match.group(0)[35:]  # Remove the comment
        # Find a good place to insert the helper (before the run method)
        run_pattern = r'(\s+async run\(\) \{)'
        content = re.sub(run_pattern, f'\n{helper_method}\n\\1', content)
        print("✅ Added validateAndGetProjectId helper method")
    
    # Write the updated content back
    with open(mcp_file, 'w') as f:
        f.write(content)
    
    print("✅ Successfully applied MCP server isolation fixes")
    return True

if __name__ == "__main__":
    apply_mcp_isolation_fix()