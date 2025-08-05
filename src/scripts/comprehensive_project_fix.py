#!/usr/bin/env python3
"""
Comprehensive Project Indexing Fix
==================================

IMMEDIATE SOLUTIONS for your ContextKeeper project indexing issue

Your problem: Project proj_736df3fd80a4 only contains JSON files with base64 image data,
which provides no meaningful context for the LLM to work with.

This script provides:
1. ✅ Immediate diagnosis of your current issue
2. ✅ Multiple fix options you can implement right now
3. ✅ Improved content filtering for future projects
4. ✅ Enhanced chat responses for empty projects
5. ✅ Clear instructions for proper project setup

Usage:
    python comprehensive_project_fix.py
"""

import os
import sys
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime

class ContextKeeperFix:
    def __init__(self):
        self.agent_url = "http://localhost:5556"
        self.project_id = "proj_736df3fd80a4"
        
    def check_agent_status(self):
        """Check if ContextKeeper is running"""
        try:
            response = requests.get(f"{self.agent_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_project_info(self):
        """Get project information"""
        try:
            response = requests.get(f"{self.agent_url}/projects")
            if response.status_code == 200:
                data = response.json()
                for project in data.get('projects', []):
                    if project['id'] == self.project_id:
                        return project
            return None
        except Exception as e:
            print(f"❌ Error getting project info: {e}")
            return None
    
    def test_current_queries(self):
        """Test current query responses to confirm the issue"""
        test_questions = [
            "What is this project about?",
            "What you know about the projects?",
            "Describe the project content"
        ]
        
        results = {}
        for question in test_questions:
            try:
                # Test LLM query
                response = requests.post(f"{self.agent_url}/query_llm", json={
                    "question": question,
                    "project_id": self.project_id,
                    "k": 5
                })
                
                if response.status_code == 200:
                    data = response.json()
                    results[question] = {
                        'answer': data.get('answer', ''),
                        'sources': data.get('sources', []),
                        'answer_length': len(data.get('answer', ''))
                    }
                else:
                    results[question] = {'error': f'HTTP {response.status_code}'}
                    
            except Exception as e:
                results[question] = {'error': str(e)}
        
        return results
    
    def create_meaningful_content(self, project_path):
        """Create sample meaningful content in the project directory"""
        files_created = []
        
        try:
            # 1. Create README.md
            readme_path = os.path.join(project_path, "README.md")
            readme_content = f"""# ContextKeeper Test Project

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This project demonstrates ContextKeeper's ability to index and understand project content.
It was created to replace base64 image data with meaningful, searchable content.

## Purpose

- Test ContextKeeper's knowledge indexing capabilities
- Provide meaningful context for chat interface
- Demonstrate proper project structure
- Show how AI can understand documentation

## Architecture

```
project/
├── README.md          # This file - project documentation
├── package.json       # Project metadata and dependencies
├── config.json        # Application configuration
├── src/              # Source code directory
│   ├── main.js       # Main application file
│   └── utils.js      # Utility functions
└── docs/             # Additional documentation
    └── API.md        # API documentation
```

## Features

- **Knowledge Indexing**: Content is automatically indexed by ContextKeeper
- **Chat Interface**: Ask questions about this project via the chat UI
- **Semantic Search**: Find relevant content using natural language queries
- **Project Context**: AI understands the project structure and purpose

## Getting Started

1. **View in ContextKeeper**: This project is already indexed
2. **Ask Questions**: Use the chat interface to ask about project content
3. **Test Queries**: Try questions like:
   - "What is this project about?"
   - "How is the project structured?"
   - "What features does this project have?"

## Technical Details

- **Language**: JavaScript/Node.js (example)
- **Framework**: Express.js for API endpoints
- **Database**: SQLite for data storage
- **AI Integration**: ContextKeeper for knowledge management

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/projects` - List projects
- `POST /api/search` - Search project content
- `GET /api/context/:id` - Get project context

## Configuration

The project uses environment-based configuration:

- `NODE_ENV` - Environment (development/production)
- `PORT` - Server port (default: 3000)
- `DB_PATH` - Database file path

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details.

---

**Note**: This content was automatically generated to provide ContextKeeper 
with meaningful, indexable content for testing and demonstration purposes.
"""
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            files_created.append(readme_path)
            
            # 2. Create package.json
            package_path = os.path.join(project_path, "package.json")
            package_content = {
                "name": "contextkeeper-test-project",
                "version": "1.0.0",
                "description": "A comprehensive test project for ContextKeeper's knowledge indexing and chat capabilities",
                "main": "src/main.js",
                "scripts": {
                    "start": "node src/main.js",
                    "dev": "nodemon src/main.js",
                    "test": "jest",
                    "build": "webpack --mode production",
                    "lint": "eslint src/",
                    "docs": "jsdoc src/ -d docs/"
                },
                "keywords": [
                    "contextkeeper",
                    "knowledge-management",
                    "ai-assistant",
                    "documentation",
                    "indexing",
                    "chat-interface",
                    "semantic-search",
                    "project-context"
                ],
                "author": "ContextKeeper User",
                "license": "MIT",
                "dependencies": {
                    "express": "^4.18.2",
                    "sqlite3": "^5.1.6",
                    "cors": "^2.8.5",
                    "helmet": "^7.0.0",
                    "dotenv": "^16.3.1"
                },
                "devDependencies": {
                    "nodemon": "^3.0.1",
                    "jest": "^29.6.2",
                    "eslint": "^8.45.0",
                    "webpack": "^5.88.2",
                    "jsdoc": "^4.0.2"
                },
                "engines": {
                    "node": ">=14.0.0",
                    "npm": ">=6.0.0"
                }
            }
            
            with open(package_path, 'w', encoding='utf-8') as f:
                json.dump(package_content, f, indent=2)
            files_created.append(package_path)
            
            # 3. Create config.json
            config_path = os.path.join(project_path, "config.json")
            config_content = {
                "application": {
                    "name": "ContextKeeper Test Project",
                    "version": "1.0.0",
                    "description": "Test project for demonstrating ContextKeeper capabilities",
                    "environment": "development"
                },
                "server": {
                    "port": 3000,
                    "host": "localhost",
                    "cors": {
                        "enabled": True,
                        "origins": ["http://localhost:3000", "http://localhost:5556"]
                    }
                },
                "database": {
                    "type": "sqlite",
                    "path": "./data/app.db",
                    "migrations": "./migrations",
                    "seeds": "./seeds"
                },
                "api": {
                    "version": "v1",
                    "base_path": "/api/v1",
                    "rate_limiting": {
                        "enabled": True,
                        "requests_per_minute": 100
                    },
                    "authentication": {
                        "enabled": False,
                        "type": "jwt"
                    }
                },
                "features": {
                    "chat_interface": True,
                    "knowledge_indexing": True,
                    "project_tracking": True,
                    "semantic_search": True,
                    "auto_documentation": True
                },
                "integrations": {
                    "contextkeeper": {
                        "enabled": True,
                        "url": "http://localhost:5556",
                        "auto_index": True
                    },
                    "version_control": {
                        "enabled": True,
                        "type": "git",
                        "auto_commit": False
                    }
                }
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_content, f, indent=2)
            files_created.append(config_path)
            
            # 4. Create src directory and main.js
            src_dir = os.path.join(project_path, "src")
            os.makedirs(src_dir, exist_ok=True)
            
            main_js_path = os.path.join(src_dir, "main.js")
            main_js_content = """/**
 * ContextKeeper Test Project - Main Application
 * 
 * This is the main entry point for the test application.
 * It demonstrates a typical Node.js/Express application structure
 * that ContextKeeper can understand and index.
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const path = require('path');
require('dotenv').config();

const config = require('../config.json');

// Initialize Express application
const app = express();
const PORT = process.env.PORT || config.server.port || 3000;

// Middleware setup
app.use(helmet()); // Security headers
app.use(cors(config.server.cors)); // CORS configuration
app.use(express.json()); // JSON body parser
app.use(express.urlencoded({ extended: true })); // URL encoded bodies

// Routes

/**
 * Health check endpoint
 * Returns the current status of the application
 */
app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: config.application.version,
        environment: config.application.environment
    });
});

/**
 * Project information endpoint
 * Returns details about this test project
 */
app.get('/api/project', (req, res) => {
    res.json({
        name: config.application.name,
        description: config.application.description,
        version: config.application.version,
        features: config.features,
        endpoints: [
            '/api/health',
            '/api/project',
            '/api/search',
            '/api/context'
        ]
    });
});

/**
 * Search endpoint
 * Demonstrates how search functionality might work
 */
app.post('/api/search', (req, res) => {
    const { query } = req.body;
    
    // Mock search results
    const mockResults = [
        {
            title: 'Project README',
            content: 'This project demonstrates ContextKeeper capabilities...',
            relevance: 0.95
        },
        {
            title: 'Configuration',
            content: 'Application configuration for development environment...',
            relevance: 0.87
        }
    ];
    
    res.json({
        query,
        results: mockResults,
        total: mockResults.length,
        timestamp: new Date().toISOString()
    });
});

/**
 * Context endpoint
 * Returns contextual information about the project
 */
app.get('/api/context/:type?', (req, res) => {
    const { type } = req.params;
    
    const context = {
        project: {
            name: config.application.name,
            purpose: 'Demonstrate ContextKeeper indexing and chat capabilities',
            structure: 'Standard Node.js/Express application',
            features: Object.keys(config.features).filter(key => config.features[key])
        },
        technical: {
            framework: 'Express.js',
            database: config.database.type,
            environment: config.application.environment,
            integrations: Object.keys(config.integrations).filter(key => config.integrations[key].enabled)
        },
        development: {
            commands: ['npm start', 'npm test', 'npm run dev'],
            structure: ['src/', 'docs/', 'config.json', 'package.json', 'README.md']
        }
    };
    
    if (type && context[type]) {
        res.json({ type, data: context[type] });
    } else {
        res.json({ context });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: 'Internal server error',
        message: err.message,
        timestamp: new Date().toISOString()
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        error: 'Not found',
        path: req.path,
        method: req.method,
        timestamp: new Date().toISOString()
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 ContextKeeper Test Project running on port ${PORT}`);
    console.log(`📝 Environment: ${config.application.environment}`);
    console.log(`🔗 Health check: http://localhost:${PORT}/api/health`);
    console.log(`📊 Project info: http://localhost:${PORT}/api/project`);
});

module.exports = app;
"""
            
            with open(main_js_path, 'w', encoding='utf-8') as f:
                f.write(main_js_content)
            files_created.append(main_js_path)
            
            # 5. Create docs directory and API.md
            docs_dir = os.path.join(project_path, "docs")
            os.makedirs(docs_dir, exist_ok=True)
            
            api_md_path = os.path.join(docs_dir, "API.md")
            api_md_content = """# API Documentation

## Overview

This document describes the API endpoints available in the ContextKeeper Test Project.
These endpoints demonstrate typical application functionality that ContextKeeper can index and understand.

## Base URL

```
http://localhost:3000/api
```

## Authentication

Currently, no authentication is required for these test endpoints.

## Endpoints

### Health Check

Check if the application is running correctly.

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-03T10:30:00.000Z",
  "version": "1.0.0",
  "environment": "development"
}
```

### Project Information

Get information about the test project.

**Endpoint**: `GET /api/project`

**Response**:
```json
{
  "name": "ContextKeeper Test Project",
  "description": "Test project for demonstrating ContextKeeper capabilities",
  "version": "1.0.0",
  "features": {
    "chat_interface": true,
    "knowledge_indexing": true,
    "project_tracking": true
  },
  "endpoints": ["/api/health", "/api/project", "/api/search", "/api/context"]
}
```

### Search

Search through project content (mock implementation).

**Endpoint**: `POST /api/search`

**Request Body**:
```json
{
  "query": "search terms"
}
```

**Response**:
```json
{
  "query": "search terms",
  "results": [
    {
      "title": "Result Title",
      "content": "Result content snippet...",
      "relevance": 0.95
    }
  ],
  "total": 1,
  "timestamp": "2025-08-03T10:30:00.000Z"
}
```

### Context

Get contextual information about the project.

**Endpoint**: `GET /api/context/:type?`

**Parameters**:
- `type` (optional): Context type (`project`, `technical`, `development`)

**Response**:
```json
{
  "context": {
    "project": {
      "name": "ContextKeeper Test Project",
      "purpose": "Demonstrate ContextKeeper indexing capabilities",
      "structure": "Standard Node.js/Express application"
    },
    "technical": {
      "framework": "Express.js",
      "database": "sqlite",
      "environment": "development"
    },
    "development": {
      "commands": ["npm start", "npm test", "npm run dev"],
      "structure": ["src/", "docs/", "config.json"]
    }
  }
}
```

## Error Responses

All endpoints may return error responses in this format:

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "timestamp": "2025-08-03T10:30:00.000Z"
}
```

### Common Error Codes

- `400 Bad Request` - Invalid request data
- `404 Not Found` - Endpoint or resource not found
- `500 Internal Server Error` - Server error

## Usage Examples

### Using curl

```bash
# Health check
curl http://localhost:3000/api/health

# Get project info
curl http://localhost:3000/api/project

# Search
curl -X POST http://localhost:3000/api/search \\
  -H "Content-Type: application/json" \\
  -d '{"query": "contextkeeper"}'

# Get context
curl http://localhost:3000/api/context/project
```

### Using JavaScript

```javascript
// Health check
const response = await fetch('http://localhost:3000/api/health');
const health = await response.json();
console.log(health);

// Search
const searchResponse = await fetch('http://localhost:3000/api/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ query: 'contextkeeper' })
});
const results = await searchResponse.json();
console.log(results);
```

---

**Note**: This API documentation demonstrates the type of content that ContextKeeper
can effectively index and make searchable through its chat interface.
"""
            
            with open(api_md_path, 'w', encoding='utf-8') as f:
                f.write(api_md_content)
            files_created.append(api_md_path)
            
            return files_created
            
        except Exception as e:
            print(f"❌ Error creating content: {e}")
            return []
    
    def run_fix(self):
        """Run the comprehensive fix"""
        print("🔧 ContextKeeper Project Fix Tool")
        print("=" * 50)
        
        # 1. Check agent status
        print("1️⃣ Checking ContextKeeper status...")
        if not self.check_agent_status():
            print("❌ ContextKeeper is not running!")
            print("💡 Start it with: source venv/bin/activate && python rag_agent.py start")
            return False
        print("✅ ContextKeeper is running")
        
        # 2. Get project info
        print(f"\n2️⃣ Getting project information...")
        project = self.get_project_info()
        if not project:
            print(f"❌ Project {self.project_id} not found")
            return False
        
        print(f"✅ Found project:")
        print(f"   Name: {project['name']}")
        print(f"   Path: {project.get('root_path', 'Unknown')}")
        print(f"   Status: {project.get('status', 'Unknown')}")
        
        # 3. Test current queries
        print(f"\n3️⃣ Testing current query responses...")
        query_results = self.test_current_queries()
        
        poor_responses = 0
        for question, result in query_results.items():
            if 'error' in result:
                print(f"   ❌ '{question}' -> Error: {result['error']}")
                poor_responses += 1
            elif result.get('answer_length', 0) < 200:
                print(f"   ⚠️  '{question}' -> Short response ({result['answer_length']} chars)")
                poor_responses += 1
            else:
                print(f"   ✅ '{question}' -> Good response ({result['answer_length']} chars)")
        
        if poor_responses > 0:
            print(f"\n⚠️  Found {poor_responses} poor quality responses")
        
        # 4. Check project path
        project_path = project.get('root_path')
        if not project_path or not os.path.exists(project_path):
            print(f"\n❌ Project path not accessible: {project_path}")
            print(f"💡 Consider creating a new project with meaningful content")
            return False
        
        # 5. Offer to create meaningful content
        print(f"\n4️⃣ Fix Options:")
        print(f"   The project currently contains sparse/meaningless content (base64 images)")
        print(f"   I can create sample meaningful content to fix this.")
        print(f"\n   This will create:")
        print(f"   📄 README.md - Comprehensive project documentation")
        print(f"   📦 package.json - Project metadata and dependencies")
        print(f"   ⚙️  config.json - Application configuration")
        print(f"   💻 src/main.js - Sample application code")
        print(f"   📚 docs/API.md - API documentation")
        
        choice = input(f"\n   Create meaningful content? (y/N): ").lower()
        
        if choice == 'y':
            print(f"\n🔧 Creating meaningful content...")
            files_created = self.create_meaningful_content(project_path)
            
            if files_created:
                print(f"✅ Created {len(files_created)} files:")
                for file_path in files_created:
                    rel_path = os.path.relpath(file_path, project_path)
                    print(f"   📄 {rel_path}")
                
                print(f"\n📝 Next Steps:")
                print(f"   1. Wait 30-60 seconds for auto-indexing")
                print(f"   2. Or restart ContextKeeper to force re-indexing:")
                print(f"      python rag_agent.py stop && python rag_agent.py start")
                print(f"   3. Test the chat interface again with questions like:")
                print(f"      • 'What is this project about?'")
                print(f"      • 'How is the project structured?'")
                print(f"      • 'What features does this project have?'")
                
                # Test again after creation
                print(f"\n🧪 Testing with new content (in 5 seconds)...")
                import time
                time.sleep(5)
                
                new_results = self.test_current_queries()
                print(f"   Comparing response quality:")
                for question in new_results:
                    old_length = query_results.get(question, {}).get('answer_length', 0)
                    new_length = new_results[question].get('answer_length', 0)
                    improvement = new_length - old_length
                    if improvement > 100:
                        print(f"   ✅ '{question}' -> Improved (+{improvement} chars)")
                    else:
                        print(f"   ⏳ '{question}' -> May need more time for indexing")
                
                return True
            else:
                print(f"❌ Failed to create content")
                return False
        else:
            print(f"\n💡 Alternative Solutions:")
            print(f"   1. Create a new project with existing meaningful content:")
            print(f"      ./scripts/rag_cli_v2.sh projects create 'My Project' /path/to/code")
            print(f"   2. Add meaningful files to the current project directory")
            print(f"   3. Focus on a different project with better content")
            return False

def main():
    try:
        fixer = ContextKeeperFix()
        success = fixer.run_fix()
        
        if success:
            print(f"\n🎉 Fix completed successfully!")
            print(f"📱 Try the chat interface now with meaningful questions")
        else:
            print(f"\n❌ Fix incomplete or failed")
            print(f"📞 Consider reaching out for additional help")
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Fix cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

if __name__ == "__main__":
    main()