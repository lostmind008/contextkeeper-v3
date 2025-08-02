#!/usr/bin/env python3
"""
Test script to verify the Google GenAI API usage pattern
"""

import os
from google import genai

def test_genai_patterns():
    """Test different Google GenAI API patterns"""
    
    # Set test API key if not present
    if not os.getenv('GOOGLE_API_KEY'):
        print("⚠️ GOOGLE_API_KEY not set, using test key")
        os.environ['GOOGLE_API_KEY'] = 'test-key-for-api-pattern-check'
    
    try:
        # Initialize client like in our fixed code
        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        print("✅ Client initialized successfully")
        print(f"   Client type: {type(client)}")
        
        # Check if models attribute exists
        if hasattr(client, 'models'):
            print("✅ client.models attribute exists")
            print(f"   models type: {type(client.models)}")
            
            # Check if generate_content method exists
            if hasattr(client.models, 'generate_content'):
                print("✅ client.models.generate_content method exists")
                print("✅ API pattern validation successful!")
                
                # Show method signature info if possible
                import inspect
                try:
                    sig = inspect.signature(client.models.generate_content)
                    print(f"   Method signature: {sig}")
                except:
                    print("   (Could not retrieve method signature)")
                
            else:
                print("❌ client.models.generate_content method missing")
        else:
            print("❌ client.models attribute missing")
            
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        print(f"   Exception type: {type(e)}")

def test_alternative_patterns():
    """Test alternative API patterns"""
    print("\n🔍 Testing alternative patterns...")
    
    try:
        # Test direct genai usage
        if hasattr(genai, 'generate_content'):
            print("✅ genai.generate_content exists (alternative pattern)")
        else:
            print("❌ genai.generate_content not found")
            
    except Exception as e:
        print(f"❌ Error testing alternatives: {e}")

if __name__ == "__main__":
    print("🧪 Testing Google GenAI API Patterns")
    print("=" * 50)
    
    test_genai_patterns()
    test_alternative_patterns()
    
    print("\n" + "=" * 50)
    print("✅ API pattern testing complete")
    print("\nExpected usage in rag_agent.py:")
    print("   self.client.models.generate_content(model='gemini-2.5-flash', contents='...')")