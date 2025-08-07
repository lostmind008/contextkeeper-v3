import pytest
import asyncio
from src.core.rag_agent import ProjectKnowledgeAgent, RAGServer
from src.core.project_manager import ProjectManager
import os
import json
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="module")
def event_loop():
    """Overrides pytest-asyncio default event_loop fixture."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def test_agent():
    config = {
        "db_path": "./test_rag_knowledge_db",
        "projects_config_dir": os.path.expanduser("~/.test_rag_projects"),
        "default_file_extensions": [".py", ".md"],
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "max_results": 10,
        "embedding_model": "gemini-embedding-001",
        "api_port": 5557,
        "ignore_directories": ["node_modules", ".git", "__pycache__"],
        "ignore_files": ["*.log"],
        "sensitive_patterns": []
    }
    # Clean up previous test runs
    if os.path.exists(config["db_path"]):
        import shutil
        shutil.rmtree(config["db_path"])
    if os.path.exists(config["projects_config_dir"]):
        import shutil
        shutil.rmtree(config["projects_config_dir"])

    agent = ProjectKnowledgeAgent(config)

    # Mock the embedding client
    agent.embedder = MagicMock()
    agent.embedder.models.embed_content.return_value = MagicMock(embeddings=[MagicMock(values=[0.1] * 768)])

    # Create a test project
    agent.project_manager.create_project("Test Project", "/tmp/test_project", ["/tmp/test_project"])

    yield agent

    # Clean up
    if os.path.exists(config["db_path"]):
        import shutil
        shutil.rmtree(config["db_path"])
    if os.path.exists(config["projects_config_dir"]):
        import shutil
        shutil.rmtree(config["projects_config_dir"])

@pytest.fixture(scope="module")
def client(test_agent):
    server = RAGServer(test_agent, port=5557)
    with server.app.test_client() as client:
        yield client

def test_git_activity_endpoint(client):
    # This is a basic test, as we don't have a git repo initialized
    response = client.get('/projects/proj_1/git/activity')
    assert response.status_code == 404 # No git repo initialized

def test_create_sacred_plan(client):
    response = client.post('/sacred/plans', json={
        "project_id": "proj_1",
        "title": "Test Plan",
        "content": "This is a test plan."
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'created'
    assert 'plan_id' in data
    assert 'verification_code' in data

def test_analytics_summary_endpoint(client):
    response = client.get('/analytics/summary')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_projects' in data
    assert 'active_projects' in data
    assert 'projects' in data
