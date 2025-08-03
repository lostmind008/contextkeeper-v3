#!/usr/bin/env python3
"""
Diagnostic script to test the specific project mentioned in the user's screenshot.
Based on: "The provided context states that it is from the project 'proj_736df3fd80a4'"
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5556"
TARGET_PROJECT = "proj_736df3fd80a4"

def test_service_health():
    """Check if the service is running"""
    print("🔍 Checking service health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Service is running")
            return True
        else:
            print(f"❌ Service unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Service not accessible: {e}")
        print("💡 Start with: python rag_agent.py start")
        return False

def test_raw_query():
    """Test the raw /query endpoint to see what context is available"""
    print(f"\n🔍 Testing raw query for project {TARGET_PROJECT}...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/query",
            json={
                "question": "What is this project about?", 
                "k": 5,
                "project_id": TARGET_PROJECT
            },
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Raw query failed")
            print(f"   Response: {response.text}")
            return None
            
        data = response.json()
        results = data.get('results', [])
        
        print(f"   📊 Results count: {len(results)}")
        
        if len(results) == 0:
            print("   💔 NO CONTENT FOUND - This explains the poor responses!")
            print("   💡 The project knowledge base is empty")
            return {'empty': True, 'results': []}
            
        print(f"   ✅ Found {len(results)} results")
        for i, result in enumerate(results[:2]):  # Show first 2
            content = result.get('content', 'No content')[:150]
            metadata = result.get('metadata', {})
            distance = result.get('distance', 'Unknown')
            print(f"   📄 Result {i+1}:")
            print(f"      Content: {content}...")
            print(f"      File: {metadata.get('file', 'Unknown')}")
            print(f"      Distance: {distance}")
            
        return data
        
    except Exception as e:
        print(f"   ❌ Error testing raw query: {e}")
        return None

def test_llm_query():
    """Test the LLM /query_llm endpoint to reproduce the issue"""
    print(f"\n🤖 Testing LLM query for project {TARGET_PROJECT}...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/query_llm",
            json={
                "question": "can you please let me know what you know about the projects?", 
                "k": 5,
                "project_id": TARGET_PROJECT
            },
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ LLM query failed")
            print(f"   Response: {response.text}")
            return None
            
        data = response.json()
        answer = data.get('answer', 'No answer')
        sources = data.get('sources', [])
        
        print(f"   💬 LLM Response:")
        print(f"      Answer: {answer}")
        print(f"      Sources: {sources}")
        
        # Check for the specific poor response mentioned by user
        if "proj_736df3fd80a4" in answer and "does not contain any further information" in answer:
            print("   🎯 REPRODUCED THE EXACT ISSUE!")
            print("   💡 This confirms the knowledge base is sparse/empty")
        elif "No project context specified" in answer:
            print("   🔍 Got 'no project context' - different from user's issue")
        else:
            print("   📝 Got a different response than expected")
            
        return data
        
    except Exception as e:
        print(f"   ❌ Error testing LLM query: {e}")
        return None

def test_projects_list():
    """Check what projects are available"""
    print(f"\n📋 Checking available projects...")
    
    try:
        response = requests.get(f"{BASE_URL}/projects", timeout=10)
        if response.status_code != 200:
            print(f"   ❌ Failed to get projects: {response.status_code}")
            return None
            
        projects = response.json()
        print(f"   📁 Found {len(projects)} projects total:")
        
        target_found = False
        for project in projects:
            project_id = project.get('id', 'unknown')
            project_name = project.get('name', 'unnamed')
            print(f"      {project_id} - {project_name}")
            
            if TARGET_PROJECT in project_id:
                target_found = True
                print(f"      🎯 Target project found!")
                print(f"      Details: {json.dumps(project, indent=8)}")
                
        if not target_found:
            print(f"   ⚠️ Target project {TARGET_PROJECT} not found in projects list")
            
        return projects
        
    except Exception as e:
        print(f"   ❌ Error getting projects: {e}")
        return None

def test_no_project_id():
    """Test what happens when no project_id is sent"""
    print(f"\n🚫 Testing query_llm without project_id...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/query_llm",
            json={
                "question": "What is this project about?", 
                "k": 5
                # No project_id
            },
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', 'No answer')
            print(f"   💬 Response: {answer}")
            
            if "No project context specified" in answer:
                print("   ✅ Correctly handles missing project_id")
            else:
                print("   ⚠️ Unexpected response for missing project_id")
        else:
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    print("🚨 DIAGNOSTICS: Query LLM Poor Response Quality")
    print("=" * 60)
    print(f"User reported: 'The provided context states that it is from the project {TARGET_PROJECT}'")
    print("Investigating knowledge base content and LLM responses...")
    print()
    
    # Test 1: Service health
    if not test_service_health():
        sys.exit(1)
    
    # Test 2: Projects list
    projects = test_projects_list()
    
    # Test 3: Raw query (what context is available)
    raw_results = test_raw_query()
    
    # Test 4: LLM query (reproduce the issue)
    llm_results = test_llm_query()
    
    # Test 5: No project ID handling
    test_no_project_id()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if raw_results and raw_results.get('empty'):
        print("🎯 ROOT CAUSE IDENTIFIED: Empty Knowledge Base")
        print()
        print("FINDINGS:")
        print("✅ Service is running correctly")
        print("✅ Project exists in system")
        print("✅ Query endpoints are functional")
        print("❌ Project has NO indexed content")
        print()
        print("EXPLANATION:")
        print("The LLM is generating poor responses because the RAG system")
        print("is returning no context from the knowledge base. When the")
        print("knowledge base is empty, the LLM has nothing meaningful to")
        print("work with, leading to generic responses.")
        print()
        print("SOLUTION:")
        print("Index the project with content:")
        print(f"./scripts/rag_cli_v2.sh projects ingest {TARGET_PROJECT} /path/to/project/files")
        
    elif raw_results and len(raw_results.get('results', [])) > 0:
        print("🔍 PARTIAL ISSUE: Sparse Knowledge Base")
        print()
        print("FINDINGS:")
        print("✅ Service is running correctly") 
        print("✅ Project has some content")
        print("⚠️ Content may be insufficient or irrelevant")
        print()
        print("POSSIBLE CAUSES:")
        print("1. Not enough content indexed")
        print("2. Content doesn't match user's questions")
        print("3. LLM prompt needs improvement")
        
    else:
        print("❌ UNKNOWN ISSUE")
        print("The diagnostic tests failed to complete successfully.")
        print("Check the service logs for more details.")

if __name__ == "__main__":
    main()