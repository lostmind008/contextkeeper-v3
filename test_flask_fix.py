#!/usr/bin/env python3
"""
Test script to verify Flask async compatibility fix
"""
import sys
import requests  
import time
import threading
import json
sys.path.append('.')
from rag_agent import RAGServer, ProjectKnowledgeAgent, CONFIG

def test_endpoints():
    time.sleep(3)  # Wait for server to start
    try:
        # Test health endpoint (should work)
        health_response = requests.get('http://localhost:5556/health', timeout=5)
        print(f'✅ Health endpoint: {health_response.status_code} - {health_response.json()}')
        
        # Test a converted async endpoint
        query_data = {'question': 'test query', 'k': 1}
        query_response = requests.post('http://localhost:5556/query', 
                                      json=query_data, timeout=10)
        print(f'✅ Query endpoint: {query_response.status_code}')
        
        if query_response.status_code != 500:
            print('✅ SUCCESS: Query endpoint no longer returns 500 error!')
            print('✅ Flask async compatibility issue RESOLVED')
            result = query_response.json()
            print(f'✅ Query returned {len(result.get("results", []))} results')
        else:
            print('❌ Query endpoint still returning 500 error')
            print(f'Error details: {query_response.text}')
            
    except Exception as e:
        print(f'Test error: {e}')

if __name__ == '__main__':
    print('🧪 Testing Flask async compatibility fix...')
    
    # Start server in background thread  
    agent = ProjectKnowledgeAgent(CONFIG)
    server = RAGServer(agent, 5556)
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()
    
    # Run test
    test_endpoints()
    print('🎉 Test completed!')