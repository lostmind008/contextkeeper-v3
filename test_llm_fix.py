#!/usr/bin/env python3
"""
Test script to verify LLM integration fix
"""

import asyncio
import sys
import os
import requests
import time
import subprocess
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_endpoint():
    """Test the /query_llm endpoint"""
    print("🧪 Testing /query_llm endpoint...")
    
    # Check if service is running
    try:
        health_response = requests.get('http://localhost:5556/health', timeout=5)
        if health_response.status_code != 200:
            print("❌ Service not running or unhealthy")
            return False
    except requests.exceptions.RequestException:
        print("❌ Service not accessible on port 5556")
        return False
    
    # Test the LLM endpoint
    test_query = {
        "question": "What is the sacred layer?",
        "k": 3,
        "project_id": "youtube_analyzer_legacy"  # Using the legacy project
    }
    
    try:
        response = requests.post(
            'http://localhost:5556/query_llm',
            json=test_query,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LLM endpoint working!")
            print(f"Question: {result.get('question', 'N/A')}")
            print(f"Answer preview: {result.get('answer', 'N/A')[:100]}...")
            print(f"Sources: {len(result.get('sources', []))} files")
            return True
        else:
            print(f"❌ LLM endpoint failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing LLM endpoint: {e}")
        return False

def test_client_attribute():
    """Test if the client attribute exists in ProjectKnowledgeAgent"""
    print("🧪 Testing client attribute existence...")
    
    try:
        from rag_agent import ProjectKnowledgeAgent
        
        # Get default config
        config = {
            'chunk_size': 1000,
            'chunk_overlap': 200,
            'embedding_model': 'gemini-embedding-001',
            'db_path': 'test_db',
            'sensitive_patterns': [],
            'ignore_directories': ['node_modules', '.git'],
            'ignore_files': ['*.pyc'],
            'default_file_extensions': ['.py', '.js', '.md']
        }
        
        # Test if we can create an agent without errors
        agent = ProjectKnowledgeAgent(config)
        
        # Check if client attribute exists
        if hasattr(agent, 'client'):
            print("✅ client attribute exists")
            if agent.client is not None:
                print("✅ client is initialized")
                return True
            else:
                print("❌ client is None")
                return False
        else:
            print("❌ client attribute missing")
            return False
            
    except Exception as e:
        print(f"❌ Error testing client attribute: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 Testing LLM Integration Fix")
    print("=" * 50)
    
    # Test 1: Client attribute
    client_test = test_client_attribute()
    
    # Test 2: API endpoint (only if service is running)
    api_test = test_api_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Client Attribute: {'✅ PASS' if client_test else '❌ FAIL'}")
    print(f"API Endpoint: {'✅ PASS' if api_test else '❌ FAIL'}")
    
    if client_test and api_test:
        print("\n🎉 All tests passed! LLM integration fix successful.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)