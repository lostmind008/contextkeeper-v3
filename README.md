# LostMind AI - ContextKeeper v3.0

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-16%2B-green.svg)](https://nodejs.org)

**ContextKeeper** is a revolutionary AI-powered development context management system by **LostMindAI**. It provides intelligent context tracking, architectural decision management, and AI-driven insights to maintain clarity and consistency across your development projects.

> **✅ CURRENT STATUS (August 2025)**: v3.0.0 - Production Ready! Beautiful Three.js dashboard, real-time analytics, multi-project support, and comprehensive API integration.

## 🌟 What's New in v3.0

ContextKeeper v3.0 introduces groundbreaking features that transform how you manage development context:

- **🎨 Beautiful Three.js Dashboard**: Interactive particle animation with modern dark theme and responsive design
- **📊 Real-time Analytics**: Live metrics, project health monitoring, and performance insights
- **🎯 Multi-Project Support**: Complete project isolation with zero cross-contamination
- **🤖 LLM Integration**: Natural language responses powered by Google Gemini 2.5 Flash
- **📝 Decision & Objective Tracking**: Record architectural decisions and track development objectives
- **🔍 Semantic Search**: Search entire codebase using natural language with context-aware results
- **🔐 Auto Security**: Automatically redacts API keys and sensitive data
- **⚡ Performance**: Async Flask endpoints, optimized embeddings, and intelligent caching
- **📱 Mobile Support**: Fully responsive design that works on all devices

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
python rag_agent.py server

# Verify it's working
curl http://localhost:5556/health
# Expected response: {"status":"healthy"}
```

### 4. Access the Beautiful Dashboard

Open your browser and navigate to:
```
http://localhost:5556/analytics_dashboard_live.html
```

Experience the stunning Three.js particle animation with:
- Interactive particle sphere with 4000 animated particles
- Mouse-responsive disintegration effects
- Modern dark theme with glass morphism
- Real-time project statistics
- Responsive design for all devices

### 5. Create Your First Project

```bash
# Create a new project with automatic file filtering
./scripts/rag_cli_v2.sh projects create "My Project" /path/to/project

# List all projects
./scripts/rag_cli_v2.sh projects list

# Ask questions with LLM-enhanced responses
./scripts/rag_cli_v2.sh ask "What is this project about?"
```

## ✨ Key Features

### 🎨 Beautiful User Interface
- **Three.js Background**: Interactive particle sphere with mouse interaction
- **Modern Design**: Tailwind CSS with dark theme and glass morphism
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Real-time Updates**: Live data refresh with smooth animations
- **Interactive Elements**: Hover effects, modals, and toast notifications

### 🎯 Intelligent Context Management
- **Multi-Project Support**: Isolated contexts for different projects with no cross-contamination
- **Smart File Filtering**: Automatically excludes venv, node_modules, build files, binaries, and non-relevant languages
- **LLM-Enhanced Queries**: Natural language responses instead of raw code chunks
- **Git Integration**: Track development activity through git commits and file changes
- **Path Intelligence**: Sophisticated filtering prevents database pollution

### 📊 Real-time Analytics
- **Live Metrics**: Active projects, focused project, total decisions, system health
- **Project Health**: Status monitoring with color-coded indicators
- **Performance Insights**: Load times, API response times, and system metrics
- **Export Options**: PDF, PNG, and JSON export functionality
- **Mobile Support**: Fully responsive analytics dashboard

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

# Analytics dashboard
GET http://localhost:5556/analytics_dashboard_live.html
# Returns: Beautiful Three.js dashboard
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
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              Beautiful Three.js Dashboard               │
│  • Interactive particle animation                      │
│  • Real-time analytics and metrics                     │
│  • Responsive design for all devices                   │
│  • Modern UI with glass morphism effects               │
└─────────────────────────────────────────────────────────┘
```

## 🎨 Dashboard Features

### Visual Design
- **4000 Particles**: Distributed in a Fibonacci sphere pattern
- **Mouse Interaction**: Particles respond to cursor with disintegration effects
- **Color Gradient**: Gold to white particles with smooth transitions
- **Smooth Rotation**: Continuous gentle rotation for dynamic feel

### UI Components
- **Glass Morphism**: Semi-transparent cards with backdrop blur effects
- **Color Coding**: Violet, pink, cyan, and green accent colors
- **Hover Effects**: Transform animations and shadow effects
- **Status Indicators**: Color-coded project status badges

### Interactive Features
- **Real-time Stats**: Live project metrics and system health
- **Project Management**: Create, view, and focus projects
- **Modal System**: Beautiful create project modal with form validation
- **Toast Notifications**: Real-time user feedback for actions
- **Auto-refresh**: Updates every 30 seconds with visual feedback

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

#### ✅ Server Not Starting
**Issue**: Server fails to start with segmentation fault  
**Solution**: Use server-only mode to bypass file watcher issues
```bash
# Use server-only mode (recommended)
python rag_agent.py server

# Instead of full start mode
# python rag_agent.py start  # May cause segmentation fault
```

#### ✅ Dashboard Not Loading
**Issue**: Dashboard shows blank page or 404 errors  
**Solution**: Ensure proper route configuration
```bash
# Verify dashboard is accessible
curl -I http://localhost:5556/analytics_dashboard_live.html

# Should return: HTTP/1.1 200 OK
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
python rag_agent.py server  # Will recreate with correct settings
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
│   ├── rag_cli_v2.sh            # Enhanced CLI (use this one)
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
├── analytics_dashboard_live.html # Beautiful Three.js dashboard
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
DEBUG=1 python rag_agent.py server

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
- **Beautiful Dashboard**: Three.js particle animation with modern UI design
- **Real-time Analytics**: Live metrics and performance monitoring
- **LLM Integration**: Natural language query responses using Google Gemini 2.5 Flash
- **Project Isolation**: Complete isolation with zero cross-contamination verified
- **Git Integration**: Comprehensive development activity tracking
- **MCP Tools**: 8 powerful tools for Claude Code integration
- **Sacred Metrics API**: Comprehensive analytics endpoint for governance metrics

### 🐛 Critical Fixes Applied
- **Server Stability**: Fixed segmentation fault issues with server-only mode
- **Dashboard Rendering**: Resolved blank page issues with proper route configuration
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
- Beautiful UI with [Three.js](https://threejs.org/) and [Tailwind CSS](https://tailwindcss.com/)
- Git integration using native Python git libraries

## 📚 Documentation

### Core Documentation
- **📖 User Guide**: [USER_GUIDE.md](USER_GUIDE.md) - Comprehensive user manual
- **🚀 Deployment Guide**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Production deployment steps
- **📊 Analytics Guide**: Access dashboard at `http://localhost:5556/analytics_dashboard_live.html`
- **🔧 API Reference**: [docs/api/API_REFERENCE.md](docs/api/API_REFERENCE.md) - Complete endpoint documentation

### Technical References
- **🏗️ Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design and components
- **🤖 MCP Tools**: 8 tools available in Claude Code (see MCP integration above)
- **📝 Test Report**: [TEST_REPORT_2025-07-31.md](TEST_REPORT_2025-07-31.md) - Comprehensive test analysis
- **🔍 Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and solutions

### Support
- **🐛 Issues**: [GitHub Issues](https://github.com/lostmind008/contextkeeper-v3/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/lostmind008/contextkeeper-v3/discussions)

---

**✨ Made with care by [LostMindAI](https://github.com/lostmind008) | Ready for production use with beautiful Three.js dashboard**