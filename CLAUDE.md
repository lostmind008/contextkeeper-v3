# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
- **`src/` layout**: The core Python logic is now cleanly organized in the `src/` directory.
- **WebSocket Layer**: The dashboard maintains a real-time connection to the backend via Socket.IO for instant UI updates.
- **Analytics Service**: A new `src/analytics` module provides on-demand governance metrics.

### Core Components
1. **RAG Agent** (`rag_agent.py`): Flask API server, handles all operations and WebSocket communication.
2. **Project Manager** (`src/core/project_manager.py`): Manages project state, decisions, and objectives.
3. **Sacred Layer** (`src/sacred/sacred_layer_implementation.py`): Enforces architectural governance.
4. **Analytics Service** (`src/analytics/analytics_service.py`): Calculates and serves project metrics.
5. **MCP Integration** (`mcp-server/enhanced_mcp_server.js`): Bridge for external AI tools.
6. **Dashboard** (`analytics_dashboard_live.html`): Real-time UI for all user interactions.

## Essential Commands & Workflows

### 1. Starting the System
```bash
# Start the backend server (API and WebSockets)
python src/rag_agent.py server
```

### 2. Onboarding a New Project (The *Only* Way)
The old, multi-step process is deprecated. Use this single command:
```bash
# This command creates the project AND indexes it, with a progress bar.
./scripts/contextkeeper.sh project add "/path/to/your/code" "Project Name"
```
There is no longer a separate `ingest` command for initial setup.

### 3. Daily Development
```bash
# Focus on a project (launches a fuzzy finder if no ID is given)
./scripts/contextkeeper.sh project focus

# Query the focused project
./scripts/contextkeeper.sh query "How does our auth work?"

# Run tests
pytest tests/ -v --tb=short
```

## Critical Implementation Details

### Asynchronous Operations & Real-Time Updates
- Project creation is now asynchronous. The `/projects/create-and-index` endpoint returns a `task_id`.
- The backend emits WebSocket events (`indexing_progress`, `indexing_complete`, etc.) to update clients in real-time. Do not implement polling logic; use WebSockets.

### Code Locations
- The main Flask application logic is in `rag_agent.py` in the root directory.
- Core business logic (ProjectManager, SacredLayerManager, AnalyticsService) is in the `src/` subdirectories. All new Python business logic should go into the appropriate `src/` module.

### Common Issues & Solutions
- **Issue**: "Project not found" after creation.
  - **Cause**: This should no longer happen due to the new onboarding workflow. If it does, it's a bug in the background task handling.
- **Issue**: Dashboard doesn't update when I use the CLI.
  - **Cause**: A backend action is likely missing a WebSocket event emission.
  - **Fix**: Ensure the relevant API endpoint in `rag_agent.py` calls `self.socketio.emit(...)` after performing its action. For example, `focus_project` emits a `focus_changed` event.

## Code Style
- Follow PEP 8 and use `black` and `flake8` (enforced by pre-commit hooks).
- Use Australian English spelling (e.g., "colour").

## Environment Variables
```bash
GOOGLE_API_KEY=        # Required for Gemini API
SACRED_APPROVAL_KEY=   # Required for approving Sacred Plans
MCP_CACHE_TTL_SECONDS=300 # Optional: Cache duration for the MCP server
```
