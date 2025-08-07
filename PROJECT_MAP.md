# Project: ContextKeeper v3.0
Generated: 2025-08-06
Last Updated: 2025-08-06

## 🎯 Project Overview
ContextKeeper v3.0 is an AI-powered development context management system with multi-project support, sacred architectural principles, and real-time analytics. Built as a hybrid Python/Node.js system with a Flask backend and MCP integration.

## ✅ Governance Compliance Status
- ✅ PROJECT_MAP.md present and updated
- ✅ Directory-level CLAUDE.md files created and updated
- ✅ Documentation consolidated and updated

## Directory Structure
```
contextkeeper/
├── src/
│   ├── ck_analytics/
│   ├── core/
│   ├── sacred/
│   └── tracking/
├── scripts/
│   └── contextkeeper.sh        # Main CLI script
├── tests/
├── docs/
│   ├── USER_GUIDE.md
│   ├── ARCHITECTURE.md
│   └── api/
│       └── API_REFERENCE.md
├── analytics_dashboard_live.html # Main dashboard
├── rag_agent.py                  # Main RAG orchestrator
└── README.md
```

## Key Files with Governance Context

### Core System Files
- **`rag_agent.py`**
  - Main orchestrator with Flask API server and Socket.IO for real-time updates.
  - Handles all RAG operations, project management, and serves the dashboard.
  - Dependencies: flask, chromadb, google.genai, flask-socketio.

- **`src/core/project_manager.py`**
  - Multi-project state management.
  - Tracks decisions, objectives, events.

### Sacred Layer
- **`src/sacred/sacred_layer_implementation.py`**
  - Implements immutable architectural decisions and the 2-layer approval system.

- **`src/sacred/enhanced_drift_sacred.py`**
  - Advanced drift detection engine.

### Analytics
- **`src/ck_analytics/analytics_service.py`**
  - Service layer for the `/analytics/sacred` endpoint.
- **`src/ck_analytics/sacred_metrics.py`**
  - Core logic for calculating governance metrics.

### Frontend
- **`analytics_dashboard_live.html`**
  - Real-time dashboard with WebSocket integration.
  - UI for project management, Sacred Plan approval, and global search.

### MCP Integration
- **`mcp-server/enhanced_mcp_server.js`**
  - Bridge for Claude Code integration.

## Development Workflow

1. **Start System**
   ```bash
   source venv/bin/activate
   python src/rag_agent.py server
   ```

2. **Create & Index Project**
   ```bash
   ./scripts/contextkeeper.sh project add "/path/to/your/code" "My Project"
   ```

3. **Interactive Usage**
   - **Dashboard**: Open `http://localhost:5556/analytics_dashboard_live.html`
   - **CLI**: Use `./scripts/contextkeeper.sh` for commands like `focus` and `query`.

## Next Governance Steps

1. **Enforcement Scripts** ✅ COMPLETED
   - Pre-commit hooks for governance are in place (`.pre-commit-config.yaml`).

2. **Documentation Lifecycle** ✅ COMPLETED
   - Documentation has been consolidated and updated.

3. **Continuous Verification** (Ongoing)
   - Ensure documentation is kept in sync with new features.
