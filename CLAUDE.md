# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
**ContextKeeper v3.0** - AI-powered development context management system with multi-project support, sacred architectural principles, and real-time analytics. Built as a hybrid Python/Node.js system with Flask backend and MCP integration.

## 🤖 SUBAGENT DELEGATION PROTOCOL (MANDATORY)

**CRITICAL**: Never attempt heavy lifting directly. Always delegate to specialized subagents first.

### Governance First (ALWAYS START HERE)
```bash
> use architecture-enforcer to assess project governance
> use project-scanner to analyze unknown codebases
> use chaos-manager for extremely messy projects
```

### Development Workflow Delegation
```bash
# Planning & Architecture
> use planner to break down complex features
> use solution-architect for system design
> use product-strategist for feature prioritization

# Implementation & Quality
> use code-implementer to build within skeleton structure
> use debugger to diagnose complex issues
> use maintainer to refactor legacy code
> use performance-optimiser to analyze bottlenecks

# Security & Compliance
> use security-guardian for comprehensive audits
> use code-reviewer for quality assurance
> use qa-engineer for testing strategies

# Documentation & Recovery
> use documentation-writer for technical docs
> use project-scanner for unknown projects
> use examples to create usage patterns
```

### Task-Specific Delegation Rules
- **Unknown codebase**: project-scanner → architecture-enforcer → solution-architect
- **Feature development**: planner → solution-architect → code-implementer → qa-engineer
- **Bug fixing**: debugger → maintainer → security-guardian
- **Documentation**: documentation-writer → examples → ui-ux-designer
- **Performance issues**: performance-optimiser → code-reviewer → maintainer

### Integration Priority
1. **ALWAYS** start with governance agents (architecture-enforcer/project-scanner)
2. **DELEGATE** complex tasks to specialized agents
3. **ORCHESTRATE** multi-agent workflows for complex problems
4. **DOCUMENT** all decisions via contextkeeper integration

## Essential Commands

### Daily Development
```bash
# Start development environment
source venv/bin/activate
python rag_agent.py server  # MUST use 'server', not 'start'

# Quick project management
./contextkeeper_simple.sh   # Interactive menu for chat/create/index
./quick_start.sh /path/to/project  # One-command setup

# Run tests
pytest tests/ -v --tb=short
pytest tests/sacred/ -v      # Sacred layer tests only
pytest tests/api/ -v -k "test_query"  # Specific API tests

# Check code style (Australian English)
python -m flake8 --extend-ignore=E501 *.py
```

### Project Indexing Workflow
```bash
# CRITICAL: Must follow this exact sequence
./scripts/rag_cli_v2.sh projects create "Name" /absolute/path
./scripts/rag_cli_v2.sh projects focus <project_id>
python rag_agent.py ingest --path /absolute/path  # OFTEN FORGOTTEN!

# Verify indexing worked
curl http://localhost:5556/projects | jq '.projects[] | select(.id=="<project_id>")'
```

### MCP Server Development
```bash
cd mcp-server
npm install
npm start  # Runs enhanced_mcp_server.js
```

## Architecture Overview

### System Flow
```
User Request → Claude Code → MCP Server → RAG Agent → ChromaDB/LLM
                    ↓             ↓             ↓
                Dashboard   Sacred Layer   Project Manager
```

### Core Components
1. **RAG Agent** (`rag_agent.py`): Flask API server, handles all operations
   - Async endpoints for performance
   - Project isolation via ChromaDB collections
   - Security filtering for sensitive data

2. **Project Manager** (`project_manager.py`): Multi-project state management
   - Each project gets isolated ChromaDB collection
   - Tracks decisions, objectives, and events
   - Persists to `projects/` directory

3. **Sacred Layer** (`sacred_layer_implementation.py`): Architectural governance
   - Immutable architectural decisions
   - 2-layer approval system
   - Drift detection between plans and implementation

4. **MCP Integration** (`mcp-server/enhanced_mcp_server.js`): Claude Code bridge
   - Provides tools for context retrieval
   - Handles sacred drift checking
   - Manages LLM queries

5. **Dashboard** (`analytics_dashboard_live.html`): Three.js visualization
   - Real-time project metrics
   - Interactive chat interface
   - 4000 animated particles (performance consideration)

## Critical Implementation Details

### ChromaDB Collections
- Collection naming: `project_{project_id}`
- Metadata constraints: Only str, int, float, bool, None
- Arrays must be comma-separated strings: `'tags': ', '.join(tags)`
- Embedding model: Google's text-embedding-004 (768 dimensions)

### API Authentication
All endpoints require project_id for isolation:
```python
# WRONG - security risk
@app.route('/query', methods=['POST'])
def query():
    return self.agent.query(request.json['question'])

# CORRECT - enforces isolation
@app.route('/query', methods=['POST'])
def query():
    project_id = request.json.get('project_id')
    if not project_id:
        return {'error': 'project_id required'}, 400
    return self.agent.query(request.json['question'], project_id=project_id)
```

### Error Handling Patterns
```python
# Always use this pattern for ChromaDB operations
try:
    collection = self.db.get_collection(f"project_{project_id}")
except:
    # Collection doesn't exist - create it
    collection = self.db.create_collection(
        name=f"project_{project_id}",
        embedding_function=self.embedding_function,
        metadata={"hnsw:space": "cosine"}
    )
```

## Common Issues & Solutions

### Issue: "Project not found" after creation
**Cause**: Server's `self.collections` dict not updated
**Fix**: Restart server or call `self.agent._init_project_collections()`

### Issue: Poor query results
**Cause**: Project not indexed or focused
**Fix**: 
```bash
./scripts/rag_cli_v2.sh projects focus <project_id>
python rag_agent.py ingest --path /project/path
```

### Issue: Embedding dimension mismatch
**Cause**: Using wrong Google API model
**Fix**: Ensure using `text-embedding-004` not `gemini-embedding-001`

### Issue: Server segmentation fault
**Cause**: Using `python rag_agent.py start`
**Fix**: Always use `python rag_agent.py server`

## Testing Guidelines
- Run tests with `pytest -v --tb=short` for cleaner output
- Sacred layer tests require `SACRED_APPROVAL_KEY` in .env
- API tests use real ChromaDB - ensure clean state
- Use `./cleanup_all.sh` for fresh test environment

## Code Style Requirements
- Australian English spelling (colour, behaviour, realise)
- Conversational comments ("alright, so here's the thing...")
- Update LOGBOOK.md after significant changes
- Format: `[YYYY-MM-DD HH:MM AEST] - [Component] - [Action] - [Details]`

## Environment Variables
```bash
GOOGLE_API_KEY=        # Required: Gemini API access
SACRED_APPROVAL_KEY=   # Required: Sacred layer approvals
FLASK_ASYNC_MODE=True  # Performance: Async endpoints
DEBUG=0               # Production: Disable debug mode
```

## Performance Considerations
- Each project uses ~100MB for ChromaDB collection
- Dashboard animation may lag on older devices
- Indexing speed: ~1000 files/minute
- Query latency: <500ms for most operations
- Use path filtering to exclude system files