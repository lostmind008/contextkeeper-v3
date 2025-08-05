#!/usr/bin/env python3
"""
Quick script to fix the most critical sacred layer test issues
"""

import re
import sys
from pathlib import Path

def fix_test_file(filepath):
    """Fix the main test file issues"""
    print(f"Fixing {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix 1: Add @pytest.mark.asyncio and await for create_plan calls
    content = re.sub(
        r'(\s+)def (test_.*create_plan.*)\(self, sacred_manager\):',
        r'\1@pytest.mark.asyncio\n\1async def \2(self, sacred_manager):',
        content
    )
    
    content = re.sub(
        r'plan = sacred_manager\.create_plan\(',
        r'plan = await sacred_manager.create_plan(',
        content
    )
    
    content = re.sub(
        r'plan1 = sacred_manager\.create_plan\(',
        r'plan1 = await sacred_manager.create_plan(',
        content
    )
    
    content = re.sub(
        r'plan2 = sacred_manager\.create_plan\(',
        r'plan2 = await sacred_manager.create_plan(',
        content
    )
    
    # Fix 2: Change generate_verification_code to _generate_verification_code
    content = re.sub(
        r'sacred_manager\.generate_verification_code\(',
        r'sacred_manager._generate_verification_code(',
        content
    )
    
    # Fix 3: Add async for approval tests
    content = re.sub(
        r'(\s+)def (test_.*approval.*)\(self, sacred_manager\):',
        r'\1@pytest.mark.asyncio\n\1async def \2(self, sacred_manager):',
        content
    )
    
    # Fix 4: Update approve_plan calls to be async and match signature
    content = re.sub(
        r'approval_result = sacred_manager\.approve_plan\(',
        r'success, message = await sacred_manager.approve_plan(',
        content
    )
    
    # Fix 5: Update assertions for approval results
    content = re.sub(
        r'assert approval_result is True',
        r'assert success is True',
        content
    )
    
    content = re.sub(
        r'assert approval_result is False',
        r'assert success is False',
        content
    )
    
    # Fix 6: Update plan ID length expectation
    content = re.sub(
        r'assert len\(plan\.plan_id\) == 12',
        r'assert len(plan.plan_id) == 17  # "plan_" + 12 char hash',
        content
    )
    
    # Fix 7: Add missing imports
    if 'import time' not in content:
        content = content.replace('import os', 'import os\nimport time')
    
    # Write back
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"Fixed {filepath}")

if __name__ == "__main__":
    test_file = Path("/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/tests/sacred/test_sacred_layer.py")
    fix_test_file(test_file)
    print("Sacred layer test fixes completed!")