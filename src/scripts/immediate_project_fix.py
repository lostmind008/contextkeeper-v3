#!/usr/bin/env python3
"""
Immediate Project Fix Script
===========================

This script provides immediate solutions for the user's project indexing issue.
It includes both diagnosis and practical fixes.
"""

import os
import sys
import json
import requests
from pathlib import Path

def get_project_info():
    """Get current project information"""
    try:
        response = requests.get("http://localhost:5556/projects")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"❌ Failed to get projects: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error connecting to agent: {e}")
        print("💡 Make sure ContextKeeper is running: source venv/bin/activate && python rag_agent.py start")
        return None

def test_query_project(project_id: str):
    """Test querying the problematic project"""
    try:
        # Test raw query
        raw_response = requests.post("http://localhost:5556/query", json={
            "question": "What is this project about?",
            "project_id": project_id,
            "k": 5
        })
        
        # Test LLM query
        llm_response = requests.post("http://localhost:5556/query_llm", json={
            "question": "What is this project about?",
            "project_id": project_id,
            "k": 5
        })
        
        return {
            'raw': raw_response.json() if raw_response.status_code == 200 else None,
            'llm': llm_response.json() if llm_response.status_code == 200 else None
        }
    except Exception as e:
        print(f"❌ Error testing queries: {e}")
        return None

def create_sample_content(project_path: str):
    """Create sample meaningful content for testing"""
    if not os.path.exists(project_path):
        print(f"❌ Project path doesn't exist: {project_path}")
        return False
    
    # Create a README.md with project description
    readme_path = os.path.join(project_path, "README.md")
    readme_content = """# Project Overview

This is a sample project created to test ContextKeeper's knowledge indexing capabilities.

## Purpose

This project demonstrates how ContextKeeper can index and understand project content 
to provide meaningful responses in the chat interface.

## Features

- Sample documentation structure
- Configuration examples
- Code snippets for testing
- Meaningful content for AI analysis

## Architecture

The project follows a simple structure:
- Documentation in markdown files
- Configuration in JSON/YAML files
- Source code in appropriate directories

## Getting Started

1. Clone the repository
2. Install dependencies
3. Run the application
4. Test the chat interface

## Notes

This content was generated to provide ContextKeeper with meaningful text to index
and understand, replacing base64 image data that provided no useful context.
"""
    
    # Create a package.json with meaningful metadata
    package_json_path = os.path.join(project_path, "package.json")
    package_content = {
        "name": "contextkeeper-test-project",
        "version": "1.0.0",
        "description": "A test project for demonstrating ContextKeeper's indexing capabilities",
        "main": "index.js",
        "scripts": {
            "start": "node index.js",
            "test": "jest",
            "build": "webpack --mode production",
            "dev": "webpack serve --mode development"
        },
        "keywords": [
            "contextkeeper",
            "knowledge-management",
            "ai-assistant",
            "documentation",
            "indexing"
        ],
        "author": "ContextKeeper User",
        "license": "MIT",
        "dependencies": {
            "express": "^4.18.0",
            "react": "^18.0.0",
            "axios": "^1.0.0"
        },
        "devDependencies": {
            "webpack": "^5.0.0",
            "jest": "^29.0.0",
            "eslint": "^8.0.0"
        }
    }
    
    # Create a simple config file
    config_path = os.path.join(project_path, "config.json")
    config_content = {
        "application": {
            "name": "ContextKeeper Test Project",
            "version": "1.0.0",
            "environment": "development"
        },
        "database": {
            "type": "sqlite",
            "path": "./data/app.db"
        },
        "api": {
            "port": 3000,
            "host": "localhost",
            "cors": True
        },
        "features": {
            "chat_interface": True,
            "knowledge_indexing": True,
            "project_tracking": True
        }
    }
    
    try:
        # Write README.md
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        print(f"✅ Created: {readme_path}")
        
        # Write package.json
        with open(package_json_path, 'w') as f:
            json.dump(package_content, f, indent=2)
        print(f"✅ Created: {package_json_path}")
        
        # Write config.json
        with open(config_path, 'w') as f:
            json.dump(config_content, f, indent=2)
        print(f"✅ Created: {config_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample content: {e}")
        return False

def main():
    print("🔧 ContextKeeper Project Fix Tool")
    print("=" * 40)
    
    # 1. Check agent status
    print("1️⃣ Checking ContextKeeper status...")
    projects_data = get_project_info()
    if not projects_data:
        return
    
    print(f"✅ ContextKeeper is running")
    print(f"   Total projects: {projects_data.get('total_projects', 0)}")
    
    # 2. Find the problematic project
    target_project_id = "proj_736df3fd80a4"
    target_project = None
    
    for project in projects_data.get('projects', []):
        if project['id'] == target_project_id:
            target_project = project
            break
    
    if not target_project:
        print(f"❌ Project {target_project_id} not found")
        print("Available projects:")
        for proj in projects_data.get('projects', []):
            print(f"   - {proj['name']} ({proj['id']})")
        return
    
    print(f"2️⃣ Found problematic project:")
    print(f"   Name: {target_project['name']}")
    print(f"   ID: {target_project['id']}")
    print(f"   Path: {target_project.get('root_path', 'Unknown')}")
    print(f"   Status: {target_project.get('status', 'Unknown')}")
    
    # 3. Test current queries
    print(f"\n3️⃣ Testing current query responses...")
    query_results = test_query_project(target_project_id)
    
    if query_results:
        raw_count = len(query_results['raw'].get('results', [])) if query_results['raw'] else 0
        print(f"   Raw query results: {raw_count} items")
        
        if query_results['llm'] and 'answer' in query_results['llm']:
            answer_length = len(query_results['llm']['answer'])
            print(f"   LLM response length: {answer_length} characters")
            if answer_length < 200:
                print(f"   ⚠️  Response is very short (likely poor quality)")
        else:
            print(f"   ❌ No LLM response received")
    
    # 4. Offer solutions
    print(f"\n4️⃣ Available Solutions:")
    print(f"   A) Add meaningful content to existing project")
    print(f"   B) Create a new project with proper content")
    print(f"   C) Re-index project after adding content")
    
    choice = input("\nChoose solution (A/B/C): ").upper()
    
    if choice == 'A':
        project_path = target_project.get('root_path')
        if project_path and os.path.exists(project_path):
            print(f"\n🔧 Adding meaningful content to {project_path}...")
            if create_sample_content(project_path):
                print(f"\n✅ Sample content created!")
                print(f"📝 Next steps:")
                print(f"   1. Wait 30 seconds for auto-indexing, or")
                print(f"   2. Restart ContextKeeper to force re-indexing")
                print(f"   3. Test the chat interface again")
            else:
                print(f"❌ Failed to create sample content")
        else:
            print(f"❌ Project path not accessible: {project_path}")
    
    elif choice == 'B':
        print(f"\n🔧 Creating new project with meaningful content...")
        print(f"💡 Use this command:")
        print(f'   ./scripts/rag_cli_v2.sh projects create "My Test Project" "/path/to/new/project"')
        print(f"\n📝 Then create content in the new project directory:")
        print(f"   - README.md with project description")
        print(f"   - package.json or requirements.txt")
        print(f"   - Source code files")
        print(f"   - Documentation files")
    
    elif choice == 'C':
        print(f"\n🔧 Project re-indexing...")
        print(f"⚠️  Note: ContextKeeper doesn't have a manual re-index command yet.")
        print(f"💡 Workarounds:")
        print(f"   1. Restart ContextKeeper agent")
        print(f"   2. Modify a file in the project (triggers auto-reindex)")
        print(f"   3. Add new meaningful content (auto-indexed)")
    
    else:
        print(f"❌ Invalid choice. Please run script again.")

if __name__ == "__main__":
    main()