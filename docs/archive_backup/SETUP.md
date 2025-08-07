# ContextKeeper Setup Guide

## Prerequisites
- Python 3.8+
- Git  
- Google Cloud account (for GenAI API)

## ✅ System Status: Fully Operational
All infrastructure fixes completed - setup process tested and working.

## Installation

### 1. Automated Setup (Recommended)
```bash
# Clone repository
git clone [repository-url]
cd contextkeeper

# Run automated setup script
./setup.sh

# This will:
# - Create virtual environment
# - Install all dependencies
# - Set up directory structure
# - Create configuration templates
```

### 1b. Manual Setup (Alternative)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy template
cp .env.template .env

# Edit .env with your values
nano .env
```

Required environment variables:
```bash
# Google Cloud (REQUIRED - using latest models)
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global  
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Sacred Layer (OPTIONAL - for architecture protection) 
SACRED_APPROVAL_KEY=your-secret-approval-key
```

### 3. Google Cloud Setup
```bash
# Install Google Cloud CLI
# Follow: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud auth application-default login

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com
```

### 4. Directory Structure Setup
```bash
# Create required directories
mkdir -p ~/.rag_projects
mkdir -p rag_knowledge_db
mkdir -p rag_knowledge_db/sacred_plans
mkdir -p rag_knowledge_db/sacred_chromadb
```

## Verification

<<<<<<< HEAD
### Test Current Functionality (v3.0 Base)
=======
### Test Current Working Functionality
>>>>>>> v3-upgrade
```bash
# Activate environment
source venv/bin/activate

# Start agent (runs on port 5556)
python rag_agent.py start

<<<<<<< HEAD
# Test basic functionality
./scripts/rag_cli.sh projects list
./scripts/rag_cli.sh projects create "Test Project" /path/to/project

# Test LLM-enhanced queries (returns natural language responses)
./scripts/rag_cli.sh ask "What is this project about?"

# Get daily briefing
./scripts/rag_cli.sh briefing

# Check agent health
curl http://localhost:5556/health
=======
# Test currently working endpoints
curl http://localhost:5556/health      # Should return {"status":"healthy"}
curl http://localhost:5556/projects    # Should return projects data

# Note: Some endpoints may require database setup to function properly
>>>>>>> v3-upgrade
```

### Test v3.0 Upgrade (When Ready)
```bash
# Run upgrade script
./upgrade_to_v3_sacred.sh

# Test sacred layer
./scripts/rag_cli.sh sacred create test_project "Test Plan" 
```

## Troubleshooting

### Common Issues

**Google Cloud Authentication:**
```bash
# Check credentials
gcloud auth list
echo $GOOGLE_APPLICATION_CREDENTIALS

# Re-authenticate if needed
gcloud auth application-default login
```

**ChromaDB Issues:**
```bash
# Clear database if corrupted
rm -rf rag_knowledge_db
mkdir rag_knowledge_db
```

**Sacred Layer Issues:**
```bash
# Check sacred key is set
echo $SACRED_APPROVAL_KEY

# Verify sacred files exist
ls sacred_layer_implementation.py
ls tests/sacred/
```

### Debugging Commands
```bash
# Check agent logs
tail -f rag_agent.log

<<<<<<< HEAD
# Verify API health (v2.0 on 5556, v3.0 Sacred Layer on 5556)
=======
# Verify API health (ContextKeeper runs on port 5556)
>>>>>>> v3-upgrade
curl http://localhost:5556/health

# Test embeddings
python -c "from rag_agent import ProjectKnowledgeAgent; agent = ProjectKnowledgeAgent(); print('OK')"
```

## Development Setup

### IDE Configuration
- Recommended: VS Code with Python extension
- Configure linting: flake8, black
- Set Python interpreter to venv/bin/python

### Testing Setup
```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-asyncio

# Run tests
pytest tests/ -v
```

### Git Hooks (Optional)
```bash
# Pre-commit hook for tests
echo "pytest tests/" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```