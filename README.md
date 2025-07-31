# ContextKeeper v3.0 Sacred Layer

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-16%2B-green.svg)](https://nodejs.org)

**ContextKeeper** is a production-ready RAG-powered development context management system that prevents AI agents from derailing from approved architectural plans through the revolutionary **Sacred Layer** - an immutable plan storage system with 2-layer verification.

> **✅ CURRENT STATUS (August 2025)**: v3.0.0 - Production Ready! All critical fixes complete, LLM integration working, sacred layer tests passing, analytics dashboard live with real-time metrics.

## 🌟 What's New in v3.0

ContextKeeper v3.0 introduces groundbreaking features that ensure AI agents adhere to approved architectural plans:

- **🛡️ Sacred Layer**: Create immutable architectural plans with 2-layer verification that protects core architecture from unintended AI changes
- **🔄 Git-Based Tracking**: Robust file change tracking using Git for reliable knowledge base updates  
- **📊 Enhanced Drift Detection**: AI-powered drift analysis with automated recommendations and sacred plan alignment
- **🤖 Enhanced MCP Integration**: 8 MCP tools for seamless Claude Code integration with Sacred Layer awareness
- **📈 Live Analytics Dashboard**: Professional dashboard with real-time metrics, dark mode, export functionality, and mobile support
- **🎯 Complete Project Isolation**: Secure multi-project management with zero cross-contamination
- **💬 LLM-Enhanced Queries**: Natural language responses powered by Google Gemini 2.5 Flash
- **📝 Decision & Objective Tracking**: Record architectural decisions and track development objectives
- **🔍 Semantic Search**: Search entire codebase using natural language with context-aware results
- **🔐 Auto Security**: Automatically redacts API keys and sensitive data
- **📊 Sacred Metrics API**: Comprehensive analytics endpoint for sacred plan adherence and governance
- **⚡ Performance**: Async Flask endpoints, optimized embeddings, and intelligent caching

## 🚀 Quick Start (5 minutes)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/lostmind008/contextkeeper-v3.git
cd contextkeeper

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database (if needed)
python rag_agent.py init
```

### 2. Configure Environment

Create your `.env` file with Google Cloud credentials:

```bash
# Copy template and edit
cp .env.template .env

# Required: Google API Key (for embeddings and LLM)
export GOOGLE_API_KEY=your-google-api-key
export GEMINI_API_KEY=your-gemini-api-key  # Same as GOOGLE_API_KEY

# Required: Sacred Layer Approval Key
export SACRED_APPROVAL_KEY=your-secure-approval-key  # For 2-layer verification

# Optional: Analytics and Performance
export ANALYTICS_CACHE_DURATION=300  # Cache duration in seconds (default: 300)
export FLASK_ASYNC_MODE=True         # Enable async endpoints (default: True)
```

### 3. Start ContextKeeper

```bash
# Activate virtual environment
source venv/bin/activate

# Start the agent (runs on port 5556)
python rag_agent.py start

# Verify it's working
curl http://localhost:5556/health
# Expected response: {"status":"healthy"}
```

### 4. Create Your First Project

```bash
# Create a new project with automatic file filtering
./scripts/rag_cli_v2.sh projects create "My Project" /path/to/project

# List all projects
./scripts/rag_cli_v2.sh projects list

# Ask questions with LLM-enhanced responses
./scripts/rag_cli_v2.sh ask "What is this project about?"
```

## ✨ Key Features

### 🛡️ Sacred Layer Protection
- **Immutable Plans**: Architectural constraints that cannot be modified once approved
- **2-Layer Verification**: Hash-based codes + environment key security  
- **AI Guardrails**: Prevent AI agents from suggesting non-compliant changes
- **Drift Monitoring**: Real-time alignment checking with automated alerts

### 🎯 Intelligent Context Management
- **Multi-Project Support**: Isolated contexts for different projects with no cross-contamination
- **Smart File Filtering**: Automatically excludes venv, node_modules, build files, binaries, and non-relevant languages
- **LLM-Enhanced Queries**: Natural language responses instead of raw code chunks
- **Git Integration**: Track development activity through git commits and file changes
- **Path Intelligence**: Sophisticated filtering prevents database pollution

### 🔗 Claude Code Integration
- **8 MCP Tools**: Sacred-aware tools for seamless AI collaboration
- **Natural Language**: LLM-enhanced responses for technical queries  
- **Real-time Context**: Automatic architectural constraint provision
- **Session Awareness**: Maintains context across Claude sessions

## 🔧 Core Workflows

### Project Management (✅ Currently Working)

```bash
# List all projects
./scripts/rag_cli_v2.sh projects list

# Create a new project with automatic file filtering
./scripts/rag_cli_v2.sh projects create "My Project" /path/to/project

# Focus on a specific project
./scripts/rag_cli_v2.sh projects focus proj_123

# Ask questions with LLM-enhanced natural language responses
./scripts/rag_cli_v2.sh ask "What authentication system are we using?"

# Get daily briefing with project statistics
./scripts/rag_cli_v2.sh briefing

# Track decisions and objectives
./scripts/rag_cli_v2.sh decisions add "Using Redis for caching" "Performance reasons"
./scripts/rag_cli_v2.sh objectives add "Implement user auth" "High priority"
```

### Sacred Plan Management (✅ Currently Working)

```bash
# Create architectural plan
./scripts/rag_cli_v2.sh sacred create proj_123 "Database Architecture" plan.md

# Approve with 2-layer verification
./scripts/rag_cli_v2.sh sacred approve plan_abc123

# Check alignment with current codebase
./scripts/rag_cli_v2.sh sacred drift proj_123

# Query Sacred Layer directly
curl -X POST http://localhost:5556/sacred/query \
  -H "Content-Type: application/json" \
  -d '{"query": "database architecture plans"}'
```

### API Endpoints (✅ All Working)

```bash
# Health check
GET http://localhost:5556/health
# Response: {"status":"healthy"}

# List projects
GET http://localhost:5556/projects
# Returns: Array of project objects with metadata

# Query project context
POST http://localhost:5556/query
Content-Type: application/json
{
  "query": "authentication implementation",
  "project_id": "proj_123"
}

# Sacred Layer query
POST http://localhost:5556/sacred/query
Content-Type: application/json
{
  "query": "architectural constraints for database"
}
```

## 🏗️ Architecture

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Git Activity   │  │  Multi-Project  │  │  Sacred Layer   │
│  Tracker        │  │  RAG Agent      │  │  Manager        │
└─────────┬───────┘  └─────────┬───────┘  └─────────┬───────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│               ChromaDB Vector Storage                   │
│  • Project Collections (isolated)                      │
│  • Sacred Collections (immutable)                      │
│  • Decision & Objective Tracking                       │
│  • gemini-embedding-001 with v1beta API               │
│  • Smart path filtering (no venv/node_modules)        │
└─────────────────────────────────────────────────────────┘
```

## 🔗 Claude Code Integration

Add ContextKeeper to your Claude Code MCP configuration:

```json
{
  "contextkeeper-sacred": {
    "type": "stdio", 
    "command": "node",
    "args": ["/absolute/path/to/contextkeeper/mcp-server/enhanced_mcp_server.js"],
    "env": {"RAG_AGENT_URL": "http://localhost:5556"}
  }
}
```

**Available MCP Tools:**
- `get_development_context` - Comprehensive development context
- `intelligent_search` - Semantic code search
- `analyze_git_activity` - Git activity analysis  
- `check_development_drift` - Sacred plan alignment checking
- `manage_objectives` - Objective management
- `track_decision` - Decision recording
- `suggest_next_action` - AI-powered suggestions
- `get_code_context` - Relevant code examples

## 🛠️ Troubleshooting

### Common Issues & Solutions (All Fixed as of August 2025)

#### ✅ CLI Not Working / Merge Conflicts
**Issue**: CLI commands failing with merge conflict errors  
**Solution**: Fixed in rag_cli_v2.sh - all merge conflicts resolved
```bash
# Use the updated CLI script
./scripts/rag_cli_v2.sh projects list
```

#### ✅ Sacred Layer 500 Errors  
**Issue**: Sacred endpoints returning Internal Server Error  
**Solution**: Fixed ChromaDB filter formatting
```bash
# Before (broken): {"type": "sacred_plan", "status": "approved"}
# After (working): {"$and": [{"type": "sacred_plan"}, {"status": "approved"}]}
```

#### ✅ API Version Compatibility
**Issue**: Google GenAI API version errors  
**Solution**: Updated to v1beta API with gemini-embedding-001
```bash
# Updated configuration now uses:
# HttpOptions(api_version="v1beta") 
# Model: gemini-embedding-001
```

#### ✅ ChromaDB Embedding Function Conflicts
**Issue**: Database initialization failing with embedding conflicts  
**Solution**: Database reset and compatibility resolved
```bash
# If you encounter similar issues:
rm -rf rag_knowledge_db/chroma.sqlite3
python rag_agent.py start  # Will recreate with correct settings
```

#### ✅ Path Filtering Not Working
**Issue**: venv/node_modules files being indexed  
**Solution**: Confirmed working - smart filtering active
```bash
# Verify filtering with:
./scripts/rag_cli_v2.sh projects create test /path/to/project
# Check logs show filtered paths being excluded
```

### Getting Help

If you encounter issues:

1. **Check server status**: `curl http://localhost:5556/health` should return `{"status":"healthy"}`
2. **Verify environment**: Ensure `.env` file has correct Google Cloud credentials
3. **Check logs**: Server logs show detailed information about operations
4. **Reset database**: If corruption occurs, remove `rag_knowledge_db/` and restart
5. **CLI issues**: Always use `./scripts/rag_cli_v2.sh` (not the old rag_cli.sh)

## 📊 Project Structure

```
contextkeeper/
├── docs/                          # Comprehensive documentation
│   ├── api/                      # API reference docs
│   │   ├── API_REFERENCE.md      # Complete endpoint documentation
│   │   └── MCP_TOOLS_REFERENCE.md # Claude Code integration guide
│   ├── guides/                   # User and developer guides
│   │   ├── QUICK_REFERENCE.md    # Command quick reference
│   │   └── MIGRATION_GUIDE.md    # Upgrade instructions
│   ├── INSTALLATION.md           # Detailed setup instructions
│   ├── USAGE.md                  # Comprehensive usage guide
│   ├── ARCHITECTURE.md           # System design documentation
│   └── CONTRIBUTING.md           # Contribution guidelines
├── examples/                      # Usage examples and templates
│   ├── basic-usage.py           # Basic integration example
│   └── sacred-plan-templates/    # Sacred plan examples
├── mcp-server/                    # Claude Code integration
│   ├── enhanced_mcp_server.js   # Main MCP server
│   ├── package.json             # Node.js dependencies
│   └── README.md                # MCP-specific documentation
├── scripts/                       # CLI and automation scripts
│   ├── rag_cli_v2.sh            # Fixed CLI (use this one)
│   ├── sacred_cli_integration.sh # Sacred Layer CLI tools
│   └── setup.sh                 # Automated setup script
├── tests/                         # Comprehensive test suite
│   ├── api/                     # API endpoint tests
│   ├── sacred/                  # Sacred Layer tests
│   ├── integration/             # End-to-end tests
│   └── unit/                    # Unit tests
├── rag_agent.py                  # Main RAG orchestrator
├── sacred_layer_implementation.py # Sacred Layer core logic
├── git_activity_tracker.py       # Git integration
├── enhanced_drift_sacred.py      # Drift detection engine
├── project_manager.py            # Multi-project management
└── requirements.txt              # Python dependencies
```

## 🧪 Development & Testing  

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm  
- Git
- Google Cloud account with GenAI API enabled

### Running Tests

```bash
# Install test dependencies (included in setup.sh)
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test suites
pytest tests/sacred/ -v          # Sacred Layer tests
pytest tests/api/ -v             # API endpoint tests
pytest tests/integration/ -v     # End-to-end workflow tests

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Development Workflow

```bash
# Set up development environment
./setup.sh

# Start in development mode (with debug logging)
DEBUG=1 python rag_agent.py start

# Run integration tests
python test_comprehensive_fix.py

# Check Sacred Layer functionality
curl -X POST http://localhost:5556/sacred/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

## 📈 Use Cases

### AI-Assisted Development
- **Context Provision**: Provide architectural context to AI coding assistants
- **Constraint Enforcement**: Ensure AI suggestions align with approved designs
- **Knowledge Persistence**: Maintain context across development sessions

### Team Collaboration  
- **Shared Architecture**: Team-wide architectural constraints and guidelines
- **Decision Tracking**: Capture and preserve architectural decisions with rationale
- **Onboarding**: Quick context provision for new team members

### Compliance & Governance
- **Audit Trail**: Complete history of architectural changes and decisions
- **Drift Detection**: Monitor codebase alignment with approved designs
- **Change Management**: Controlled modification of architectural constraints

## 🔐 Security Features

- **🏠 Local-First**: All data stored locally, no external service dependencies (except Google GenAI for embeddings)
- **🔒 Immutable Plans**: Sacred plans cannot be modified once approved  
- **🛡️ 2-Layer Verification**: Hash-based codes + environment key prevent unauthorized changes
- **📋 Audit Trail**: Complete logging of all sacred operations and changes
- **🔍 Data Redaction**: Automatic detection and redaction of API keys and sensitive data
- **🚧 Path Security**: Smart filtering prevents access to sensitive system directories

## 🔄 v3.0.0 Release (August 2025)

### ✅ Major Features Completed
- **Sacred Layer**: Full implementation with 2-layer verification and immutable plans
- **Analytics Dashboard**: Live dashboard with real-time metrics, dark mode, and export functionality
- **LLM Integration**: Natural language query responses using Google Gemini 2.5 Flash
- **Project Isolation**: Complete isolation with zero cross-contamination verified
- **Git Integration**: Comprehensive development activity tracking
- **MCP Tools**: 8 powerful tools for Claude Code integration
- **Sacred Metrics API**: Comprehensive analytics endpoint for governance metrics

### 🐛 Critical Fixes Applied
- **Sacred Query Endpoint**: Fixed 500 errors with proper error handling
- **CLI JSON Parsing**: Resolved merge conflicts and added proper validation
- **LLM Client Integration**: Added missing client attribute to ProjectKnowledgeAgent
- **Test Suite Updates**: All sacred layer tests updated to match implementation
- **Vector Search**: Verified proper project isolation (false positive resolved)

### 🚀 Performance & Quality Improvements
- **Async Endpoints**: All Flask endpoints now use async for better performance
- **Smart Caching**: 5-minute caching for analytics endpoints
- **Error Recovery**: Exponential backoff and automatic retry logic
- **Mobile Support**: Fully responsive analytics dashboard
- **Export Options**: PDF, PNG, and JSON export functionality

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [ChromaDB](https://github.com/chroma-core/chroma) for vector storage
- Powered by [Google GenAI](https://ai.google.dev/) embedding models
- Integrated with [Claude Code](https://claude.ai/code) via MCP protocol
- Git integration using native Python git libraries

## 📚 Documentation

### Core Documentation
- **📖 User Guide**: [USER_GUIDE.md](USER_GUIDE.md) - Comprehensive user manual
- **🚀 Deployment Guide**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Production deployment steps
- **📊 Analytics Guide**: Access dashboard at `http://localhost:5556/analytics_dashboard_live.html`
- **🔧 API Reference**: [API_REFERENCE.md](API_REFERENCE.md) - Complete endpoint documentation

### Technical References
- **🏗️ Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - System design and components
- **🤖 MCP Tools**: 8 tools available in Claude Code (see MCP integration above)
- **📝 Test Report**: [TEST_REPORT_2025-07-31.md](TEST_REPORT_2025-07-31.md) - Comprehensive test analysis
- **🔍 Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

### Support
- **🐛 Issues**: [GitHub Issues](https://github.com/lostmind008/contextkeeper-v3/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/lostmind008/contextkeeper-v3/discussions)

---

**✨ Made with care by [LostMindAI](https://github.com/lostmind008) | Ready for production use with full Sacred Layer protection**