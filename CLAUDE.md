# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
**ContextKeeper v3.0** - AI-powered development context management system with multi-project support, sacred architectural principles, and real-time analytics. Built as a hybrid Python/Node.js system with Flask backend and MCP integration.

## Essential Commands

### CLI Usage (NEW - ✅ COMPLETE)
```bash
# Main CLI entry point (interactive menu if no args)
python contextkeeper_cli.py
./contextkeeper  # After running setup_cli.py

# Quick commands
python contextkeeper_cli.py --help
python contextkeeper_cli.py server start
python contextkeeper_cli.py project list
python contextkeeper_cli.py query ask "How does authentication work?"
python contextkeeper_cli.py sacred status

# Setup and test CLI
python setup_cli.py  # Installs Click/requests, creates wrapper
python test_cli.py   # Test all CLI components
```

### Server and Testing
```bash
# Start server (NEW UNIFIED CLI - RECOMMENDED)
python contextkeeper_cli.py server start
# Or: ./contextkeeper server start (after setup)

# Legacy method (still works):
source venv/bin/activate
python rag_agent.py server  # Direct Flask server

# Run tests
pytest tests/ -v --tb=short
pytest tests/sacred/ -v -k "test_plan"  # Specific sacred tests
pytest tests/api/ -v -k "test_query"    # API endpoint tests

# Quick project setup (NEW CLI - RECOMMENDED)
python contextkeeper_cli.py  # Interactive menu
# Or with auto-setup:
python contextkeeper_cli.py project create "Name" /path/to/project --auto-index
```

### Project Management Workflow
```bash
# NEW UNIFIED CLI: All-in-one command
python contextkeeper_cli.py project create "Name" /absolute/path --auto-index

# Or step-by-step:
python contextkeeper_cli.py project create "Name" /absolute/path
python contextkeeper_cli.py project focus <project_id>
python contextkeeper_cli.py project index <project_id>

# Verify indexing worked
python contextkeeper_cli.py project list
# Or via API:
curl http://localhost:5556/projects | jq '.projects[] | select(.id=="<project_id>")'
```

### MCP Server Setup
```bash
cd mcp-server
npm install
npm start  # Runs enhanced_mcp_server.js
```

## Architecture Overview

### System Components
```
User Request → Claude Code → MCP Server → RAG Agent → ChromaDB/LLM
                    ↓             ↓             ↓
                Dashboard   Sacred Layer   Project Manager
```

1. **RAG Agent** (`rag_agent.py`): Flask API server, port 5556
   - Async endpoints for performance
   - Project isolation via ChromaDB collections
   - Automatic security filtering

2. **Project Manager** (`project_manager.py`): Multi-project state
   - Collection naming: `project_{project_id}`
   - Persists to `projects/` directory
   - Tracks decisions, objectives, events

3. **Sacred Layer** (`sacred_layer_implementation.py`): Architectural governance
   - Immutable plans with 2-layer approval
   - Drift detection between plans and implementation
   - Plan states: DRAFT, APPROVED, LOCKED, SUPERSEDED

4. **MCP Integration** (`mcp-server/enhanced_mcp_server.js`): Claude Code bridge
   - 8 tools for context retrieval and management
   - Handles sacred drift checking
   - Manages LLM queries

5. **Dashboard** (`analytics_dashboard_live.html`): Three.js visualization
   - 4000 animated particles (performance consideration)
   - Real-time project metrics
   - Interactive chat interface

6. **CLI System** (`contextkeeper_cli.py` + `cli/commands/`): ✅ COMPLETE
   - Click-based command structure with 5 command groups
   - Interactive menu system when run without arguments
   - Server management: start, stop, restart, status, logs
   - Project management: create, list, focus, ingest, archive
   - Query system: ask, search, history, stats, interactive mode
   - Sacred layer: status, decisions, approve, drift detection
   - System utilities: health, version, config, backup, cleanup
   - API integration with Flask server on port 5556

## Critical Implementation Details

### ChromaDB Requirements
```python
# Collection naming MUST follow this pattern
collection_name = f"project_{project_id}"

# Metadata constraints - only primitives allowed
metadata = {
    'tags': ', '.join(tags),  # Arrays must be comma-separated strings
    'status': 'active',       # Only str, int, float, bool, None
}

# Embedding model (768 dimensions)
embedding_function = GoogleGenerativeAiEmbeddingFunction(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model_name="text-embedding-004"
)
```

### API Authentication Pattern
```python
# CORRECT - enforces project isolation
@app.route('/query', methods=['POST'])
def query():
    project_id = request.json.get('project_id')
    if not project_id:
        return {'error': 'project_id required'}, 400
    return self.agent.query(request.json['question'], project_id=project_id)
```

### Error Handling Pattern
```python
# Always use for ChromaDB operations
try:
    collection = self.db.get_collection(f"project_{project_id}")
except:
    collection = self.db.create_collection(
        name=f"project_{project_id}",
        embedding_function=self.embedding_function,
        metadata={"hnsw:space": "cosine"}
    )
```

## Common Issues & Solutions

### "Project not found" after creation
**Fix**: Restart server or call `self.agent._init_project_collections()`

### Poor query results
**Fix**: Ensure project is indexed:
```bash
./scripts/rag_cli_v2.sh projects focus <project_id>
python rag_agent.py ingest --path /project/path
```

### Embedding dimension mismatch
**Fix**: Use `text-embedding-004` not `gemini-embedding-001`

### Server segmentation fault
**Fix**: Always use `python rag_agent.py server` (not 'start')

## Environment Variables
```bash
# Required
GOOGLE_API_KEY=        # Gemini API access
SACRED_APPROVAL_KEY=   # Sacred layer approvals

# Optional
FLASK_ASYNC_MODE=True  # Async endpoints (recommended)
DEBUG=0               # Production mode
```

## Code Style
- Australian English spelling (colour, behaviour, realise)
- Conversational comments preferred
- Update LOGBOOK.md after significant changes
- Format: `[YYYY-MM-DD HH:MM AEST] - [Component] - [Action]`

## Performance Considerations
- Each project uses ~100MB for ChromaDB collection
- Dashboard animation may lag on older devices (4000 particles)
- Indexing speed: ~1000 files/minute
- Query latency: <500ms typical
- Use path filtering to exclude system files

## Directory Structure
```
contextkeeper/
├── src/                    # Core implementation modules
│   ├── sacred/            # Sacred layer components
│   ├── tracking/          # Git and event tracking
│   └── analytics/         # Analytics services
├── mcp-server/            # Claude Code MCP integration
├── scripts/               # CLI tools (use rag_cli_v2.sh)
├── tests/                 # Test suites (pytest)
├── projects/              # Project data persistence
└── rag_knowledge_db/      # ChromaDB storage
```