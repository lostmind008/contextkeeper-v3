# ContextKeeper v3 Unified CLI Implementation Plan

**Project**: ContextKeeper v3 Unified CLI  
**Location**: `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/`  
**Timeline**: 4 days (32 development hours)  
**Framework**: Click (Python CLI framework)  

## Executive Summary

Transform the existing shell script ecosystem into a unified Python CLI that provides all ContextKeeper functionality through a single `contextkeeper` command. This plan builds upon the existing CLI foundation in `/cli/` directory and integrates with the current Flask API server.

---

## Phase 1 - Foundation Setup (Day 1 Morning - 4 hours)

### 1.1 Project Structure & Dependencies

**Files to Create:**
```bash
/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/setup.py
/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/__init__.py
/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/main.py
/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/core/__init__.py
/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/commands/__init__.py
/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/interactive/__init__.py
```

**Commands to Run:**
```bash
cd /Users/sumitm1/contextkeeper-pro-v3/contextkeeper

# Install Click framework
pip install click rich tabulate psutil requests

# Create package structure
touch cli/__init__.py cli/core/__init__.py cli/commands/__init__.py cli/interactive/__init__.py

# Install in development mode
pip install -e .
```

**Success Criteria:**
- `contextkeeper --help` displays main help
- All directories have `__init__.py` files
- Dependencies installed without conflicts

### 1.2 Main CLI Entry Point

**Primary Task:** Create `cli/main.py` with main Click command group

**Dependencies:** Click, existing CLI modules

**Key Features:**
- Main `contextkeeper` command group
- Global options (--project-id, --verbose, --config)
- Version information
- Basic error handling

**Testing Approach:**
```bash
# Test basic CLI structure
contextkeeper --version
contextkeeper --help
contextkeeper server --help
```

---

## Phase 2 - Core Commands (Day 1 Afternoon - 4 hours)

### 2.1 Server Management Commands

**Files to Modify/Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/commands/server.py`
- Integrate with existing `rag_agent.py`

**Commands to Implement:**
```bash
contextkeeper server start     # Replace restart_server.sh
contextkeeper server stop      # New functionality
contextkeeper server status    # Check if running
contextkeeper server logs      # Show recent logs
contextkeeper server restart   # Combine stop/start
```

**Dependencies:** psutil, requests, subprocess

**Integration Points:**
- Use existing `rag_agent.py server` command
- Parse existing log files
- Health check via API endpoints

### 2.2 Project Management Commands

**Files to Modify:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/commands/project.py` (exists)

**Commands to Implement:**
```bash
contextkeeper project create <name> <path>    # Replace rag_cli_v2.sh
contextkeeper project list                    # Show all projects
contextkeeper project focus <id>             # Set active project
contextkeeper project info <id>              # Project details
contextkeeper project delete <id>            # Remove project
contextkeeper project index <id>             # Re-index project
```

**API Integration:**
- Use existing Flask API endpoints
- Handle ChromaDB collection management
- Project state persistence

### 2.3 Basic Query Commands

**Files to Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/commands/query.py`

**Commands to Implement:**
```bash
contextkeeper query <question>               # Basic query
contextkeeper query --project <id> <q>      # Project-specific
contextkeeper query --interactive           # Chat mode
```

**Success Criteria:**
- All core commands functional
- API integration working
- Error handling in place

---

## Phase 3 - Advanced Features (Day 2 - 8 hours)

### 3.1 Sacred Layer Integration

**Files to Create/Modify:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/commands/sacred.py`
- Integration with existing `sacred_layer_implementation.py`

**Commands to Implement:**
```bash
contextkeeper sacred plan create <name>       # Create architectural plan
contextkeeper sacred plan list               # List all plans
contextkeeper sacred plan approve <id>       # Approve plan
contextkeeper sacred drift check <project>   # Check for drift
contextkeeper sacred decision add <text>     # Add decision
```

**Integration Requirements:**
- Sacred approval key handling
- 2-layer approval workflow
- Drift detection between plans and implementation

### 3.2 Decision & Objective Tracking

**Files to Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/commands/decision.py`
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/commands/objective.py`

**Commands to Implement:**
```bash
contextkeeper decision add <text>            # Add decision
contextkeeper decision list [--project id]  # List decisions
contextkeeper objective set <text>           # Set objective
contextkeeper objective track <id>           # Track progress
```

### 3.3 Analytics Integration

**Files to Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/commands/analytics.py`

**Commands to Implement:**
```bash
contextkeeper analytics dashboard            # Open dashboard
contextkeeper analytics report <project>     # Generate report
contextkeeper analytics export <format>      # Export data
```

**Success Criteria:**
- Sacred layer fully integrated
- Decision tracking operational
- Analytics accessible via CLI

---

## Phase 4 - Interactive Features (Day 3 - 8 hours)

### 4.1 Enhanced Menu System

**Files to Modify:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/interactive/menu.py` (exists)

**Features to Implement:**
- Rich TUI with colours and formatting
- Navigation breadcrumbs
- Context-aware menus
- Keyboard shortcuts

**Commands:**
```bash
contextkeeper menu                          # Launch interactive menu
contextkeeper menu --project <id>          # Project-specific menu
```

### 4.2 Chat Interface

**Files to Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/interactive/chat.py`

**Features:**
- Real-time chat with project context
- History persistence
- Command suggestions
- Multi-line input support

**Commands:**
```bash
contextkeeper chat                          # Start chat session
contextkeeper chat --project <id>          # Project chat
contextkeeper chat --history               # Show chat history
```

### 4.3 Progress Tracking & Notifications

**Files to Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/utils/progress.py`
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/utils/notifications.py`

**Features:**
- Progress bars for long operations
- Desktop notifications
- Status indicators

**Success Criteria:**
- Interactive menu fully functional
- Chat interface operational
- Progress feedback implemented

---

## Phase 5 - Migration & Compatibility (Day 4 - 8 hours)

### 5.1 Shell Script Compatibility Wrappers

**Files to Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/compat/`
- Wrapper scripts for each legacy command

**Migration Strategy:**
```bash
# Create compatibility wrappers
contextkeeper_simple.sh -> contextkeeper menu
rag_cli_v2.sh -> contextkeeper project
chat_with_project.sh -> contextkeeper chat
```

### 5.2 Configuration Migration

**Files to Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/commands/migrate.py`

**Migration Commands:**
```bash
contextkeeper migrate from-scripts          # Migrate from shell scripts
contextkeeper migrate config               # Update configuration
contextkeeper migrate projects             # Migrate existing projects
```

### 5.3 Comprehensive Testing

**Files to Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/tests/cli/`
- Unit tests for all CLI modules
- Integration tests for workflows

**Test Commands:**
```bash
pytest tests/cli/ -v --tb=short
contextkeeper test-suite                   # Built-in test runner
```

### 5.4 Documentation & Help System

**Files to Create:**
- `/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/help/`
- Context-sensitive help
- Command examples
- Troubleshooting guides

**Success Criteria:**
- All shell scripts have CLI equivalents
- Migration tools functional
- Complete test coverage
- Documentation complete

---

## Implementation Details

### Directory Structure
```
cli/
├── __init__.py
├── main.py                 # Main entry point
├── core/
│   ├── __init__.py
│   ├── context.py          # Existing - enhance
│   ├── api_client.py       # Existing - enhance
│   ├── config.py           # New - configuration management
│   └── exceptions.py       # New - custom exceptions
├── commands/
│   ├── __init__.py
│   ├── project.py          # Existing - enhance
│   ├── server.py           # New - server management
│   ├── query.py            # New - query operations
│   ├── sacred.py           # New - sacred layer
│   ├── decision.py         # New - decision tracking
│   ├── objective.py        # New - objective management
│   ├── analytics.py        # New - analytics integration
│   └── migrate.py          # New - migration tools
├── interactive/
│   ├── __init__.py
│   ├── menu.py             # Existing - enhance
│   ├── chat.py             # New - chat interface
│   └── prompts.py          # New - user prompts
├── utils/
│   ├── __init__.py
│   ├── progress.py         # New - progress indicators
│   ├── notifications.py    # New - desktop notifications
│   ├── formatting.py       # New - output formatting
│   └── validation.py       # New - input validation
└── compat/
    ├── __init__.py
    └── wrappers.py         # New - legacy script wrappers
```

### Key Dependencies
```python
# setup.py dependencies
install_requires=[
    "click>=8.0.0",           # CLI framework
    "rich>=12.0.0",           # Rich text and beautiful formatting
    "tabulate>=0.9.0",        # Table formatting
    "psutil>=5.8.0",          # System monitoring
    "requests>=2.28.0",       # HTTP client
    "python-dotenv>=0.19.0",  # Environment variables
    "pydantic>=1.10.0",       # Data validation
    "typer>=0.7.0",           # CLI enhancements (optional)
]
```

### Testing Strategy

**Unit Tests:**
- Each command module tested independently
- Mock API responses
- Configuration edge cases

**Integration Tests:**
- Full workflow testing
- API server interaction
- File system operations

**Performance Tests:**
- CLI startup time (<1 second)
- Large project handling
- Memory usage monitoring

### Deployment Strategy

1. **Development Installation:**
   ```bash
   pip install -e .
   ```

2. **Production Installation:**
   ```bash
   pip install contextkeeper-v3
   ```

3. **Binary Distribution:**
   ```bash
   # Future: PyInstaller for standalone executable
   pyinstaller --onefile cli/main.py
   ```

---

## Risk Mitigation

### Technical Risks
- **API Compatibility**: Extensive testing against existing Flask API
- **Performance**: Profiling and optimisation in Phase 4
- **Dependencies**: Pin versions and test compatibility

### User Experience Risks
- **Learning Curve**: Comprehensive help system and migration tools
- **Workflow Disruption**: Gradual migration with compatibility wrappers
- **Feature Parity**: Careful mapping of all shell script functionality

### Maintenance Risks
- **Code Quality**: Comprehensive testing and documentation
- **Future Updates**: Modular architecture for easy updates
- **Backward Compatibility**: Version management and deprecation strategy

---

## Success Metrics

### Functional Metrics
- [ ] 100% shell script functionality replicated
- [ ] <1 second CLI startup time
- [ ] >95% API integration success rate
- [ ] Zero data loss during migration

### User Experience Metrics
- [ ] Intuitive command structure
- [ ] Comprehensive help system
- [ ] Error messages actionable
- [ ] Progress feedback for long operations

### Quality Metrics
- [ ] >90% test coverage
- [ ] Zero critical security vulnerabilities
- [ ] Australian English spelling throughout
- [ ] Documentation complete and accurate

---

## Timeline Checkpoints

### Day 1 Checkpoint
- [ ] Basic CLI structure functional
- [ ] Server management commands working
- [ ] Project operations integrated

### Day 2 Checkpoint
- [ ] Sacred layer fully integrated
- [ ] Decision/objective tracking operational
- [ ] Analytics accessible

### Day 3 Checkpoint
- [ ] Interactive menu enhanced
- [ ] Chat interface functional
- [ ] Progress tracking implemented

### Day 4 Checkpoint
- [ ] Migration tools complete
- [ ] All tests passing
- [ ] Documentation ready
- [ ] Ready for production use

---

## Agent Assignment

### code-implementer Tasks
- Phase 1: Foundation setup and entry point
- Phase 2: Core command implementation
- Phase 5: Migration tools and wrappers

### solution-architect Tasks
- CLI architecture validation
- API integration design
- Performance optimization strategy

### qa-engineer Tasks
- Test suite design and implementation
- Integration testing strategy
- Performance benchmarking

### security-guardian Tasks
- Input validation security
- API authentication handling
- Configuration security review

### documentation-writer Tasks
- Help system content
- Migration guides
- API documentation updates

---

**Implementation Start**: Ready to begin Phase 1  
**Estimated Completion**: 4 working days  
**Next Action**: Execute Phase 1.1 - Project structure setup