#!/usr/bin/env python3
"""
Advanced isolation test with specific data ingestion to ensure no cross-contamination
"""

import requests
import json
import time
import tempfile
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:5556"
TIMEOUT = 10

def create_project_with_unique_data(name: str, auth_method: str, unique_key: str):
    """Create a project with unique, identifiable data"""
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Create unique test files
        files = [
            {
                "name": "authentication.md",
                "content": f"""# {name} Authentication System

## Authentication Method
This project uses **{auth_method}** for authentication.

## Unique Identifier
Project Key: {unique_key}

## Security Details
- Authentication Type: {auth_method}
- Project ID Marker: {unique_key}
- Isolation Test: This content should ONLY appear in {name} queries
"""
            },
            {
                "name": "config.json",
                "content": json.dumps({
                    "project_name": name,
                    "auth_method": auth_method,
                    "unique_key": unique_key,
                    "isolation_test": f"ONLY_IN_{name.upper()}"
                }, indent=2)
            },
            {
                "name": "README.md", 
                "content": f"""# {name}

This is the {name} project.
Authentication: {auth_method}
Unique Key: {unique_key}
"""
            }
        ]
        
        # Write files
        for file_info in files:
            file_path = os.path.join(temp_dir, file_info["name"])
            with open(file_path, 'w') as f:
                f.write(file_info["content"])
        
        # Create project
        payload = {
            "name": name,
            "root_path": temp_dir,
            "description": f"Test project with {auth_method}"
        }
        
        response = requests.post(
            f"{BASE_URL}/projects",
            json=payload,
            timeout=TIMEOUT
        )
        
        if response.status_code != 200:
            logger.error(f"Failed to create project {name}: {response.text}")
            return None
            
        data = response.json()
        project_id = data['project_id']
        
        # Wait for project creation
        time.sleep(1)
        
        # Set this project as focused to ensure ingestion goes to the right place
        focus_response = requests.post(
            f"{BASE_URL}/projects/{project_id}/focus",
            timeout=TIMEOUT
        )
        
        if focus_response.status_code != 200:
            logger.warning(f"Could not focus project {name}, ingestion may fail")
        
        # Ingest all files
        for file_info in files:
            file_path = os.path.join(temp_dir, file_info["name"])
            ingest_payload = {
                "path": file_path,
                "project_id": project_id
            }
            
            ingest_response = requests.post(
                f"{BASE_URL}/ingest",
                json=ingest_payload,
                timeout=TIMEOUT
            )
            
            if ingest_response.status_code != 200:
                logger.error(f"Failed to ingest {file_info['name']} for {name}")
                logger.error(f"Response: {ingest_response.text}")
            else:
                logger.info(f"✅ Ingested {file_info['name']} for {name}")
        
        # Wait for indexing
        time.sleep(2)
        
        return {
            "id": project_id,
            "name": name,
            "auth_method": auth_method,
            "unique_key": unique_key,
            "temp_dir": temp_dir
        }
        
    except Exception as e:
        logger.error(f"Error creating project {name}: {e}")
        return None

def test_advanced_isolation():
    """Run advanced isolation tests"""
    logger.info("🚀 Starting Advanced Isolation Tests")
    logger.info("="*60)
    
    # Check service health
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code != 200:
            logger.error("❌ Service is not healthy")
            return False
    except:
        logger.error("❌ Cannot connect to service")
        return False
    
    # Create two test projects with distinct data
    logger.info("\n📁 Creating test projects with unique data...")
    
    project1 = create_project_with_unique_data(
        "IsolationTestAlpha",
        "OAuth2 with JWT tokens",
        "ALPHA-UNIQUE-12345"
    )
    
    project2 = create_project_with_unique_data(
        "IsolationTestBeta", 
        "API Keys with HMAC signing",
        "BETA-UNIQUE-67890"
    )
    
    if not project1 or not project2:
        logger.error("❌ Failed to create test projects")
        return False
    
    logger.info(f"\n✅ Created projects:")
    logger.info(f"   - {project1['name']} (ID: {project1['id']})")
    logger.info(f"   - {project2['name']} (ID: {project2['id']})")
    
    # Test 1: Query for OAuth2 in Alpha project
    logger.info("\n📋 Test 1: Query for OAuth2 in Alpha project")
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "question": "What authentication method is used?",
            "k": 10,
            "project_id": project1['id']
        },
        timeout=TIMEOUT
    )
    
    data1 = response.json()
    results1 = data1.get('results', [])
    
    # Debug logging
    logger.info(f"   Query response: {response.status_code}")
    logger.info(f"   Response keys: {list(data1.keys())}")
    logger.info(f"   Number of results: {len(results1)}")
    if results1:
        logger.info(f"   First result keys: {list(results1[0].keys())}")
        logger.info(f"   First result preview: {str(results1[0])[:200]}...")
    
    # Check results contain OAuth2 and ALPHA-UNIQUE
    oauth_found = False
    alpha_found = False
    beta_found = False
    
    for result in results1:
        text = result.get('content', '')  # Changed from 'text' to 'content'
        if 'OAuth2' in text:
            oauth_found = True
        if 'ALPHA-UNIQUE' in text:
            alpha_found = True
        if 'BETA-UNIQUE' in text or 'API Keys' in text:
            beta_found = True
    
    if oauth_found and alpha_found and not beta_found:
        logger.info("✅ Alpha project correctly returns OAuth2 and ALPHA-UNIQUE content")
        logger.info("✅ No Beta project content found in Alpha results")
    else:
        logger.error(f"❌ Alpha project results incorrect:")
        logger.error(f"   OAuth2 found: {oauth_found}")
        logger.error(f"   ALPHA-UNIQUE found: {alpha_found}")
        logger.error(f"   Beta content found: {beta_found}")
        return False
    
    # Test 2: Query for API Keys in Beta project
    logger.info("\n📋 Test 2: Query for API Keys in Beta project")
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "question": "What authentication method is used?",
            "k": 10,
            "project_id": project2['id']
        },
        timeout=TIMEOUT
    )
    
    data2 = response.json()
    results2 = data2.get('results', [])
    
    # Check results contain API Keys and BETA-UNIQUE
    api_keys_found = False
    beta_found = False
    alpha_found = False
    
    for result in results2:
        text = result.get('content', '')  # Changed from 'text' to 'content'
        if 'API Keys' in text:
            api_keys_found = True
        if 'BETA-UNIQUE' in text:
            beta_found = True
        if 'ALPHA-UNIQUE' in text or 'OAuth2' in text:
            alpha_found = True
    
    if api_keys_found and beta_found and not alpha_found:
        logger.info("✅ Beta project correctly returns API Keys and BETA-UNIQUE content")
        logger.info("✅ No Alpha project content found in Beta results")
    else:
        logger.error(f"❌ Beta project results incorrect:")
        logger.error(f"   API Keys found: {api_keys_found}")
        logger.error(f"   BETA-UNIQUE found: {beta_found}")
        logger.error(f"   Alpha content found: {alpha_found}")
        return False
    
    # Test 3: Query for unique keys
    logger.info("\n📋 Test 3: Query for unique project keys")
    
    # Query Alpha for its unique key
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "question": "ALPHA-UNIQUE-12345",
            "k": 5,
            "project_id": project1['id']
        },
        timeout=TIMEOUT
    )
    
    alpha_key_results = response.json().get('results', [])
    
    # Query Beta for Alpha's unique key (should find nothing)
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "question": "ALPHA-UNIQUE-12345",
            "k": 5,
            "project_id": project2['id']
        },
        timeout=TIMEOUT
    )
    
    beta_search_alpha = response.json().get('results', [])
    
    # Debug: Show what Beta found when searching for Alpha's key
    if beta_search_alpha:
        logger.warning(f"⚠️  Beta found {len(beta_search_alpha)} results for Alpha's key!")
        for i, result in enumerate(beta_search_alpha[:2]):
            logger.warning(f"   Result {i+1}: {result.get('content', '')[:100]}...")
            logger.warning(f"   Project ID in result: {result.get('project_id', 'N/A')}")
    
    if len(alpha_key_results) > 0 and len(beta_search_alpha) == 0:
        logger.info("✅ Alpha's unique key found only in Alpha project")
        logger.info(f"   Alpha results: {len(alpha_key_results)}")
        logger.info(f"   Beta results: {len(beta_search_alpha)}")
    else:
        logger.error("❌ Cross-contamination detected!")
        logger.error(f"   Alpha key in Alpha: {len(alpha_key_results)} results")
        logger.error(f"   Alpha key in Beta: {len(beta_search_alpha)} results")
        return False
    
    # Test 4: Verify result IDs are unique
    logger.info("\n📋 Test 4: Verify result IDs are completely unique")
    
    # Get all result IDs from both projects
    alpha_ids = set()
    beta_ids = set()
    
    # Query with broader search to get more results
    for query in ["authentication", "project", "config", "unique"]:
        # Alpha query
        response = requests.post(
            f"{BASE_URL}/query",
            json={"question": query, "k": 20, "project_id": project1['id']},
            timeout=TIMEOUT
        )
        for result in response.json().get('results', []):
            if result.get('id'):
                alpha_ids.add(result['id'])
        
        # Beta query
        response = requests.post(
            f"{BASE_URL}/query",
            json={"question": query, "k": 20, "project_id": project2['id']},
            timeout=TIMEOUT
        )
        for result in response.json().get('results', []):
            if result.get('id'):
                beta_ids.add(result['id'])
    
    # Check for overlap
    overlap = alpha_ids.intersection(beta_ids)
    
    if not overlap:
        logger.info("✅ No overlapping result IDs between projects")
        logger.info(f"   Alpha unique IDs: {len(alpha_ids)}")
        logger.info(f"   Beta unique IDs: {len(beta_ids)}")
    else:
        logger.error(f"❌ Found {len(overlap)} overlapping IDs!")
        logger.error(f"   Overlapping: {list(overlap)[:5]}")
        return False
    
    # Clean up
    logger.info("\n🧹 Cleaning up test data...")
    for project in [project1, project2]:
        if project and 'temp_dir' in project:
            try:
                import shutil
                shutil.rmtree(project['temp_dir'])
                logger.info(f"   Removed {project['temp_dir']}")
            except:
                pass
    
    logger.info("\n" + "="*60)
    logger.info("✅ ALL ADVANCED ISOLATION TESTS PASSED!")
    logger.info("="*60)
    logger.info("\nSummary:")
    logger.info("- Project-specific queries return only relevant content ✅")
    logger.info("- No cross-project data leakage detected ✅")
    logger.info("- Unique identifiers remain isolated ✅")
    logger.info("- Result IDs are completely unique per project ✅")
    
    return True

if __name__ == "__main__":
    success = test_advanced_isolation()
    exit(0 if success else 1)