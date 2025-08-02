#!/usr/bin/env python3
"""
Simple test to check if client attribute is properly initialized
"""

import os
import sys
from pathlib import Path

# Set up environment variables if not already set
if not os.getenv('GOOGLE_API_KEY'):
    os.environ['GOOGLE_API_KEY'] = 'test-key-for-initialization-check'
if not os.getenv('GEMINI_API_KEY'):
    os.environ['GEMINI_API_KEY'] = 'test-key-for-initialization-check'

try:
    from rag_agent import ProjectKnowledgeAgent
    
    print("✅ Successfully imported ProjectKnowledgeAgent")
    
    # Test basic config
    config = {
        'chunk_size': 1000,
        'chunk_overlap': 200,
        'embedding_model': 'gemini-embedding-001',
        'db_path': './test_db',
        'sensitive_patterns': [],
        'ignore_directories': ['node_modules', '.git', '__pycache__', 'venv'],
        'ignore_files': ['*.pyc', '*.pyo'],
        'default_file_extensions': ['.py', '.js', '.md'],
        'projects_config_dir': './projects'
    }
    
    # Create test directories if they don't exist
    Path('./test_db').mkdir(exist_ok=True)
    Path('./projects').mkdir(exist_ok=True)
    
    try:
        agent = ProjectKnowledgeAgent(config)
        print("✅ Successfully created ProjectKnowledgeAgent instance")
        
        # Check for client attribute
        if hasattr(agent, 'client'):
            print("✅ client attribute exists")
            print(f"   client type: {type(agent.client)}")
            if agent.client is not None:
                print("✅ client is not None")
            else:
                print("❌ client is None")
        else:
            print("❌ client attribute missing")
        
        # Check for embedder attribute
        if hasattr(agent, 'embedder'):
            print("✅ embedder attribute exists")
            print(f"   embedder type: {type(agent.embedder)}")
        else:
            print("❌ embedder attribute missing")
            
        print("\n🎉 Client initialization test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error creating ProjectKnowledgeAgent: {e}")
        print(f"   Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("   Make sure you're in the correct directory and all dependencies are installed")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()