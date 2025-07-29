# CLAUDE.md - AI Assistant Context

## 🎯 CURRENT DEVELOPMENT STATE
**Project**: ContextKeeper v3.0
**Branch**: main
**Status**: ✅ v3.0 Upgrade Complete
**Priority**: General Maintenance
**Last Updated**: 2025-07-29 (All documentation and merge conflicts resolved)

## 🚀 QUICK START (Get Running in 2 Minutes)
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Start the agent
python rag_agent.py start

# 3. Test working endpoints  
curl http://localhost:5556/health       # Should return {"status":"healthy"}
curl http://localhost:5556/projects     # Should return projects data
./scripts/rag_cli_v2.sh projects list   # CLI interface

# 4. Check MCP server is connected (optional)
# Verify in Claude Code that contextkeeper-sacred tools are available
```

## 🔥 CURRENT STATUS - Sacred Layer COMPLETE ✅

### ✅ LATEST UPDATE: All Infrastructure Fixes & Documentation Completed
**Date**: 2025-07-29  
**Status**: All major infrastructure issues resolved and fully operational  
**Fixes Completed**:
- ✅ Flask Async Compatibility: All async endpoints now return 200 OK (was 500 errors)
- ✅ Path Filtering: Fixed venv/site-packages indexing pollution 
- ✅ API Model Updates: Updated to latest Google GenAI models (gemini-embedding-001, gemini-2.5-flash)
- ✅ CLI Port Fix: Sacred CLI now connects to correct port 5556 (was 5555)
- ✅ Sacred Layer Testing: Comprehensive testing completed, all endpoints functional
- ✅ CLI Merge Conflicts: All merge conflicts in rag_cli_v2.sh resolved
- ✅ ChromaDB Compatibility: Database reset and embedding function conflicts resolved
- ✅ Documentation Update: README, API_REFERENCE, TROUBLESHOOTING, and CLAUDE.md all updated

**Current State**: All Sacred Layer endpoints, CLI commands, and core RAG functionality operational
**What I've completed:**

1. **COMPLETE**: ✅ Phase 2 Sacred Layer Implementation 
2. **COMPLETE**: ✅ Phase 2.5 - LLM-Enhanced Query Responses 
3. **COMPLETE**: ✅ Phase 3 - MCP Server for Claude Code Integration
4. **COMPLETE**: ✅ Sacred plan creation and approval workflow tested

**Available Enhancement Options:**
- Phase 4: Analytics Dashboard (infrastructure ready)
- Advanced monitoring and metrics
- Additional MCP tools and integrations

**Key files completed:**
- `rag_agent.py` ✅ Phase 2.5 LLM enhancement integrated and operational
- `sacred_layer_implementation.py` ✅ Core methods implemented and tested
- `git_activity_tracker.py` ✅ Methods implemented and integrated
- `enhanced_drift_sacred.py` ✅ Methods implemented and operational
- `mcp-server/enhanced_mcp_server.js` ✅ 8 tools implemented and tested

## 🛠️ DEVELOPMENT PATTERNS

### Code Style (Follow User's Preferences)
```python
# Use Australian English spelling
colour = "blue"  # not color
behaviour = "expected"  # not behavior

# Conversational comments (user's signature style)
# alright, so the idea here is to...
# basically, we need to do this because...
# fair warning - this might seem unconventional, but...
```

### Architecture Patterns to Follow
- **Sacred Layer**: Immutable storage, 2-layer verification, isolated ChromaDB
- **Project Isolation**: Each project gets own ChromaDB collection
- **Git Integration**: Track commits, not file changes
- **Fail-Safe Design**: Sacred plans act as guardrails for AI agents

### Testing Approach
```bash
# Always test after changes
pytest tests/sacred -v          # Sacred layer
pytest tests/git -v             # Git integration  
pytest tests/drift -v           # Drift detection
python test_multiproject.py     # End-to-end
```

## 📁 FILE NAVIGATION MAP

**Core Sacred Files** (what you'll work with most):
```
rag_agent.py                 # Main orchestrator - ADD sacred integration here
sacred_layer_implementation.py  # Sacred core - USE as-is
git_activity_tracker.py     # Git tracking - USE as-is
enhanced_drift_sacred.py    # Drift detection - USE as-is
sacred_cli_integration.sh   # CLI commands - SOURCE this
```

**Reference Implementations** (approved patterns):
```
v3 Approved Plan for AI Agent/
├── sacred_layer_implementation.py    # Reference if needed
├── enhanced_mcp_server.js           # MCP server for later
├── analytics_dashboard.html         # Dashboard for later
└── revised_implementation_roadmap.md # Complete vision
```

## ⚡ COMMON WORKFLOWS

### Sacred Plan Workflow
```bash
# 1. Create a sacred plan
./scripts/rag_cli_v2.sh sacred create proj_123 "API Authentication" api_auth_plan.md

# 2. Approve the plan with 2-layer verification
./scripts/rag_cli_v2.sh sacred approve plan_abc123

# 3. Check for drift
./scripts/rag_cli_v2.sh sacred drift proj_123
```

### Querying the Knowledge Base
```bash
# Ask a question via CLI
./scripts/rag_cli_v2.sh ask "What is the approved method for API authentication?"

# Test natural language responses via API
curl -X POST http://localhost:5556/query_llm \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the sacred layer?", "k": 5}'

# Compare with raw query  
curl -X POST http://localhost:5556/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the sacred layer?", "k": 5}'
```

### LLM-Enhanced Query
```bash
# Get a natural language response
curl -X POST http://localhost:5556/query_llm \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain the sacred layer.", "k": 5}'
```

## 🚨 CURRENT STATUS & KNOWN ISSUES

### ✅ Currently Working
- **Service Running**: ContextKeeper runs on port 5556
- **Health Check**: `/health` endpoint returns {"status":"healthy"}
- **Projects API**: `/projects` endpoint returns project data
- **MCP Integration**: MCP server configured and connects to Claude Code

### ✅ System Status: Fully Operational
- ✅ **Database Connectivity**: ChromaDB connections working correctly
- ✅ **Query Endpoints**: All query endpoints functional (raw and LLM-enhanced)
- ✅ **Sacred Integration**: All sacred layer endpoints tested and operational
- ✅ **CLI Commands**: Sacred CLI commands working with proper port connectivity
- ✅ **API Endpoints**: All Flask async endpoints returning proper responses
- ✅ **Path Filtering**: No more venv/site-packages pollution in knowledge base

## 🧭 CONTEXT HIERARCHY

When you need more info, check in this order:
1. `AI_AGENT_TODO_EXPANDED.md` - Micro-tasks (current work)
2. `v3 Approved Plan for AI Agent/AI Agent TODO List.md` - Step-by-step guide
3. `QUICK_REFERENCE.md` - All CLI commands
4. `PROJECT_SUMMARY.md` - v2.0 implementation summary

## 🎯 MCP Server Tools

The MCP server provides the following tools for AI assistants:

- **`get_sacred_context`**: Get approved sacred plans for a project.
- **`check_sacred_drift`**: Check if current development aligns with sacred plans.
- **`query_with_llm`**: Query the knowledge base with natural language responses.
- **`export_development_context`**: Export complete development context including sacred plans.
- **`get_development_context`**: Get comprehensive development context including project status, git activity, objectives, decisions, and sacred layer analysis.
- **`intelligent_search`**: Search with semantic understanding across code, decisions, objectives, and sacred plans.
- **`create_sacred_plan`**: Create a new sacred architectural plan.
- **`health_check`**: Check the health status of the sacred layer and RAG agent.

## ⚙️ ENVIRONMENT CHECK

Required for sacred layer:
```bash
# Check these exist
echo $SACRED_APPROVAL_KEY        # Should be set
ls sacred_layer_implementation.py # Should exist
ls tests/sacred/                 # Should exist
./upgrade_to_v3_sacred.sh --check # Should pass
```

## 📝 DOCUMENTATION MAINTENANCE PROTOCOL

### Critical Learning: Avoid Misleading Legacy Documentation
**Issue Discovered**: Comments and documentation left behind during development can mislead future readers who might assume outdated status represents current state rather than checking latest enhancements.

**Mandatory Practice for AI Coding Agents:**
1. **Clean Up As You Go**: Remove outdated comments, TODOs, and status indicators immediately when completing work
2. **Update Status Consistently**: Ensure all documentation files reflect current implementation state
3. **Remove Placeholder Content**: Delete template comments, example code, and "TODO" markers when functionality is complete
4. **Verify Cross-References**: Check that all file references, command examples, and technical details match actual implementation
5. **Document Completion**: Mark phases/tasks as complete in ALL relevant files, not just primary documentation

**Example**: After completing Phase 3, ALL files should show "Phase 3 COMPLETE" status, not mixed states like "Phase 1 Ready" in some files and "Phase 3 Complete" in others.

**Why This Matters**: Future developers (including AI agents) rely on documentation accuracy. Inconsistent or outdated documentation creates confusion and can lead to incorrect assumptions about project state.

---
**For detailed setup, API docs, or architecture deep-dive, see:**
- `SETUP.md` - Environment setup
- `API_REFERENCE.md` - All endpoints  
- `ARCHITECTURE.md` - System design
- `QUICK_REFERENCE.md` - All commands