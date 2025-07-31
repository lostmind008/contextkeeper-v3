#!/usr/bin/env python3
"""
Comprehensive test for project isolation in ContextKeeper
Tests to ensure complete project isolation with no cross-project data leakage
"""

import asyncio
import json
import logging
import requests
import sys
import time
from typing import Dict, List
import tempfile
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:5556"
TIMEOUT = 10

class IsolationTester:
    """Test suite for project isolation verification"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.test_results = []
        
    def check_service_health(self):
        """Verify the service is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=TIMEOUT)
            if response.status_code == 200:
                logger.info("✅ Service is healthy")
                return True
            else:
                logger.error(f"❌ Service health check failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Cannot connect to service: {e}")
            return False
    
    def test_query_without_project_id(self):
        """Test 1: Query without project_id should fail with proper error"""
        logger.info("\n📋 Test 1: Query without project_id")
        
        try:
            # Send query without project_id
            payload = {
                "question": "What is the authentication method?",
                "k": 5
            }
            
            response = requests.post(
                f"{self.base_url}/query",
                json=payload,
                timeout=TIMEOUT
            )
            
            data = response.json()
            
            # Should return error about no project context
            if response.status_code == 200 and 'error' in data:
                if 'No project context' in data['error']:
                    logger.info("✅ Correctly rejected query without project_id")
                    logger.info(f"   Error message: {data['error']}")
                    self.test_results.append(("Query without project_id", True, "Properly rejected"))
                    return True
                else:
                    logger.error(f"❌ Unexpected error message: {data['error']}")
                    self.test_results.append(("Query without project_id", False, f"Wrong error: {data['error']}"))
                    return False
            else:
                logger.error(f"❌ Query should have failed but got: {data}")
                self.test_results.append(("Query without project_id", False, "Should have returned error"))
                return False
                
        except Exception as e:
            logger.error(f"❌ Test failed with exception: {e}")
            self.test_results.append(("Query without project_id", False, str(e)))
            return False
    
    def test_query_with_invalid_project_id(self):
        """Test 2: Query with invalid project_id should fail with proper error"""
        logger.info("\n📋 Test 2: Query with invalid project_id")
        
        try:
            # Send query with non-existent project_id
            payload = {
                "question": "What is the authentication method?",
                "k": 5,
                "project_id": "non_existent_project_123"
            }
            
            response = requests.post(
                f"{self.base_url}/query",
                json=payload,
                timeout=TIMEOUT
            )
            
            data = response.json()
            
            # Should return error about project not found
            if response.status_code == 200 and 'error' in data:
                if 'not found' in data['error'] or 'non-existent' in data['error']:
                    logger.info("✅ Correctly rejected query with invalid project_id")
                    logger.info(f"   Error message: {data['error']}")
                    self.test_results.append(("Query with invalid project_id", True, "Properly rejected"))
                    return True
                else:
                    logger.error(f"❌ Unexpected error message: {data['error']}")
                    self.test_results.append(("Query with invalid project_id", False, f"Wrong error: {data['error']}"))
                    return False
            else:
                logger.error(f"❌ Query should have failed but got: {data}")
                self.test_results.append(("Query with invalid project_id", False, "Should have returned error"))
                return False
                
        except Exception as e:
            logger.error(f"❌ Test failed with exception: {e}")
            self.test_results.append(("Query with invalid project_id", False, str(e)))
            return False
    
    def get_existing_projects(self) -> List[Dict]:
        """Get list of existing projects"""
        try:
            response = requests.get(f"{self.base_url}/projects", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                return data.get('projects', [])
            else:
                logger.error(f"Failed to get projects: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error getting projects: {e}")
            return []
    
    def test_query_with_valid_project_id(self):
        """Test 3: Query with valid project_id should work"""
        logger.info("\n📋 Test 3: Query with valid project_id")
        
        # Get existing projects
        projects = self.get_existing_projects()
        if not projects:
            logger.warning("⚠️  No projects found - creating a test project")
            # Create a test project if none exist
            test_project = self.create_test_project()
            if test_project:
                projects = [test_project]
            else:
                logger.error("❌ Could not create test project")
                self.test_results.append(("Query with valid project_id", False, "No projects available"))
                return False
        
        # Use the first project
        project_id = projects[0]['id']
        project_name = projects[0]['name']
        logger.info(f"   Using project: {project_name} (ID: {project_id})")
        
        try:
            # Send query with valid project_id
            payload = {
                "question": "What are the main components of this project?",
                "k": 5,
                "project_id": project_id
            }
            
            response = requests.post(
                f"{self.base_url}/query",
                json=payload,
                timeout=TIMEOUT
            )
            
            data = response.json()
            
            # Should succeed and return results
            if response.status_code == 200 and 'error' not in data:
                logger.info("✅ Query with valid project_id succeeded")
                logger.info(f"   Query: {data.get('query', '')[:50]}...")
                logger.info(f"   Results count: {len(data.get('results', []))}")
                if data.get('results'):
                    logger.info(f"   First result: {data['results'][0].get('text', '')[:100]}...")
                self.test_results.append(("Query with valid project_id", True, "Query succeeded"))
                return True
            else:
                logger.error(f"❌ Query failed: {data}")
                self.test_results.append(("Query with valid project_id", False, f"Query failed: {data.get('error', 'Unknown error')}"))
                return False
                
        except Exception as e:
            logger.error(f"❌ Test failed with exception: {e}")
            self.test_results.append(("Query with valid project_id", False, str(e)))
            return False
    
    def create_test_project(self) -> Dict:
        """Create a test project for testing"""
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            
            payload = {
                "name": "IsolationTestProject",
                "root_path": temp_dir,
                "description": "Test project for isolation testing"
            }
            
            response = requests.post(
                f"{self.base_url}/projects",
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "id": data['project_id'],  # Keep as 'id' to match API response
                    "name": payload['name']
                }
            else:
                logger.error(f"Failed to create test project: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating test project: {e}")
            return None
    
    def test_cross_project_contamination(self):
        """Test 4: Ensure no cross-project data leakage"""
        logger.info("\n📋 Test 4: Cross-project contamination prevention")
        
        # Get existing projects
        projects = self.get_existing_projects()
        if len(projects) < 2:
            logger.info("   Need at least 2 projects for contamination test - creating test projects")
            
            # Create two test projects
            project1 = self.create_test_project_with_data("TestProject1", "Authentication uses OAuth2")
            project2 = self.create_test_project_with_data("TestProject2", "Authentication uses API keys")
            
            if not project1 or not project2:
                logger.error("❌ Could not create test projects")
                self.test_results.append(("Cross-project contamination", False, "Could not create test projects"))
                return False
                
            projects = [project1, project2]
        else:
            # Use existing projects
            project1 = projects[0]
            project2 = projects[1]
        
        logger.info(f"   Testing isolation between: {project1['name']} and {project2['name']}")
        
        try:
            # Query project1 for specific content
            payload1 = {
                "question": "What authentication method is used?",
                "k": 10,
                "project_id": project1['id']
            }
            
            response1 = requests.post(
                f"{self.base_url}/query",
                json=payload1,
                timeout=TIMEOUT
            )
            
            data1 = response1.json()
            
            # Query project2 for the same content
            payload2 = {
                "question": "What authentication method is used?",
                "k": 10,
                "project_id": project2['id']
            }
            
            response2 = requests.post(
                f"{self.base_url}/query",
                json=payload2,
                timeout=TIMEOUT
            )
            
            data2 = response2.json()
            
            # Check that results are different and project-specific
            if response1.status_code == 200 and response2.status_code == 200:
                results1 = data1.get('results', [])
                results2 = data2.get('results', [])
                
                # Extract result IDs/texts to compare
                ids1 = set([r.get('id', '') for r in results1 if r.get('id')])
                ids2 = set([r.get('id', '') for r in results2 if r.get('id')])
                
                # Check for overlap
                overlap = ids1.intersection(ids2)
                
                if overlap:
                    logger.error(f"❌ Found {len(overlap)} overlapping results between projects!")
                    logger.error(f"   Overlapping IDs: {list(overlap)[:5]}...")
                    self.test_results.append(("Cross-project contamination", False, f"{len(overlap)} overlapping results"))
                    return False
                else:
                    logger.info("✅ No cross-project contamination detected")
                    logger.info(f"   Project 1 results: {len(results1)}")
                    logger.info(f"   Project 2 results: {len(results2)}")
                    logger.info(f"   No overlapping result IDs")
                    self.test_results.append(("Cross-project contamination", True, "No contamination detected"))
                    return True
            else:
                logger.error("❌ One or both queries failed")
                self.test_results.append(("Cross-project contamination", False, "Query execution failed"))
                return False
                
        except Exception as e:
            logger.error(f"❌ Test failed with exception: {e}")
            self.test_results.append(("Cross-project contamination", False, str(e)))
            return False
    
    def create_test_project_with_data(self, name: str, content: str) -> Dict:
        """Create a test project with specific content"""
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            
            # Create a test file with specific content
            test_file = os.path.join(temp_dir, "test_content.md")
            with open(test_file, 'w') as f:
                f.write(f"# {name} Documentation\n\n")
                f.write(f"{content}\n")
                f.write(f"This content belongs exclusively to {name}.\n")
            
            # Create project
            payload = {
                "name": name,
                "root_path": temp_dir,
                "description": f"Test project: {name}"
            }
            
            response = requests.post(
                f"{self.base_url}/projects",
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                project_id = data['project_id']
                
                # Wait a moment for project creation
                time.sleep(1)
                
                # Ingest the test file
                ingest_payload = {
                    "path": test_file,
                    "project_id": project_id
                }
                
                ingest_response = requests.post(
                    f"{self.base_url}/ingest",
                    json=ingest_payload,
                    timeout=TIMEOUT
                )
                
                if ingest_response.status_code == 200:
                    logger.info(f"   Created and ingested data for {name}")
                    return {
                        "id": project_id,  # Keep as 'id' to match API response
                        "name": name,
                        "content": content
                    }
                else:
                    logger.error(f"Failed to ingest data for {name}: {ingest_response.text}")
                    return None
            else:
                logger.error(f"Failed to create project {name}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating project {name}: {e}")
            return None
    
    def print_summary(self):
        """Print test summary"""
        logger.info("\n" + "="*60)
        logger.info("🏁 TEST SUMMARY")
        logger.info("="*60)
        
        passed = sum(1 for _, result, _ in self.test_results if result)
        total = len(self.test_results)
        
        for test_name, result, message in self.test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{status} | {test_name}: {message}")
        
        logger.info("-"*60)
        logger.info(f"Total: {passed}/{total} tests passed")
        
        if passed == total:
            logger.info("\n🎉 All isolation tests passed! Project isolation is working correctly.")
            return True
        else:
            logger.info(f"\n⚠️  {total - passed} test(s) failed. Project isolation needs attention.")
            return False
    
    def run_all_tests(self):
        """Run all isolation tests"""
        logger.info("🚀 Starting ContextKeeper Project Isolation Tests")
        logger.info("="*60)
        
        # Check service health first
        if not self.check_service_health():
            logger.error("\n❌ Service is not running. Please start ContextKeeper first:")
            logger.error("   python rag_agent.py start")
            return False
        
        # Run all tests
        self.test_query_without_project_id()
        self.test_query_with_invalid_project_id()
        self.test_query_with_valid_project_id()
        self.test_cross_project_contamination()
        
        # Print summary
        return self.print_summary()


def main():
    """Main entry point"""
    tester = IsolationTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()