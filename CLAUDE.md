# CLAUDE.md - AI Assistant Context

## 🎯 CURRENT DEVELOPMENT STATE
**Project**: ContextKeeper v3.0 Sacred Layer Upgrade  
**Branch**: ContextKeeper-v3.0-upgrade  
**Status**: Phase 1 - Ready to execute upgrade  
**Priority**: Implement Sacred Layer with 2-layer verification  
**Last Updated**: 2025-07-24

## 🚀 QUICK START (Get Running in 2 Minutes)
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Start the agent (v2.0 working)
python rag_agent.py start

# 3. Test current functionality
./rag_cli.sh projects list

# 4. Run v3 upgrade (when ready)
./upgrade_to_v3_sacred.sh
```

## 🔥 CURRENT FOCUS - Sacred Layer Implementation
**What I'm working on RIGHT NOW:**

1. **IMMEDIATE**: Complete Phase 2 sacred layer implementation ⚠️ IN PROGRESS
2. **NEW**: Phase 2.5 - LLM-Enhanced Query Responses (APPROVED) ⭐
3. **NEXT**: Phase 3 - MCP server for Claude Code integration
4. **FINALLY**: Test sacred plan creation and approval workflow

**Key files to work with:**
- `rag_agent.py` ⚠️ Needs Phase 2.5 LLM enhancement integration
- `sacred_layer_implementation.py` ✅ Core methods implemented
- `git_activity_tracker.py` ✅ Methods implemented
- `enhanced_drift_sacred.py` ✅ Methods implemented

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

### Sacred Plan Workflow (v3.0 target)
```bash
# 1. Create plan
./rag_cli.sh sacred create proj_123 "Auth Architecture" auth_plan.md

# 2. Approve with 2-layer verification  
./rag_cli.sh sacred approve plan_abc123

# 3. Check alignment
./rag_cli.sh sacred drift proj_123
```

### LLM-Enhanced Query Testing (Phase 2.5)
```bash
# Test natural language responses
curl -X POST http://localhost:5555/query_llm \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the sacred layer?", "k": 5}'

# Compare with raw query  
curl -X POST http://localhost:5555/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the sacred layer?", "k": 5}'
```

## 🚨 CURRENT BLOCKERS & GOTCHAS

1. **Sacred Integration**: Need to import sacred components into `rag_agent.py`
2. **Environment Key**: Set `SACRED_APPROVAL_KEY` in `.env` before testing
3. **ChromaDB Isolation**: Sacred plans MUST use separate collections
4. **Backward Compatibility**: v2.0 functionality must keep working

## 🧭 CONTEXT HIERARCHY

When you need more info, check in this order:
1. `AI_AGENT_TODO_EXPANDED.md` - Micro-tasks (current work)
2. `v3 Approved Plan for AI Agent/AI Agent TODO List.md` - Step-by-step guide
3. `QUICK_REFERENCE.md` - All CLI commands
4. `PROJECT_SUMMARY.md` - v2.0 implementation summary

## 🎯 SUCCESS CRITERIA

**Phase 1 Complete When:**
- [ ] Sacred layer activated via upgrade script
- [ ] `rag_agent.py` imports sacred components
- [ ] Sacred plan creation works
- [ ] 2-layer approval process works
- [ ] Drift detection compares against sacred plans

**Ready for MCP Integration When:**
- [ ] All sacred endpoints responding
- [ ] Tests passing
- [ ] Claude Code can create/approve sacred plans

## ⚙️ ENVIRONMENT CHECK

Required for sacred layer:
```bash
# Check these exist
echo $SACRED_APPROVAL_KEY        # Should be set
ls sacred_layer_implementation.py # Should exist
ls tests/sacred/                 # Should exist
./upgrade_to_v3_sacred.sh --check # Should pass
```

---
**For detailed setup, API docs, or architecture deep-dive, see:**
- `SETUP.md` - Environment setup
- `API_REFERENCE.md` - All endpoints  
- `ARCHITECTURE.md` - System design
- `QUICK_REFERENCE.md` - All commands