# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL: Orchestration-Only Mode Required
**IMPORTANT**: Before working on ANY task in this repository, you MUST first read the user's global memory file at `/Users/sumitm1/.claude/CLAUDE.md`. This file contains mandatory orchestration protocols that override all direct execution. You are an ORCHESTRATOR, not a direct executor - every task must be delegated to specialized sub-agents with comprehensive context and validation criteria.

## Project Overview
**ContextKeeper v3.0** - AI-powered development context management system with multi-project support, sacred architectural principles, and real-time analytics. Built as a hybrid Python/Node.js system with a Flask backend and MCP integration.

## Architecture Overview

### System Flow
```
User Request → Claude Code → MCP Server → RAG Agent → ChromaDB/LLM
                    ↓             ↓             ↓
                Dashboard   Sacred Layer   Project Manager
 (WebSocket for Real-Time)      |              |
                    ↓             ↓              ↓
                `src/` modules (core, sacred, analytics)
```

### Core Components
1. **RAG Agent** (`rag_agent.py`): Flask API server on port 5556, handles all operations and WebSocket communication
2. **Project Manager** (`src/core/project_manager.py`): Multi-project state management
3. **Sacred Layer** (`src/sacred/sacred_layer_implementation.py`): Enforces architectural governance
4. **Analytics Service** (`src/ck_analytics/analytics_service.py`): Calculates governance metrics
5. **MCP Integration** (`mcp-server/enhanced_mcp_server.js`): Bridge for Claude Code
6. **Dashboard** (`analytics_dashboard_live.html`): Real-time UI at http://localhost:5556/analytics_dashboard_live.html

## Essential Commands

### Development Setup
```bash
# Activate Python environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install MCP server dependencies
cd mcp-server && npm install && cd ..
```

### Starting the System
```bash
# Start the backend server (required for all operations)
python rag_agent.py server

# Start MCP server (for Claude Code integration)
cd mcp-server && npm start
```

### Project Management
```bash
# Create and index a new project (single command)
./scripts/contextkeeper.sh project add "/path/to/code" "Project Name"

# Focus on a project (interactive)
./scripts/contextkeeper.sh project focus

# Query the focused project
./scripts/contextkeeper.sh query "How does authentication work?"

# List all projects
./scripts/contextkeeper.sh project list
```

### Testing
```bash
# Run all tests with verbose output
pytest tests/ -v --tb=short

# Run specific test file
pytest tests/test_rag_agent.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run integration tests only
pytest tests/test_integration/ -v
```

### Code Quality
```bash
# Format code with black
black src/ tests/ rag_agent.py

# Check code style
flake8 src/ tests/ rag_agent.py

# Type checking (if configured)
mypy src/
```

## Project Structure & Key Files

### Main Orchestrator
- `rag_agent.py` (94KB, 2000+ lines) - Flask API server with ChromaDB, handles all RAG operations
  - Runs on port 5556
  - WebSocket support via Socket.IO
  - Manages ChromaDB collections per project

### Source Modules (`src/`)
- `core/` - Core components (project_manager.py for state management)
- `sacred/` - Sacred Layer governance (immutable architectural decisions)
- `ck_analytics/` - Analytics and metrics calculation
- `tracking/` - Git activity and event tracking
- `scripts/` - Utility scripts and one-time fixes
- `utils/` - Shared utilities (currently empty placeholder)

### Infrastructure
- `projects/` - JSON files storing project state
- `rag_knowledge_db/` - ChromaDB vector store
- `mcp-server/` - Node.js MCP server for Claude Code integration
- `test_sample_project/` - Test fixture (should be in .gitignore)

## Critical Implementation Details

### Asynchronous Operations
- Project creation is async - returns `task_id` immediately
- WebSocket events: `indexing_progress`, `indexing_complete`, `focus_changed`
- Never use polling - always use WebSocket events for real-time updates

### Project Isolation
- Each project gets its own ChromaDB collection (e.g., `proj_abc123`)
- Collections are created during indexing, not during project creation
- Sacred Layer decisions are project-specific

### Common Issues & Solutions

**Server won't start**
```bash
# Check if port 5556 is in use
lsof -i :5556
# Kill existing process if needed
kill -9 <PID>
```

**Project not found after creation**
- Ensure indexing completed (check WebSocket events)
- Verify collection exists in ChromaDB
- Check `projects/` directory for JSON file

**Dashboard not updating**
- Verify WebSocket connection in browser console
- Check `rag_agent.py` emits events after operations
- Ensure `socketio.emit()` calls are present

**Dependency issues**
```bash
# Use legacy peer deps for npm
cd mcp-server && npm install --legacy-peer-deps

# For Python conflicts
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## Environment Variables
```bash
# Required
GEMINI_API_KEY=<your-key>        # For LLM queries
SACRED_APPROVAL_KEY=<your-key>   # For Sacred Plan approval (no default)

# Optional
MCP_CACHE_TTL_SECONDS=300        # MCP server cache duration
FLASK_ENV=development            # Flask debug mode
```

## Code Style & Conventions
- PEP 8 enforced via pre-commit hooks
- Australian English spelling (colour, behaviour, realise)
- Comprehensive docstrings for files >100 lines
- Type hints for Python 3.8+
- Navigation comments in large files

## Untracked Files (Need Cleanup)
- `src/core/rag_agent.py` - Duplicate of main file
- `src/utils/` - Empty directory
- `test_sample_project/` - Test fixture
- `src/scripts/__init__.py` - Missing file

## Governance Files
- `PROJECT_MAP.md` - Current project structure and status
- `ARCHITECTURE.md` - Technical deep-dive
- `docs/USER_GUIDE.md` - End-user documentation
- `docs/api/API_REFERENCE.md` - API endpoint documentation

## Sacred Layer Rules
1. Project isolation is immutable
2. ChromaDB collections cannot be shared
3. Architectural decisions require approval key
4. All changes must maintain backward compatibility
5. Test coverage must remain above 80%