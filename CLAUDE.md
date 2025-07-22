# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an enhanced Multi-Project RAG (Retrieval-Augmented Generation) Knowledge Agent that maintains persistent knowledge across multiple concurrent projects and coding sessions. It dynamically watches project directories, tracks decisions and objectives, indexes code files, and provides a searchable knowledge base with automatic security filtering, intelligent code chunking, and rich context export for AI assistants.

### Version 2.0 Features
- **Multi-project support**: Track multiple projects simultaneously with independent configurations
- **Project lifecycle management**: Create, pause, resume, archive, and focus on projects
- **Decision tracking**: Record and retrieve architectural decisions with reasoning
- **Objective tracking**: Set and monitor development goals with completion status
- **Context export**: Generate rich context for AI assistants (Claude Code, GitHub Copilot, etc.)
- **Git integration**: Track development activity through git commits and changes
- **Project isolation**: Each project maintains its own knowledge base and configuration

## Key Commands

### Project Management Commands (v2.0)
```bash
# Project lifecycle
./rag_cli.sh projects create "Project Name" /path/to/project
./rag_cli.sh projects list                     # List all projects
./rag_cli.sh projects focus proj_id            # Set active project
./rag_cli.sh projects pause proj_id            # Pause project tracking
./rag_cli.sh projects resume proj_id           # Resume project tracking
./rag_cli.sh projects archive proj_id          # Archive completed project

# Decision & objective tracking
./rag_cli.sh decisions add "Using Redis for caching" "Better performance than in-memory"
./rag_cli.sh objectives add "Implement user authentication"
./rag_cli.sh objectives list                   # Show current objectives
./rag_cli.sh objectives complete 1             # Mark objective as complete

# Context & briefing
./rag_cli.sh context export                    # Export context for AI agents
./rag_cli.sh briefing                          # Get comprehensive project status
./rag_cli.sh activity                          # Show recent project activity
```

### Core Commands
```bash
# Initial setup
./setup.sh                              # One-time setup script

# Run the agent
python rag_agent.py start               # Start the RAG agent server
./rag_cli.sh start                      # Alternative using CLI wrapper

# Query knowledge base (project-aware)
./rag_cli.sh ask "What authentication system did I use?"
python rag_agent.py query --project proj_id --question "Show integration code"

# Legacy commands (for backward compatibility)
./rag_cli.sh status                    # Check if agent is running
./rag_cli.sh logs                      # View agent logs
```

### Testing & Development
```bash
# Test API endpoints
curl -X POST http://localhost:5555/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show recent changes"}'

# Check health
curl http://localhost:5555/health
```

## Architecture & Core Components

### 1. **rag_agent.py** - Enhanced Multi-Project Application
- **ProjectManager**: Manages multiple project sessions with independent configurations
- **ChromaDB Integration**: Separate collections per project for isolation
- **Google GenAI SDK**: Embeddings via text-embedding-004 model
- **Dynamic File Watching**: Monitors project-specific directories using watchdog
- **Security Filter**: Automatically redacts API keys and sensitive data
- **Text Chunker**: Intelligent chunking preserving code structure
- **Decision & Objective Tracking**: Persistent storage of project decisions and goals
- **Context Export**: Rich context generation for AI assistants
- **Flask API**: RESTful endpoints on port 5555 with project-aware routing

### 2. **project_manager.py** - Project Lifecycle Management
- Project creation with configurable watch directories
- State management (active, paused, archived, focused)
- Decision and objective tracking per project
- Git integration for activity tracking
- Configuration persistence to disk

### 3. **rag_cli.sh** - Enhanced CLI Wrapper
- Full project management commands
- Decision and objective tracking interface
- Context export for AI agents
- Project-aware queries and operations
- Backward compatibility with v1.0 commands

### 4. **Configuration Structure**
- **Global Configuration**: `.env` file for Google Cloud credentials
- **Project Configuration**: `~/.rag_projects/` directory for project configs
- **Project Metadata**: JSON files storing project state, decisions, objectives
- **Dynamic Watch Directories**: Per-project configurable paths
- **Supported file types**: .py, .js, .jsx, .ts, .tsx, .md, .json, .yaml

## Key Architecture Patterns

### Embedding & Storage Flow
1. File changes detected by watchdog → 
2. Content passes through SecurityFilter → 
3. TextChunker creates semantic chunks → 
4. Google GenAI creates embeddings → 
5. ChromaDB stores vectors with metadata

### Query Processing
1. User question → 
2. Embedded via same model → 
3. ChromaDB similarity search → 
4. Top k results returned with metadata

### Security Considerations
- Automatic redaction of API keys, passwords, secrets, tokens
- Patterns defined in CONFIG['sensitive_patterns']
- Applied before any embedding or storage

## Environment Setup Requirements

1. **Google Cloud Configuration** (required):
   - Valid Google Cloud project with Vertex AI enabled
   - Service account JSON with appropriate permissions
   - Environment variables set in `.env` file

2. **Python Dependencies** (installed via requirements.txt):
   - google-genai: Google's unified GenAI SDK
   - chromadb: Vector database
   - tiktoken: Token counting for chunking
   - watchdog: File system monitoring
   - flask & flask-cors: API server

## Important Context

- The agent maintains knowledge across sessions by indexing watched directories
- All queries preserve code structure and context through intelligent chunking
- Designed specifically for the YouTube Analyzer project but adaptable
- Runs as a persistent background service on port 5555
- Logs to `rag_agent.log` for debugging

## Common Troubleshooting

- **Agent not starting**: Check Google Cloud credentials in `.env`
- **No results**: Ensure watch directories exist and contain supported file types
- **Import errors**: Activate virtual environment: `source venv/bin/activate`
- **Permission errors**: Make scripts executable: `chmod +x rag_cli.sh setup.sh`