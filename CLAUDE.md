# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval-Augmented Generation) Knowledge Agent that maintains persistent knowledge across coding sessions. It watches project directories, indexes code files, and provides a searchable knowledge base with automatic security filtering and intelligent code chunking.

## Key Commands

### Development Commands
```bash
# Initial setup
./setup.sh                              # One-time setup script

# Run the agent
python rag_agent.py start               # Start the RAG agent server
./rag_cli.sh start                      # Alternative using CLI wrapper

# Query knowledge base
./rag_cli.sh ask "What authentication system did I use?"
python rag_agent.py query --question "Show Gemini integration code"

# Add project decisions
./rag_cli.sh add "Using CrewAI for multi-agent system"

# Useful queries
./rag_cli.sh morning                    # Get morning briefing
./rag_cli.sh youtube gemini            # Show Gemini integration
./rag_cli.sh youtube agents            # List all agents
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

### 1. **rag_agent.py** - Main Application
- **ChromaDB Integration**: Uses ChromaDB for vector storage and similarity search
- **Google GenAI SDK**: Embeddings via text-embedding-004 model
- **File Watching**: Monitors directories using watchdog library
- **Security Filter**: Automatically redacts API keys and sensitive data
- **Text Chunker**: Intelligent chunking preserving code structure
- **Flask API**: RESTful endpoints on port 5555 with CORS support

### 2. **rag_cli.sh** - CLI Wrapper
- Bash script providing simplified commands
- Auto-starts the agent if not running
- Handles both interactive and quick queries
- Special YouTube Analyzer project shortcuts

### 3. **youtube_analyzer_integration.py** - Integration Examples
- Helper class for project-specific queries
- Code extraction utilities
- Claude prompt generation with RAG context
- Architecture decision recording

### 4. **Configuration Structure**
- Uses `.env` file for Google Cloud credentials
- Configurable via CONFIG dict in rag_agent.py
- Default watched directories: ["./youtube-analyzer-app", "./backend", "./frontend"]
- Supported file types: .py, .js, .jsx, .ts, .tsx, .md, .json, .yaml

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