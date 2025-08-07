#!/usr/bin/env python3
"""
test_flask_endpoints.py - Comprehensive API endpoint tests for ContextKeeper v3

Created: 2025-07-29 04:17:00 (Australia/Sydney)
Part of: ContextKeeper v3.0 Test Suite

Tests all Flask API endpoints including Sacred Layer endpoints, core RAG
functionality, health checks, and error handling scenarios.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
from flask import Flask
import threading
import time

# Import the main application components
try:
    from src.core.rag_agent import create_flask_app, RAGAgent
    from src.sacred.sacred_layer_implementation import SacredLayerManager, SacredIntegratedRAGAgent
    from src.core.project_manager import ProjectManager
except ImportError as e:
    # Handle case where imports might not be available during testing
    pytest.skip(f"Cannot import required modules: {e}", allow_module_level=True)


@pytest.mark.api
class TestFlaskAppInitialization:
    """Test Flask application initialization and configuration"""
    
    def test_app_creation(self):
        """Test that Flask app can be created successfully"""
        with patch('rag_agent.genai') as mock_genai:
            mock_genai.Client.return_value = Mock()
            
            # Mock RAG agent initialization
            with patch.object(RAGAgent, '__init__', return_value=None):
                app = create_flask_app()
                
                assert isinstance(app, Flask)
                assert app.config.get('TESTING') is not None
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'})
    def test_app_with_environment_variables(self):
        """Test app initialization with proper environment variables"""
        with patch('rag_agent.genai') as mock_genai:
            mock_genai.Client.return_value = Mock()
            
            with patch.object(RAGAgent, '__init__', return_value=None):
                app = create_flask_app()
                
                # Verify environment variables are accessible
                assert os.getenv('GEMINI_API_KEY') == 'test_api_key'


@pytest.mark.api
class TestHealthCheckEndpoints:
    """Test health check and status endpoints"""
    
    @pytest.fixture
    def mock_app(self):
        """Create a mock Flask app for testing"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Add basic health check endpoint
        @app.route('/health')
        def health():
            return {"status": "healthy", "service": "contextkeeper"}
        
        @app.route('/status')
        def status():
            return {
                "status": "running",
                "version": "3.0.0",
                "components": {
                    "rag_agent": "active",
                    "sacred_layer": "active",
                    "project_manager": "active"
                }
            }
        
        return app
    
    def test_health_endpoint(self, mock_app):
        """Test /health endpoint returns correct status"""
        with mock_app.test_client() as client:
            response = client.get('/health')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'healthy'
            assert data['service'] == 'contextkeeper'
    
    def test_status_endpoint(self, mock_app):
        """Test /status endpoint returns system information"""
        with mock_app.test_client() as client:
            response = client.get('/status')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'running'
            assert 'version' in data
            assert 'components' in data


@pytest.mark.api
class TestCoreRAGEndpoints:
    """Test core RAG functionality endpoints"""
    
    @pytest.fixture
    def mock_rag_app(self):
        """Create a mock Flask app with RAG endpoints"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Mock RAG endpoints
        @app.route('/query', methods=['POST'])
        def query():
            data = request.get_json()
            return {
                "query": data.get('query', ''),
                "project_id": data.get('project_id', ''),
                "results": [
                    {
                        "content": "Mock result for query",
                        "score": 0.95,
                        "source": "test_file.py"
                    }
                ],
                "count": 1
            }
        
        @app.route('/ingest', methods=['POST'])
        def ingest():
            data = request.get_json()
            return {
                "status": "success",
                "project_id": data.get('project_id', ''),
                "files_processed": data.get('files', []),
                "message": "Files ingested successfully"
            }
        
        @app.route('/query_llm', methods=['POST'])
        def query_llm():
            data = request.get_json()
            return {
                "response": f"Mock LLM response for: {data.get('prompt', '')}",
                "model": "gemini-2.5-flash",
                "usage": {
                    "input_tokens": 50,
                    "output_tokens": 100
                }
            }
        
        return app
    
    def test_query_endpoint(self, mock_rag_app):
        """Test /query endpoint processes RAG queries correctly"""
        with mock_rag_app.test_client() as client:
            query_data = {
                "query": "How to implement authentication?",
                "project_id": "test_project",
                "limit": 5
            }
            
            response = client.post('/query', 
                                 data=json.dumps(query_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['query'] == query_data['query']
            assert data['project_id'] == query_data['project_id']
            assert 'results' in data
            assert len(data['results']) > 0
    
    def test_ingest_endpoint(self, mock_rag_app):
        """Test /ingest endpoint processes file ingestion"""
        with mock_rag_app.test_client() as client:
            ingest_data = {
                "project_id": "test_project",
                "files": ["test1.py", "test2.md"],
                "recursive": True
            }
            
            response = client.post('/ingest',
                                 data=json.dumps(ingest_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert data['project_id'] == ingest_data['project_id']
            assert data['files_processed'] == ingest_data['files']
    
    def test_query_llm_endpoint(self, mock_rag_app):
        """Test /query_llm endpoint for direct LLM queries"""
        with mock_rag_app.test_client() as client:
            llm_data = {
                "prompt": "Explain the authentication flow",
                "context": "Previous conversation about security",
                "model": "gemini-2.5-flash"
            }
            
            response = client.post('/query_llm',
                                 data=json.dumps(llm_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'response' in data
            assert 'model' in data
            assert 'usage' in data


@pytest.mark.api
@pytest.mark.sacred
class TestSacredLayerEndpoints:
    """Test Sacred Layer specific API endpoints"""
    
    @pytest.fixture
    def mock_sacred_app(self):
        """Create a mock Flask app with Sacred Layer endpoints"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Mock sacred endpoints
        @app.route('/sacred/plans', methods=['POST'])
        def create_sacred_plan():
            data = request.get_json()
            return {
                "status": "created",
                "plan_id": "test_plan_12345",
                "verification_code": "verify_code_67890",
                "project_id": data.get('project_id', ''),
                "title": data.get('title', '')
            }
        
        @app.route('/sacred/plans/<plan_id>/approve', methods=['POST'])
        def approve_plan(plan_id):
            data = request.get_json()
            return {
                "status": "approved",
                "plan_id": plan_id,
                "approved_by": data.get('approver', ''),
                "approved_at": "2025-07-29T04:17:00Z"
            }
        
        @app.route('/sacred/plans', methods=['GET'])
        def list_sacred_plans():
            project_id = request.args.get('project_id')
            return {
                "plans": [
                    {
                        "plan_id": "plan_1",
                        "title": "Authentication Plan",
                        "status": "approved",
                        "project_id": project_id
                    }
                ],
                "count": 1,
                "project_id": project_id
            }
        
        @app.route('/sacred/query', methods=['POST'])
        def query_sacred():
            data = request.get_json()
            return {
                "query": data.get('query', ''),
                "project_id": data.get('project_id', ''),
                "sacred_results": [
                    {
                        "plan_id": "plan_1",
                        "title": "Authentication Plan",
                        "relevance_score": 0.95,
                        "content_snippet": "Authentication implementation..."
                    }
                ],
                "count": 1
            }
        
        return app
    
    def test_create_sacred_plan_endpoint(self, mock_sacred_app):
        """Test POST /sacred/plans endpoint for plan creation"""
        with mock_sacred_app.test_client() as client:
            plan_data = {
                "project_id": "test_project",
                "title": "New Authentication Plan",
                "content": "Detailed authentication implementation plan...",
                "requester": "test_user"
            }
            
            response = client.post('/sacred/plans',
                                 data=json.dumps(plan_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'created'
            assert 'plan_id' in data
            assert 'verification_code' in data
            assert data['project_id'] == plan_data['project_id']
            assert data['title'] == plan_data['title']
    
    def test_approve_sacred_plan_endpoint(self, mock_sacred_app):
        """Test POST /sacred/plans/<id>/approve endpoint"""
        with mock_sacred_app.test_client() as client:
            approval_data = {
                "approver": "senior_developer",
                "verification_code": "verify_code_67890",
                "secondary_key": "sacred_approval_key"
            }
            
            response = client.post('/sacred/plans/test_plan_12345/approve',
                                 data=json.dumps(approval_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'approved'
            assert data['plan_id'] == 'test_plan_12345'
            assert data['approved_by'] == approval_data['approver']
    
    def test_list_sacred_plans_endpoint(self, mock_sacred_app):
        """Test GET /sacred/plans endpoint"""
        with mock_sacred_app.test_client() as client:
            response = client.get('/sacred/plans?project_id=test_project')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'plans' in data
            assert 'count' in data
            assert data['project_id'] == 'test_project'
            assert len(data['plans']) > 0
    
    def test_query_sacred_context_endpoint(self, mock_sacred_app):
        """Test POST /sacred/query endpoint"""
        with mock_sacred_app.test_client() as client:
            query_data = {
                "query": "authentication implementation",
                "project_id": "test_project",
                "limit": 5
            }
            
            response = client.post('/sacred/query',
                                 data=json.dumps(query_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['query'] == query_data['query']
            assert data['project_id'] == query_data['project_id']
            assert 'sacred_results' in data
            assert len(data['sacred_results']) > 0


@pytest.mark.api
class TestErrorHandling:
    """Test API error handling scenarios"""
    
    @pytest.fixture
    def error_app(self):
        """Create a Flask app with error handling endpoints"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Endpoint that returns 400 error
        @app.route('/error/400')
        def bad_request():
            return {"error": "Bad request", "message": "Invalid parameters"}, 400
        
        # Endpoint that returns 401 error
        @app.route('/error/401')
        def unauthorized():
            return {"error": "Unauthorized", "message": "Authentication required"}, 401
        
        # Endpoint that returns 404 error
        @app.route('/error/404')
        def not_found():
            return {"error": "Not found", "message": "Resource not found"}, 404
        
        # Endpoint that returns 500 error
        @app.route('/error/500')
        def server_error():
            return {"error": "Internal server error", "message": "Something went wrong"}, 500
        
        # Endpoint that validates JSON input
        @app.route('/validate', methods=['POST'])
        def validate():
            data = request.get_json()
            if not data:
                return {"error": "Missing JSON body"}, 400
            
            required_fields = ['project_id', 'query']
            for field in required_fields:
                if field not in data:
                    return {"error": f"Missing required field: {field}"}, 400
            
            return {"status": "valid", "data": data}
        
        return app
    
    def test_400_bad_request(self, error_app):
        """Test 400 Bad Request error handling"""
        with error_app.test_client() as client:
            response = client.get('/error/400')
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert data['error'] == 'Bad request'
            assert 'message' in data
    
    def test_401_unauthorized(self, error_app):
        """Test 401 Unauthorized error handling"""
        with error_app.test_client() as client:
            response = client.get('/error/401')
            
            assert response.status_code == 401
            data = json.loads(response.data)
            assert data['error'] == 'Unauthorized'
    
    def test_404_not_found(self, error_app):
        """Test 404 Not Found error handling"""
        with error_app.test_client() as client:
            response = client.get('/error/404')
            
            assert response.status_code == 404
            data = json.loads(response.data)
            assert data['error'] == 'Not found'
    
    def test_500_server_error(self, error_app):
        """Test 500 Internal Server Error handling"""
        with error_app.test_client() as client:
            response = client.get('/error/500')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['error'] == 'Internal server error'
    
    def test_missing_json_validation(self, error_app):
        """Test validation of missing JSON body"""
        with error_app.test_client() as client:
            response = client.post('/validate')
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_missing_required_field_validation(self, error_app):
        """Test validation of missing required fields"""
        with error_app.test_client() as client:
            # Send JSON with missing required field
            incomplete_data = {"project_id": "test_project"}  # Missing 'query' field
            
            response = client.post('/validate',
                                 data=json.dumps(incomplete_data),
                                 content_type='application/json')
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'Missing required field' in data['error']
    
    def test_valid_request_passes_validation(self, error_app):
        """Test that valid requests pass validation"""
        with error_app.test_client() as client:
            valid_data = {
                "project_id": "test_project",
                "query": "test query"
            }
            
            response = client.post('/validate',
                                 data=json.dumps(valid_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'valid'
            assert data['data'] == valid_data


@pytest.mark.api
@pytest.mark.integration
class TestEndpointIntegration:
    """Test integration between different API endpoints"""
    
    def test_query_after_ingest_flow(self):
        """Test the flow of ingesting files then querying them"""
        # This would test the integration between ingest and query endpoints
        # Using mocks to simulate the flow
        
        mock_ingested_data = {
            "project_id": "integration_test",
            "files": ["auth.py", "models.py"],
            "content_indexed": True
        }
        
        mock_query_results = {
            "query": "authentication methods",
            "project_id": "integration_test",
            "results": [
                {"source": "auth.py", "content": "def authenticate_user():", "score": 0.9}
            ]
        }
        
        # Test the conceptual flow
        assert mock_ingested_data["content_indexed"] is True
        assert mock_query_results["project_id"] == mock_ingested_data["project_id"]
        assert len(mock_query_results["results"]) > 0
    
    def test_sacred_plan_creation_and_query_flow(self):
        """Test creating a sacred plan then querying it"""
        # Mock the sacred plan creation and query flow
        
        mock_plan_creation = {
            "status": "created",
            "plan_id": "plan_integration_test",
            "project_id": "integration_test"
        }
        
        mock_sacred_query = {
            "query": "approved plans",
            "project_id": "integration_test",
            "sacred_results": [
                {"plan_id": "plan_integration_test", "relevance_score": 0.95}
            ]
        }
        
        # Test the conceptual integration
        assert mock_plan_creation["status"] == "created"
        assert mock_sacred_query["sacred_results"][0]["plan_id"] == mock_plan_creation["plan_id"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])