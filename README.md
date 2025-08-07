# ContextKeeper v3.0 🚀

**AI-powered development context management with multi-project support and sacred architectural governance**

ContextKeeper v3.0 is a comprehensive development assistant that helps you maintain context across complex projects. It combines intelligent document indexing, real-time chat capabilities, and architectural governance to keep your development workflow organised and efficient.

## ✨ Key Features

- **Multi-Project Management**: Isolated context per project with automatic switching
- **Intelligent Indexing**: AI-powered document understanding and retrieval
- **Real-Time Chat**: Interactive development assistant with project context
- **Sacred Architecture Layer**: Immutable architectural decisions with drift detection
- **MCP Integration**: Seamless Claude Code integration for enhanced development
- **Live Dashboard**: Beautiful Three.js visualisation with real-time metrics
- **Unified CLI**: Single command-line interface replacing multiple scripts

## 🚀 Quick Start

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd contextkeeper
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Setup Unified CLI** (Optional but recommended)
   ```bash
   chmod +x contextkeeper_cli.py
   ln -s $(pwd)/contextkeeper_cli.py ./contextkeeper
   ```

### One-Command Project Setup

**Using the new unified CLI** (replaces all shell scripts):

```bash
# Create and auto-index a project
python contextkeeper_cli.py project create "MyProject" /path/to/project --auto-index

# Or use the quick alias after setup
./contextkeeper project create "MyProject" /path/to/project --auto-index
```

**Traditional method**:
```bash
# Start the server
python contextkeeper_cli.py server start

# Create project (in another terminal)
python contextkeeper_cli.py project create "MyProject" /path/to/project
python contextkeeper_cli.py project focus MyProject
python rag_agent.py ingest --path /path/to/project
```

## 📖 Usage Guide

### Interactive Mode

Run the unified CLI without arguments for an interactive menu:

```bash
python contextkeeper_cli.py
# or
./contextkeeper
```

This replaces the old `./contextkeeper_manager.sh` script with a more intuitive interface.

### Command Structure

The new CLI organises commands into logical groups:

```bash
python contextkeeper_cli.py <group> <command> [options]
```

**Available groups**:
- `server` - Start/stop the RAG server
- `project` - Project management operations  
- `query` - Ask questions and search
- `sacred` - Sacred architecture layer
- `utils` - Utility functions

### Essential Commands

**Server Management**:
```bash
# Start server (replaces manual python rag_agent.py server)
python contextkeeper_cli.py server start
./contextkeeper start  # Quick alias

# Stop server
python contextkeeper_cli.py server stop  
./contextkeeper stop   # Quick alias

# Server status
python contextkeeper_cli.py server status
```

**Project Management**:
```bash
# List projects (replaces ./scripts/rag_cli_v2.sh projects list)
python contextkeeper_cli.py project list
./contextkeeper ls     # Quick alias

# Create project (replaces ./scripts/rag_cli_v2.sh projects create)
python contextkeeper_cli.py project create "ProjectName" /path/to/project

# Focus project (replaces ./scripts/rag_cli_v2.sh projects focus)
python contextkeeper_cli.py project focus <project_name_or_id>

# Delete project (replaces ./scripts/rag_cli_v2.sh projects delete)
python contextkeeper_cli.py project delete <project_name_or_id>

# Show project details
python contextkeeper_cli.py project info <project_name_or_id>
```

**Query Operations**:
```bash
# Ask questions (replaces ./scripts/rag_cli_v2.sh ask)
python contextkeeper_cli.py query ask "How does authentication work?"
./contextkeeper ask "How does authentication work?"  # Quick alias

# Search documents (replaces ./scripts/rag_cli_v2.sh search)
python contextkeeper_cli.py query search "database connection"

# List recent queries
python contextkeeper_cli.py query history
```

**Sacred Architecture Layer**:
```bash
# Check for architectural drift
python contextkeeper_cli.py sacred check-drift

# Submit architectural decision
python contextkeeper_cli.py sacred submit-decision "Use microservices architecture"

# List sacred decisions
python contextkeeper_cli.py sacred list-decisions
```

### Dashboard Access

After starting the server, access the live dashboard at:
- **Main Dashboard**: http://localhost:5556/dashboard
- **API Status**: http://localhost:5556/health
- **Project List**: http://localhost:5556/projects

## 🏗️ Architecture Overview

### System Components

```
User Request → CLI/MCP → RAG Agent → ChromaDB/LLM
                ↓           ↓           ↓
            Dashboard   Sacred Layer   Project Manager
```

1. **Unified CLI** (`contextkeeper_cli.py`): Single entry point replacing all shell scripts
2. **RAG Agent** (`rag_agent.py`): Flask API server with async endpoints
3. **Project Manager** (`project_manager.py`): Multi-project isolation
4. **Sacred Layer** (`sacred_layer_implementation.py`): Architectural governance
5. **MCP Server** (`mcp-server/`): Claude Code integration
6. **Dashboard** (`analytics_dashboard_live.html`): Real-time visualisation

### Data Flow

1. **Indexing**: Documents → Embeddings → ChromaDB Collections
2. **Querying**: User Question → Vector Search → LLM Reasoning → Response
3. **Sacred Layer**: Architectural Decisions → Immutable Storage → Drift Detection

## ⚙️ Configuration

### Environment Variables

```bash
GOOGLE_API_KEY=your_api_key          # Required: Gemini API access
SACRED_APPROVAL_KEY=your_key         # Required: Sacred layer operations
FLASK_ASYNC_MODE=True               # Performance: Enable async endpoints
DEBUG=0                             # Production: Disable debug mode
CHROMA_PERSIST_DIRECTORY=./chroma_db # Database location
```

### Project Structure

```
contextkeeper/
├── contextkeeper_cli.py          # NEW: Unified CLI (replaces all scripts)
├── rag_agent.py                  # Core RAG server
├── project_manager.py            # Project isolation
├── sacred_layer_implementation.py # Architectural governance
├── mcp-server/                   # MCP integration
│   ├── package.json
│   └── enhanced_mcp_server.js
├── projects/                     # Project storage
├── chroma_db/                    # Vector database
└── tests/                        # Test suite
```

### Legacy Scripts (Deprecated)

The following scripts have been replaced by the unified CLI:

- ~~`./quick_start.sh`~~ → `python contextkeeper_cli.py project create --auto-index`
- ~~`./contextkeeper_manager.sh`~~ → `python contextkeeper_cli.py` (interactive)
- ~~`./contextkeeper_simple.sh`~~ → `python contextkeeper_cli.py` (interactive)
- ~~`./scripts/rag_cli_v2.sh`~~ → `python contextkeeper_cli.py <group> <command>`

## 🧪 Testing

### Running Tests

```bash
# Full test suite
pytest tests/ -v --tb=short

# Specific test categories
pytest tests/sacred/ -v           # Sacred layer tests
pytest tests/api/ -v -k "test_query"  # API tests
pytest tests/drift/ -v            # Drift detection tests
```

### Test Environment Setup

```bash
# Clean test environment
python contextkeeper_cli.py utils cleanup --force
./cleanup_all.sh  # Legacy cleanup script
```

## 🔧 Development

### Adding New Features

1. **CLI Commands**: Add to `contextkeeper_cli.py` command groups
2. **API Endpoints**: Add to `rag_agent.py` with async support
3. **Sacred Operations**: Extend `sacred_layer_implementation.py`
4. **Tests**: Add comprehensive test coverage

### Code Style

- Australian English spelling (colour, behaviour, realise)
- Conversational comments for clarity
- Update `LOGBOOK.md` for significant changes
- Format: `[YYYY-MM-DD HH:MM AEST] - [Component] - [Action] - [Details]`

### Performance Considerations

- Each project uses ~100MB for ChromaDB collection
- Dashboard animation optimised for 4000 particles
- Query latency target: <500ms
- Indexing speed: ~1000 files/minute

## 🚨 Common Issues

### Server Won't Start
```bash
# Check if port is in use
python contextkeeper_cli.py server status

# Force cleanup and restart
python contextkeeper_cli.py utils cleanup --force
python contextkeeper_cli.py server start
```

### Poor Query Results
```bash
# Ensure project is focused and indexed
python contextkeeper_cli.py project focus <project_id>
python rag_agent.py ingest --path /project/path
```

### "Project not found" Error
```bash
# List available projects
python contextkeeper_cli.py project list

# Recreate project if necessary
python contextkeeper_cli.py project create "ProjectName" /path/to/project --auto-index
```

## 📊 API Reference

### REST Endpoints

- `GET /health` - Server health check
- `GET /projects` - List all projects
- `POST /query` - Ask questions with context
- `POST /projects` - Create new project
- `POST /ingest` - Index documents
- `GET /sacred/decisions` - List architectural decisions
- `POST /sacred/check-drift` - Check for architectural drift

### MCP Tools

Available via Claude Code MCP integration:

- `contextkeeper_query` - Ask questions with project context
- `contextkeeper_list_projects` - Get available projects
- `sacred_check_drift` - Detect architectural inconsistencies
- `contextkeeper_create_project` - Create and setup new projects

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest tests/ -v`)
4. Update documentation if needed
5. Commit changes (`git commit -m 'feat: Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **ChromaDB**: Vector database foundation
- **Google Gemini**: AI reasoning capabilities
- **Three.js**: Beautiful dashboard visualisations
- **Flask**: Reliable API framework
- **Claude Code**: Development assistant integration

---

**Note**: This version introduces a unified CLI that replaces all previous shell scripts. The old scripts are maintained for compatibility but the new CLI is the recommended approach for all operations.

For detailed logs and development history, see `LOGBOOK.md`.