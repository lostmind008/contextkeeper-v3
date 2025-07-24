# ContextKeeper v3.0 Sacred Layer - Installation Guide

## Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm (for MCP server)
- **Git** (for activity tracking)
- **Google Cloud account** (for GenAI API)

## Quick Installation

### 1. Clone and Setup
```bash
# Clone repository
git clone https://github.com/lostmind008/contextkeeper.git
cd contextkeeper

# Run automated setup
./setup.sh
```

### 2. Configure Environment
```bash
# Copy template
cp .env.template .env

# Edit with your values
nano .env
```

Required environment variables:
```bash
# Google Cloud (for embeddings)
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Sacred Layer (v3.0)
SACRED_APPROVAL_KEY=your-secret-approval-key
```

### 3. Verify Installation
```bash
# Start Sacred Layer
python rag_agent.py start

# Test basic functionality
./scripts/rag_cli.sh projects list

# Test sacred layer
curl http://localhost:5556/sacred/health
```

## Google Cloud Setup

### 1. Create Project and Enable APIs
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

### 2. Create Service Account
```bash
# Create service account
gcloud iam service-accounts create contextkeeper-sa

# Download key file
gcloud iam service-accounts keys create contextkeeper-key.json \
    --iam-account contextkeeper-sa@your-project-id.iam.gserviceaccount.com

# Set in .env file
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/contextkeeper-key.json"
```

## Claude Code Integration

### 1. Configure MCP Server
Add to Claude Code MCP configuration:
```json
{
  "contextkeeper-sacred": {
    "type": "stdio",
    "command": "node",
    "args": ["/absolute/path/to/contextkeeper/mcp-server/enhanced_mcp_server.js"],
    "env": {
      "RAG_AGENT_URL": "http://localhost:5556"
    }
  }
}
```

### 2. Verify Integration
```bash
# Start Sacred Layer
python rag_agent.py start

# Test MCP tools in Claude Code
# Use: /mcp list_tools contextkeeper-sacred
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

**Sacred Layer Issues:**
```bash
# Check sacred key is set
echo $SACRED_APPROVAL_KEY

# Verify port availability
netstat -an | grep 5556
```

**MCP Integration Issues:**
```bash
# Check MCP server
node mcp-server/enhanced_mcp_server.js --help

# Verify RAG agent connectivity
curl http://localhost:5556/health
```

### Directory Structure Issues
```bash
# Create required directories
mkdir -p ~/.rag_projects
mkdir -p rag_knowledge_db/sacred_plans
mkdir -p rag_knowledge_db/sacred_chromadb

# Fix permissions
chmod +x rag_cli.sh
chmod +x setup.sh
```

### Performance Issues
```bash
# Clear database if corrupted
rm -rf rag_knowledge_db
mkdir rag_knowledge_db

# Check disk space
df -h

# Monitor memory usage
ps aux | grep python
```

## Next Steps

1. **Create Your First Project**: `./scripts/rag_cli.sh projects create "My Project" /path/to/project`
2. **Create Sacred Plan**: `./scripts/rag_cli.sh sacred create proj_123 "Architecture" plan.md`
3. **Start Development**: Use Claude Code with MCP integration for AI-aware development

For usage examples, see [USAGE.md](USAGE.md).
For API documentation, see [API_REFERENCE.md](../API_REFERENCE.md).