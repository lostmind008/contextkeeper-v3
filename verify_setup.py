#!/usr/bin/env python3
"""
Verify the ContextKeeper setup is working correctly.
This is a systematic test to ensure everything is properly configured.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_setup():
    """Verify the system setup step by step."""
    print("=" * 60)
    print("CONTEXTKEEPER SETUP VERIFICATION")
    print("=" * 60)
    
    # Step 1: Load environment variables
    print("\n1. Loading environment variables...")
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv(env_file)
        print(f"   ✅ Loaded .env file from {env_file.absolute()}")
    else:
        print(f"   ❌ No .env file found at {env_file.absolute()}")
        return False
    
    # Step 2: Check Google API key
    print("\n2. Checking Google API key...")
    api_key = os.environ.get('GOOGLE_API_KEY')
    if api_key:
        print(f"   ✅ GOOGLE_API_KEY is set ({len(api_key)} characters)")
    else:
        print("   ❌ GOOGLE_API_KEY not found in environment")
        print("   Please add GOOGLE_API_KEY=your-key-here to .env file")
        return False
    
    # Step 3: Test imports
    print("\n3. Testing imports...")
    try:
        from src.core.rag_agent import ProjectKnowledgeAgent
        print("   ✅ Can import ProjectKnowledgeAgent")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    try:
        from src.core.project_manager import ProjectManager
        print("   ✅ Can import ProjectManager")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    try:
        from src.sacred.sacred_layer_implementation import SacredLayerManager
        print("   ✅ Can import SacredLayerManager")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Step 4: Check required Python packages
    print("\n4. Checking required packages...")
    required_packages = [
        'flask',
        'chromadb',
        'google.generativeai',
        'tiktoken',
        'watchdog'
    ]
    
    for package in required_packages:
        try:
            __import__(package.split('.')[0])
            print(f"   ✅ {package} is installed")
        except ImportError:
            print(f"   ❌ {package} is NOT installed")
            print(f"      Run: pip install {package}")
            return False
    
    # Step 5: Initialize the agent with minimal config
    print("\n5. Initializing ProjectKnowledgeAgent...")
    try:
        config = {
            'db_path': './rag_knowledge_db',
            'projects_config_dir': 'projects',
            'default_file_extensions': ['.py', '.js', '.jsx', '.ts', '.tsx', '.md', '.json', '.yaml'],
            'legacy_watch_dirs': [],
            'chunk_size': 1000,
            'chunk_overlap': 200,
            'max_results': 10,
            'embedding_model': 'text-embedding-004',
            'api_port': 5556,
            'sensitive_patterns': [r'api[_-]?key', r'password', r'token'],
            'ignore_directories': [
                'node_modules', '.git', '__pycache__', 'venv', '.venv', 
                'env', 'myvenv', 'virtualenv', '.mypy_cache', '.pytest_cache'
            ],
            'ignore_files': [
                '*.pyc', '*.pyo', '*.pyd', '.DS_Store', '*.so',
                '*.dylib', '*.dll', '*.class', '*.log', '*.lock',
                '.gitignore', '.gitattributes', '.gitmodules'
            ]
        }
        
        agent = ProjectKnowledgeAgent(config)
        print("   ✅ Agent initialized successfully")
        
        # Try to access the database
        if hasattr(agent, 'db'):
            print("   ✅ ChromaDB connection established")
        else:
            print("   ⚠️  ChromaDB connection not verified")
            
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}")
        import traceback
        print("\nFull error trace:")
        traceback.print_exc()
        return False
    
    # Step 6: Check project directories
    print("\n6. Checking project directories...")
    directories = ['projects', 'rag_knowledge_db', 'test_sample_project']
    for dir_name in directories:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"   ✅ {dir_name}/ exists")
        else:
            print(f"   ⚠️  {dir_name}/ does not exist (will be created when needed)")
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = verify_setup()
    if success:
        print("\n✅ System is ready to use!")
        print("\nNext steps:")
        print("1. Run: python test_system.py")
        print("2. Or start server: python start_server.py server")
    else:
        print("\n❌ Setup verification failed. Please fix the issues above.")
    
    sys.exit(0 if success else 1)