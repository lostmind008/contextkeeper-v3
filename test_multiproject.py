#!/usr/bin/env python3
"""
Test script for multi-project RAG agent functionality
"""

import asyncio
import json
import os
import tempfile
from pathlib import Path

# Add the rag-agent directory to Python path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from project_manager import ProjectManager, ProjectStatus
from rag_agent import ProjectKnowledgeAgent, CONFIG

async def test_multi_project():
    """Test multi-project functionality"""
    print("🧪 Testing Multi-Project RAG Agent v2.0")
    print("=" * 50)
    
    # Create temporary test directories
    test_dir = tempfile.mkdtemp(prefix="rag_test_")
    project1_dir = Path(test_dir) / "project1"
    project2_dir = Path(test_dir) / "project2"
    project1_dir.mkdir()
    project2_dir.mkdir()
    
    # Create test files
    (project1_dir / "test1.py").write_text("""
def authenticate_user(username, password):
    '''Authenticate user with JWT tokens'''
    # This is project 1 authentication
    return create_jwt_token(username)
""")
    
    (project2_dir / "test2.py").write_text("""
def authenticate_user(email, api_key):
    '''Authenticate user with API keys'''
    # This is project 2 authentication
    return validate_api_key(email, api_key)
""")
    
    try:
        # Test 1: Project Manager
        print("\n1️⃣ Testing ProjectManager...")
        pm = ProjectManager(str(Path(test_dir) / "test_projects"))
        
        # Create projects
        proj1 = pm.create_project("Test Project 1", str(project1_dir), 
                                 description="Testing project 1")
        print(f"   ✅ Created project: {proj1.name} ({proj1.project_id})")
        
        proj2 = pm.create_project("Test Project 2", str(project2_dir),
                                 description="Testing project 2")
        print(f"   ✅ Created project: {proj2.name} ({proj2.project_id})")
        
        # Test project lifecycle
        pm.pause_project(proj1.project_id)
        print(f"   ✅ Paused project: {proj1.project_id}")
        
        pm.resume_project(proj1.project_id)
        print(f"   ✅ Resumed project: {proj1.project_id}")
        
        # Test decisions and objectives
        decision = pm.add_decision(proj1.project_id, 
                                  "Use JWT for authentication",
                                  "Industry standard, stateless",
                                  ["auth", "security"])
        print(f"   ✅ Added decision: {decision.decision}")
        
        objective = pm.add_objective(proj1.project_id,
                                    "Implement user login",
                                    "Basic authentication flow",
                                    "high")
        print(f"   ✅ Added objective: {objective.title}")
        
        # Test 2: RAG Agent Integration
        print("\n2️⃣ Testing RAG Agent with projects...")
        
        # Create test config
        test_config = CONFIG.copy()
        test_config['db_path'] = str(Path(test_dir) / "test_db")
        test_config['projects_config_dir'] = str(Path(test_dir) / "test_projects")
        test_config['legacy_watch_dirs'] = []  # Don't import legacy
        
        # Initialize agent
        agent = ProjectKnowledgeAgent(test_config)
        agent.project_manager = pm  # Use our test project manager
        agent._init_project_collections()
        
        # Ingest files
        chunks1 = await agent.ingest_file(str(project1_dir / "test1.py"), proj1.project_id)
        print(f"   ✅ Ingested {chunks1} chunks from project 1")
        
        chunks2 = await agent.ingest_file(str(project2_dir / "test2.py"), proj2.project_id)
        print(f"   ✅ Ingested {chunks2} chunks from project 2")
        
        # Test project-specific queries
        print("\n3️⃣ Testing project-specific queries...")
        
        # Query project 1
        pm.set_focus(proj1.project_id)
        results1 = await agent.query("How does authentication work?")
        print(f"   ✅ Query project 1: Found {len(results1['results'])} results")
        if results1['results']:
            print(f"      Content: {results1['results'][0]['content'][:100]}...")
        
        # Query project 2
        pm.set_focus(proj2.project_id)
        results2 = await agent.query("How does authentication work?")
        print(f"   ✅ Query project 2: Found {len(results2['results'])} results")
        if results2['results']:
            print(f"      Content: {results2['results'][0]['content'][:100]}...")
        
        # Test context export
        print("\n4️⃣ Testing context export...")
        context = pm.export_context(proj1.project_id)
        print(f"   ✅ Exported context for project 1:")
        print(f"      - Decisions: {context['statistics']['total_decisions']}")
        print(f"      - Objectives: {context['statistics']['total_objectives']}")
        print(f"      - Recent decision: {context['recent_decisions'][0]['decision']}")
        
        # Test project summary
        print("\n5️⃣ Testing project summary...")
        summary = pm.get_project_summary()
        print(f"   ✅ Project summary:")
        print(f"      - Total projects: {summary['total_projects']}")
        print(f"      - Active projects: {summary['active_projects']}")
        print(f"      - Focused project: {summary['focused_project']}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)
        print(f"\n🧹 Cleaned up test directory: {test_dir}")

if __name__ == "__main__":
    asyncio.run(test_multi_project())