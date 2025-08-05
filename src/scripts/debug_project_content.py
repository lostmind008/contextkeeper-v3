#!/usr/bin/env python3
"""
Debug script to investigate why query_llm responses are poor quality.
Based on user screenshot showing: "The provided context states that it is from the project 'proj_736df3fd80a4'"

This suggests the LLM is getting minimal context from the knowledge base.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5556"

def check_rag_agent_status():
    """Check if RAG agent is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ RAG agent is running")
            return True
        else:
            print(f"❌ RAG agent health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ RAG agent is not running: {e}")
        return False

def investigate_projects():
    """Get list of projects and their content"""
    print("\n🔍 Investigating available projects...")
    
    try:
        response = requests.get(f"{BASE_URL}/projects", timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to get projects: {response.status_code}")
            return None
            
        projects = response.json()
        print(f"📋 Found {len(projects)} projects:")
        
        for project in projects:
            project_id = project.get('id', 'unknown')
            project_name = project.get('name', 'unnamed')
            print(f"   📁 {project_id} - {project_name}")
            
            # Check if this is the problematic project
            if 'proj_736df3fd80a4' in project_id:
                print(f"   🎯 Found the problematic project!")
                print(f"   Project details: {json.dumps(project, indent=6)}")
                return project_id
                
        return projects[0].get('id') if projects else None
        
    except Exception as e:
        print(f"❌ Error getting projects: {e}")
        return None

def test_raw_query(project_id):
    """Test the raw /query endpoint to see what context is available"""
    print(f"\n🔍 Testing raw query for project {project_id}...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/query",
            json={
                "question": "What is this project about?", 
                "k": 5,
                "project_id": project_id
            },
            timeout=15
        )
        
        if response.status_code != 200:
            print(f"❌ Raw query failed: {response.status_code}")
            return None
            
        data = response.json()
        results = data.get('results', [])
        
        print(f"📊 Raw query returned {len(results)} results:")
        
        if not results:
            print("   💔 NO CONTENT FOUND - This explains the poor responses!")
            print("   💡 The project likely has an empty knowledge base")
            return None
            
        for i, result in enumerate(results[:3]):  # Show first 3
            content = result.get('content', 'No content')[:200]  # First 200 chars
            metadata = result.get('metadata', {})
            print(f"   📄 Result {i+1}:")
            print(f"      Content: {content}...")
            print(f"      File: {metadata.get('file', 'Unknown')}")
            print(f"      Score: {result.get('distance', 'Unknown')}")
            
        return data
        
    except Exception as e:
        print(f"❌ Error testing raw query: {e}")
        return None

def test_llm_query(project_id):
    """Test the LLM /query_llm endpoint to see the actual response"""
    print(f"\n🤖 Testing LLM query for project {project_id}...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/query_llm",
            json={
                "question": "What is this project about?", 
                "k": 5,
                "project_id": project_id
            },
            timeout=15
        )
        
        if response.status_code != 200:
            print(f"❌ LLM query failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
        data = response.json()
        answer = data.get('answer', 'No answer')
        sources = data.get('sources', [])
        
        print(f"💬 LLM Response:")
        print(f"   Answer: {answer}")
        print(f"   Sources: {sources}")
        
        # Check for the specific poor response mentioned by user
        if answer == "The provided context states that it is from the project 'proj_736df3fd80a4'":
            print("   🎯 FOUND THE EXACT ISSUE!")
            print("   💡 This suggests the LLM is getting minimal context")
            
        return data
        
    except Exception as e:
        print(f"❌ Error testing LLM query: {e}")
        return None

def diagnose_collection(project_id):
    """Try to get collection info if possible"""
    print(f"\n🗄️ Checking collection info for project {project_id}...")
    
    try:
        # Try the collection endpoint if it exists
        response = requests.get(f"{BASE_URL}/projects/{project_id}/collection", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Collection data: {json.dumps(data, indent=4)}")
        else:
            print(f"   Collection endpoint not available or failed: {response.status_code}")
            
    except Exception as e:
        print(f"   Collection check failed: {e}")

def main():
    print("🚨 DEBUG: Query LLM Poor Response Quality")
    print("=" * 50)
    print("User reported: 'The provided context states that it is from the project proj_736df3fd80a4'")
    print("This suggests the knowledge base is empty or has minimal content.")
    print()
    
    # Check if service is running
    if not check_rag_agent_status():
        print("\n❌ RAG agent not running. Start it with: python rag_agent.py start")
        sys.exit(1)
    
    # Get projects
    project_id = investigate_projects()
    if not project_id:
        print("\n❌ No projects found")
        sys.exit(1)
    
    # Use the specific project mentioned in the issue
    target_project = "proj_736df3fd80a4"
    print(f"\n🎯 Focusing on problematic project: {target_project}")
    
    # Test raw query first
    raw_results = test_raw_query(target_project)
    
    # Test LLM query
    llm_results = test_llm_query(target_project)
    
    # Try to get collection info
    diagnose_collection(target_project)
    
    # Summary
    print("\n📋 DIAGNOSIS SUMMARY:")
    print("=" * 30)
    
    if raw_results and raw_results.get('results'):
        print("✅ Raw query has content - LLM prompt may need improvement")
    else:
        print("❌ Raw query has NO content - project knowledge base is empty!")
        print("💡 SOLUTION: The project needs to be re-indexed with content")
        print("   Run: ./scripts/rag_cli_v2.sh projects ingest <project_id> <path>")
    
    if llm_results:
        answer = llm_results.get('answer', '')
        if 'proj_736df3fd80a4' in answer and len(answer) < 100:
            print("🎯 CONFIRMED: LLM is getting minimal context")
            print("💡 Root cause: Empty or sparse knowledge base")

if __name__ == "__main__":
    main()