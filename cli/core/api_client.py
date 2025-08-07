#!/usr/bin/env python3
"""
File: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/core/api_client.py
Project: ContextKeeper v3
Purpose: Flask API integration with error handling and streaming
Dependencies: requests, urllib3
Dependents: All command modules
Created: 2025-08-06
Modified: 2025-08-06

PLANNING CONTEXT:
- RESTful client wrapper for Flask API
- Comprehensive error handling with retries
- Streaming support for progress tracking
- Response parsing and validation

TODO FROM PLANNING:
- [x] API client with all endpoints
- [x] Error handling and retries
- [x] Response parsing
- [x] Streaming support for indexing progress
- [ ] Add WebSocket support for real-time updates
"""

import json
import time
import logging
from typing import Dict, Any, Optional, List, Generator, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# === NAVIGATION ===
# Previous: [./context.py] - Gets configuration from here
# Next: [../commands/project.py] - Uses this for API calls
# Parent: [../cli.py] - Initialises API client

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Base exception for API errors"""
    def __init__(self, message: str, status_code: int = None, response_data: Dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class ProjectNotFoundError(APIError):
    """Project doesn't exist"""
    pass


class SacredViolationError(APIError):
    """Sacred layer violation detected"""
    pass


class IndexingError(APIError):
    """Error during file indexing"""
    pass


@dataclass
class APIResponse:
    """Standardised API response wrapper"""
    success: bool
    data: Any
    error: Optional[str] = None
    status_code: int = 200
    headers: Dict[str, str] = None
    
    def raise_for_status(self):
        """Raise exception if response indicates failure"""
        if not self.success:
            if self.status_code == 404:
                raise ProjectNotFoundError(self.error, self.status_code, self.data)
            elif 'sacred' in self.error.lower():
                raise SacredViolationError(self.error, self.status_code, self.data)
            else:
                raise APIError(self.error, self.status_code, self.data)


class ContextKeeperAPI:
    """
    Flask API client for ContextKeeper
    
    Handles:
    - All REST endpoints
    - Error handling and retries
    - Response parsing
    - Progress streaming
    - Authentication (if needed)
    """
    
    def __init__(self, base_url: str = "http://localhost:5556", 
                 timeout: int = 30, max_retries: int = 3,
                 verify_ssl: bool = False):
        """Initialise API client with retry strategy"""
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, 
                     data: Dict = None, params: Dict = None,
                     stream: bool = False) -> APIResponse:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout,
                verify=self.verify_ssl,
                stream=stream
            )
            
            # Handle streaming responses
            if stream:
                return response  # Return raw response for streaming
            
            # Parse JSON response
            try:
                response_data = response.json() if response.text else {}
            except json.JSONDecodeError:
                response_data = {'raw': response.text}
            
            # Check for errors
            if response.status_code >= 400:
                error_msg = response_data.get('error', f"HTTP {response.status_code}")
                return APIResponse(
                    success=False,
                    data=response_data,
                    error=error_msg,
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )
            
            return APIResponse(
                success=True,
                data=response_data,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
        except requests.exceptions.Timeout:
            return APIResponse(
                success=False,
                data={},
                error=f"Request timeout after {self.timeout}s",
                status_code=408
            )
        except requests.exceptions.ConnectionError:
            return APIResponse(
                success=False,
                data={},
                error=f"Cannot connect to {self.base_url}",
                status_code=503
            )
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return APIResponse(
                success=False,
                data={},
                error=str(e),
                status_code=500
            )
    
    # === Health & Status ===
    
    def health_check(self) -> bool:
        """Check if API is healthy"""
        response = self._make_request('GET', '/health')
        return response.success and response.data.get('status') == 'healthy'
    
    # === Project Management ===
    
    def list_projects(self) -> List[Dict]:
        """List all projects"""
        response = self._make_request('GET', '/projects')
        response.raise_for_status()
        return response.data.get('projects', [])
    
    def create_project(self, name: str, path: str, description: str = None) -> Dict:
        """Create new project"""
        data = {
            'name': name,
            'path': path,
            'description': description or f"Project at {path}"
        }
        response = self._make_request('POST', '/projects', data=data)
        response.raise_for_status()
        return response.data
    
    def focus_project(self, project_id: str) -> Dict:
        """Focus on a specific project"""
        response = self._make_request('POST', f'/projects/{project_id}/focus')
        response.raise_for_status()
        return response.data
    
    def get_project_status(self, project_id: str) -> Dict:
        """Get project status and metadata"""
        response = self._make_request('GET', f'/projects/validate/{project_id}')
        response.raise_for_status()
        return response.data
    
    def update_project_status(self, project_id: str, status: str) -> Dict:
        """Update project status"""
        data = {'status': status}
        response = self._make_request('PUT', f'/projects/{project_id}/status', data=data)
        response.raise_for_status()
        return response.data
    
    # === Indexing & Ingestion ===
    
    def index_project(self, project_id: str, path: str, 
                      file_types: List[str] = None,
                      exclude_dirs: List[str] = None,
                      stream_progress: bool = True) -> Generator[Dict, None, None]:
        """
        Index project files with streaming progress
        
        Yields progress updates if stream_progress=True
        """
        data = {
            'project_id': project_id,
            'path': path,
            'file_types': file_types or ['.py', '.js', '.ts', '.md', '.txt'],
            'exclude_dirs': exclude_dirs or ['node_modules', '__pycache__', '.git', 'venv']
        }
        
        if stream_progress:
            # Use streaming endpoint for progress updates
            response = self._make_request('POST', '/ingest', data=data, stream=True)
            
            if isinstance(response, requests.Response):
                for line in response.iter_lines():
                    if line:
                        try:
                            progress = json.loads(line.decode('utf-8'))
                            yield progress
                        except json.JSONDecodeError:
                            continue
            else:
                yield response.data
        else:
            # Regular blocking request
            response = self._make_request('POST', '/ingest', data=data)
            response.raise_for_status()
            yield response.data
    
    # === Query & Context ===
    
    def query(self, question: str, project_id: str = None, 
              context_size: int = 5) -> Dict:
        """Query the knowledge base"""
        data = {
            'question': question,
            'project_id': project_id,
            'k': context_size
        }
        response = self._make_request('POST', '/query', data=data)
        response.raise_for_status()
        return response.data
    
    def get_context(self, project_id: str, limit: int = 10) -> Dict:
        """Get project context and recent activity"""
        params = {'limit': limit}
        response = self._make_request('GET', f'/projects/{project_id}/context', params=params)
        response.raise_for_status()
        return response.data
    
    # === Sacred Layer ===
    
    def create_sacred_plan(self, project_id: str, title: str, 
                           description: str, rationale: str) -> Dict:
        """Create new sacred architectural plan"""
        data = {
            'project_id': project_id,
            'title': title,
            'description': description,
            'rationale': rationale
        }
        response = self._make_request('POST', '/sacred/plans', data=data)
        response.raise_for_status()
        return response.data
    
    def list_sacred_plans(self, project_id: str = None, 
                         status: str = None) -> List[Dict]:
        """List sacred plans with optional filters"""
        params = {}
        if project_id:
            params['project_id'] = project_id
        if status:
            params['status'] = status
        
        response = self._make_request('GET', '/sacred/plans', params=params)
        response.raise_for_status()
        return response.data.get('plans', [])
    
    def approve_sacred_plan(self, plan_id: str, approval_key: str, 
                           tier: int = 1) -> Dict:
        """Approve sacred plan (requires key)"""
        data = {
            'approval_key': approval_key,
            'tier': tier
        }
        response = self._make_request('POST', f'/sacred/plans/{plan_id}/approve', data=data)
        response.raise_for_status()
        return response.data
    
    def check_sacred_drift(self, project_id: str, hours: int = 24) -> Dict:
        """Check for sacred drift violations"""
        params = {'hours': hours}
        response = self._make_request('GET', f'/projects/{project_id}/sacred-drift', params=params)
        response.raise_for_status()
        return response.data
    
    def query_sacred(self, project_id: str, query: str) -> Dict:
        """Query sacred architectural decisions"""
        data = {
            'project_id': project_id,
            'query': query
        }
        response = self._make_request('POST', '/sacred/query', data=data)
        response.raise_for_status()
        return response.data
    
    # === Decision & Event Tracking ===
    
    def record_decision(self, project_id: str, title: str, 
                       description: str, rationale: str,
                       alternatives: List[str] = None) -> Dict:
        """Record architectural decision"""
        data = {
            'project_id': project_id,
            'title': title,
            'description': description,
            'rationale': rationale,
            'alternatives': alternatives or []
        }
        response = self._make_request('POST', '/decision', data=data)
        response.raise_for_status()
        return response.data
    
    def record_event(self, project_id: str, event_type: str, 
                    description: str, metadata: Dict = None) -> Dict:
        """Record project event"""
        data = {
            'project_id': project_id,
            'event_type': event_type,
            'description': description,
            'metadata': metadata or {}
        }
        response = self._make_request('POST', '/events', data=data)
        response.raise_for_status()
        return response.data
    
    def get_events(self, project_id: str, event_type: str = None, 
                  limit: int = 50) -> List[Dict]:
        """Get project events"""
        params = {
            'project_id': project_id,
            'limit': limit
        }
        if event_type:
            params['event_type'] = event_type
        
        response = self._make_request('GET', '/events', params=params)
        response.raise_for_status()
        return response.data.get('events', [])
    
    # === Objectives Management ===
    
    def add_objective(self, project_id: str, title: str, 
                     description: str, success_criteria: List[str]) -> Dict:
        """Add project objective"""
        data = {
            'title': title,
            'description': description,
            'success_criteria': success_criteria
        }
        response = self._make_request('POST', f'/projects/{project_id}/objectives', data=data)
        response.raise_for_status()
        return response.data
    
    def complete_objective(self, project_id: str, objective_id: str) -> Dict:
        """Mark objective as complete"""
        response = self._make_request('POST', 
                                     f'/projects/{project_id}/objectives/{objective_id}/complete')
        response.raise_for_status()
        return response.data
    
    # === Git Integration ===
    
    def get_git_activity(self, project_id: str, days: int = 7) -> Dict:
        """Get Git activity for project"""
        params = {'days': days}
        response = self._make_request('GET', f'/projects/{project_id}/git/activity', params=params)
        response.raise_for_status()
        return response.data
    
    # === Utility Methods ===
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test connection to API"""
        try:
            if self.health_check():
                return True, f"Connected to {self.base_url}"
            else:
                return False, "API unhealthy"
        except Exception as e:
            return False, str(e)
    
    def get_stats(self) -> Dict:
        """Get overall system statistics"""
        stats = {
            'projects': len(self.list_projects()),
            'api_url': self.base_url,
            'healthy': self.health_check()
        }
        return stats