#!/usr/bin/env python3
"""
Comprehensive test script to verify all converted Flask async endpoints work
"""
import sys
import requests  
import time
import threading
import json
sys.path.append('.')
from rag_agent import RAGServer, ProjectKnowledgeAgent, CONFIG

def test_all_endpoints():
    time.sleep(3)  # Wait for server to start
    
    endpoints_to_test = [
        {
            'name': 'Health (sync control)',
            'method': 'GET', 
            'url': 'http://localhost:5557/health',
            'expected_status': 200
        },
        {
            'name': 'Query (converted async)',
            'method': 'POST',
            'url': 'http://localhost:5557/query',
            'data': {'question': 'test query', 'k': 1},
            'expected_status': 200
        },
        {
            'name': 'Query LLM (converted async)', 
            'method': 'POST',
            'url': 'http://localhost:5557/query_llm',
            'data': {'question': 'test question', 'k': 1},
            'expected_status': 200
        }
    ]
    
    print('🧪 Testing all converted async endpoints...\n')
    
    for test in endpoints_to_test:
        try:
            if test['method'] == 'GET':
                response = requests.get(test['url'], timeout=10)
            else:
                response = requests.post(test['url'], json=test['data'], timeout=15)
            
            status = '✅ SUCCESS' if response.status_code == test['expected_status'] else '❌ FAILED'
            print(f"{status}: {test['name']} - Status: {response.status_code}")
            
            if response.status_code != test['expected_status']:
                print(f"  Error details: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ FAILED: {test['name']} - Exception: {e}")
    
    print('\n🎉 Comprehensive test completed!')

if __name__ == '__main__':
    print('🔧 Flask Async Compatibility Fix - Comprehensive Test\n')
    
    # Start server on different port to avoid conflicts
    agent = ProjectKnowledgeAgent(CONFIG)
    server = RAGServer(agent, 5557)
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()
    
    test_all_endpoints()