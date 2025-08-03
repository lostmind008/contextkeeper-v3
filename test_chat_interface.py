#!/usr/bin/env python3
"""Test script to verify the chat interface integration with query_llm endpoint"""

import requests
import json
import time

BASE_URL = "http://localhost:5556"

def test_chat_queries():
    """Test various chat queries through the query_llm endpoint"""
    
    test_queries = [
        {
            "question": "What are my active projects?",
            "description": "Query about active projects"
        },
        {
            "question": "Show me recent decisions",
            "description": "Query about recent decisions"
        },
        {
            "question": "What is the sacred layer?",
            "description": "Query about sacred layer concept"
        },
        {
            "question": "What recent events have been tracked?",
            "description": "Query about event tracking",
            "project_id": "proj_736df3fd80a4"  # veo3app project
        }
    ]
    
    print("🧪 Testing Chat Interface Queries")
    print("=" * 50)
    
    for test in test_queries:
        print(f"\n📝 {test['description']}")
        print(f"Question: {test['question']}")
        
        payload = {
            "question": test["question"],
            "k": 5
        }
        
        # Add project_id if specified
        if "project_id" in test:
            payload["project_id"] = test["project_id"]
        
        try:
            response = requests.post(
                f"{BASE_URL}/query_llm",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response received:")
                print(f"   Answer: {data.get('answer', 'No answer')[:200]}...")
                if 'sources' in data and data['sources']:
                    print(f"   Sources: {len(data['sources'])} files referenced")
                print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
            else:
                print(f"❌ Error: Status {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        
        time.sleep(1)  # Rate limiting

def test_dashboard_access():
    """Test dashboard HTML access"""
    print("\n🌐 Testing Dashboard Access")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/analytics_dashboard_live.html")
        if response.status_code == 200:
            # Check if chat components are in the HTML
            html_content = response.text
            chat_components = [
                "chat-container",
                "chatPanel",
                "chatMessages", 
                "chatInput",
                "ContextKeeper AI",
                "query_llm"
            ]
            
            found_components = []
            missing_components = []
            
            for component in chat_components:
                if component in html_content:
                    found_components.append(component)
                else:
                    missing_components.append(component)
            
            print(f"✅ Dashboard loaded successfully")
            print(f"✅ Found chat components: {', '.join(found_components)}")
            
            if missing_components:
                print(f"⚠️  Missing components: {', '.join(missing_components)}")
            else:
                print("✅ All chat components present!")
                
        else:
            print(f"❌ Dashboard access failed: Status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def main():
    """Run all tests"""
    print("🚀 ContextKeeper Chat Interface Test Suite")
    print("=" * 50)
    
    # Test 1: Dashboard access
    test_dashboard_access()
    
    # Test 2: Chat queries
    test_chat_queries()
    
    print("\n✨ Test suite completed!")
    print("\n📌 Next Steps:")
    print("1. Open http://localhost:5556/analytics_dashboard_live.html in your browser")
    print("2. Click the purple chat button in the bottom-right corner")
    print("3. Try the quick action buttons or type custom queries")
    print("4. Check that responses appear with proper formatting")

if __name__ == "__main__":
    main()