# Project: ContextKeeper v3.0
Generated: 2025-08-05 23:45 AEST
Last Updated: 2025-08-05 (GOVERNANCE COMPLIANCE IN PROGRESS)

## 🎯 Project Overview
ContextKeeper v3.0 is an AI-powered development context management system with multi-project support, sacred architectural principles, and real-time analytics. Built as a hybrid Python/Node.js system with Flask backend and MCP integration.

**✨ NEW: Unified CLI** - All functionality now accessible through `python contextkeeper_cli.py` (or `./contextkeeper`), replacing multiple shell scripts with a single, comprehensive command-line interface.

## ✅ Governance Compliance Status
- ✅ PROJECT_MAP.md present and updated
- ✅ Directory-level CLAUDE.md files created (9/9 all directories)
- ✅ Governance header added to all core Python files
- ✅ Documentation archived (reduced from 44 to 6 essential files in root)
- ✅ Python files restructured into /src/ subdirectories (48 files moved)
- ✅ All imports updated to use new paths
- ⚠️ Enforcement scripts pending creation

## Directory Structure (POST-GOVERNANCE)
```
contextkeeper/
├── CLAUDE.md                    # Project-level context
├── PROJECT_MAP.md              # This file - governance compliant
├── README.md                   # User-facing documentation
├── CHANGELOG.md                # Release history
├── LOGBOOK.md                  # Development log
├── ARCHITECTURE.md             # System architecture
├── .env                        # Environment configuration
│
├── src/                        # Source code organization ✅ RESTRUCTURED
│   ├── CLAUDE.md              ✅ Directory context
│   ├── core/                  # Core system components
│   │   ├── CLAUDE.md          ✅ Directory context
│   │   ├── rag_agent.py       ✅ Governance header added
│   │   └── project_manager.py ✅ Governance header added
│   ├── sacred/                # Sacred layer implementation
│   │   ├── CLAUDE.md          ✅ Directory context
│   │   ├── sacred_layer_implementation.py ✅ Governance header
│   │   └── enhanced_drift_sacred.py      ✅ Governance header
│   ├── analytics/             # Analytics integration
│   │   ├── CLAUDE.md          ✅ Directory context
│   │   └── analytics_integration.py ✅ Governance header
│   ├── tracking/              # Event and git tracking
│   │   ├── CLAUDE.md          ✅ Directory context
│   │   └── git_activity_tracker.py ✅ Governance header
│   ├── scripts/               # Utility scripts and fixes
│   │   ├── CLAUDE.md          ✅ Directory context
│   │   └── [38 fix/patch scripts moved here]
│   └── utils/                 # Shared utilities (ready for future use)
│
├── docs/                       # Documentation repository
│   ├── CLAUDE.md              ✅ Directory context
│   ├── archive/               # 38 archived documentation files
│   │   └── MANIFEST.md        # Archive manifest
│   └── GOVERNANCE_CLEANUP_SUMMARY.md
│
├── contextkeeper_cli.py        # ✨ NEW: Unified Python CLI (replaces shell scripts)
├── contextkeeper               # ✨ NEW: Executable wrapper for CLI
├── cli/                        # ✨ NEW: CLI implementation modules
│   ├── __init__.py
│   └── commands/              # CLI command implementations
│       ├── __init__.py
│       ├── server.py          # Server management
│       ├── project.py         # Project operations
│       ├── query.py           # Knowledge queries
│       ├── sacred.py          # Sacred layer commands
│       └── utils.py           # System utilities
│
├── scripts/                    # Legacy automation scripts (DEPRECATED)
│   ├── CLAUDE.md              ✅ Directory context
│   ├── rag_cli_v2.sh          # (Deprecated - use contextkeeper_cli.py)
│   ├── contextkeeper.sh       # (Deprecated - use contextkeeper_cli.py)
│   ├── contextkeeper_simple.sh # (Deprecated - use contextkeeper_cli.py)
│   └── [other legacy scripts]
│
├── tests/                      # Test suites ✅ REORGANIZED
│   ├── CLAUDE.md              ✅ Directory context
│   ├── sacred/                # Sacred layer tests
│   ├── api/                   # API tests
│   ├── integration/           # Integration tests
│   └── [25 test files moved here from root]
│
├── mcp-server/                 # MCP Integration
│   ├── CLAUDE.md              ✅ Directory context
│   ├── enhanced_mcp_server.js # Main server
│   └── package.json
│
├── projects/                   # Project data storage
├── rag_knowledge_db/           # ChromaDB storage
├── .tmp/                       # Temporary and backup files
│   ├── rag_knowledge_db.old/   # Old database files
│   └── [backup Python files]
└── venv/                       # Python virtual environment
```

## Key Files with Governance Context

### Core System Files (now in src/core/)
- **`rag_agent.py`** (2022 lines) ✅ Governance header added
  - Main orchestrator with Flask API server
  - Handles all RAG operations and project management
  - Dependencies: flask, chromadb, google.genai
  - ✅ Imports updated to use new src/ paths
  
- **`project_manager.py`** (503 lines) ✅ Governance header added
  - Multi-project state management
  - Tracks decisions, objectives, events
  - Persists to projects/ directory

### Sacred Layer (now in src/sacred/)
- **`sacred_layer_implementation.py`** (527 lines) ✅ Governance header added
  - Immutable architectural decisions
  - 2-layer approval system
  - Drift detection

- **`enhanced_drift_sacred.py`** ✅ Governance header added
  - Advanced drift detection engine
  - Semantic similarity analysis
  - Recommendation generation

### Frontend
- **`analytics_dashboard_live.html`** (49k lines)
  - Three.js particle animation dashboard
  - Real-time metrics visualization
  - Interactive chat interface

### MCP Integration
- **`mcp-server/enhanced_mcp_server.js`**
  - Bridge for Claude Code integration
  - Provides development context tools
  - Handles LLM queries

## Active Architectural Decisions

1. **Multi-Project Isolation**
   - Each project gets isolated ChromaDB collection
   - Collection naming: `project_{project_id}`
   - Zero cross-contamination between projects

2. **Sacred Layer Architecture**
   - Immutable architectural decisions
   - 2-layer approval with SACRED_APPROVAL_KEY
   - Drift detection between plans and implementation

3. **Event-Driven Tracking**
   - Real-time development activity tracking
   - Temporal context for better retrieval
   - Git integration for commit tracking

4. **Performance Optimizations**
   - Async Flask endpoints
   - Path filtering for system files
   - Intelligent caching strategies

5. **Security First**
   - Automatic API key redaction
   - Project isolation enforcement
   - Secure approval workflows

## Development Workflow

1. **Start System**
   ```bash
   source venv/bin/activate
   python rag_agent.py server  # MUST use 'server'
   ```

2. **Create & Index Project**
   ```bash
   ./scripts/rag_cli_v2.sh projects create "Name" /path
   ./scripts/rag_cli_v2.sh projects focus <project_id>
   python rag_agent.py ingest --path /path
   ```

3. **Interactive Usage**
   ```bash
   ./contextkeeper_simple.sh  # Recommended
   ```

## Next Governance Steps

1. **Code Restructuring** ✅ COMPLETED
   - ✅ Moved 48 Python files from root to /src/ subdirectories
   - ✅ Added governance headers to all core files
   - ✅ Updated all imports to use new paths

2. **Enforcement Scripts** (High Priority - NEXT)
   - Create pre-commit hooks for governance
   - Automated context embedding checks
   - PROJECT_MAP.md auto-generation

3. **Documentation Lifecycle** (Medium Priority)
   - Establish archival policies
   - Create documentation templates
   - Automate LOGBOOK.md updates

## Dependencies
- Python 3.8+ with Flask, ChromaDB, Google GenAI
- Node.js 18+ for MCP server
- Google API credentials
- Sacred approval key

## Known Issues
- Server must use `python rag_agent.py server` (not 'start')
- Must manually index after project creation
- Collections may need server restart to load