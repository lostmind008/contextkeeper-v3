# Migration Guide: RAG Agent v1.0 to v2.0

## Overview

RAG Agent v2.0 introduces multi-project support while maintaining full backward compatibility. Your existing setup will continue to work, and your YouTube Analyzer project will be automatically imported.

## What's New in v2.0

### Major Features
- **Multi-Project Support**: Track multiple projects simultaneously
- **Project Lifecycle Management**: Pause, resume, and archive projects
- **Decision Tracking**: Record architectural decisions with reasoning
- **Objective Management**: Set and track development goals
- **Context Export**: Generate rich context for AI assistants
- **Project Isolation**: Each project has its own vector storage

### Backward Compatibility
- Your existing YouTube Analyzer configuration will be automatically imported as a project
- All v1.0 commands continue to work
- The API remains compatible with existing integrations

## Quick Start

### 1. First Run
When you first run v2.0, it will:
```bash
# Start the agent (it will auto-import your YouTube Analyzer project)
./rag_cli.sh start

# Check your projects
./rag_cli.sh projects list
```

### 2. Create Additional Projects
```bash
# Create a new project
./rag_cli.sh projects create "My New Project" /path/to/project

# Focus on the new project
./rag_cli.sh projects focus proj_<id>
```

### 3. Use Enhanced Features
```bash
# Add a decision to the current project
./rag_cli.sh decisions add "Using Redis for caching" "Better performance than in-memory"

# Add an objective
./rag_cli.sh objectives add "Implement user authentication"

# Get project context for AI assistants
./rag_cli.sh context export
```

## Command Changes

### Legacy Commands (Still Work)
```bash
./rag_cli.sh ask "What authentication system did I use?"
./rag_cli.sh add "Using CrewAI for multi-agent system"
./rag_cli.sh morning
```

### New v2.0 Commands
```bash
# Project management
./rag_cli.sh projects create|list|focus|pause|resume|archive

# Decision tracking
./rag_cli.sh decisions add "decision" "reasoning" "tags"

# Objective tracking
./rag_cli.sh objectives add|complete|list

# Context export
./rag_cli.sh context export
./rag_cli.sh briefing
```

## API Changes

### Query Endpoint
Now supports optional project filtering:
```bash
# Query specific project
curl -X POST http://localhost:5555/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show auth code", "project_id": "proj_abc123"}'
```

### New Endpoints
```bash
# Project management
GET  /projects                    # List all projects
POST /projects                    # Create project
POST /projects/<id>/focus         # Focus project
PUT  /projects/<id>/status        # Update status
GET  /projects/<id>/context       # Export context

# Objectives
POST /projects/<id>/objectives    # Add objective
POST /projects/<id>/objectives/<oid>/complete
```

## Data Migration

### Automatic Migration
- Your existing ChromaDB collection is preserved
- A new project-specific collection is created for the imported YouTube Analyzer project
- Future ingestions will use the project-specific collection

### Manual Migration (Optional)
If you want to fully migrate old data to the new structure:
```bash
# Re-ingest your project files
./rag_cli.sh projects focus proj_<youtube_id>
python rag_agent.py ingest --path "/path/to/youtube-analyzer"
```

## Configuration Files

### New Configuration Location
Project configurations are now stored in:
```
~/.rag_projects/
├── proj_<id1>.json
├── proj_<id2>.json
└── ...
```

### Legacy Configuration
The old configuration in `rag_agent.py` is used only for initial import.

## Breaking Changes

None! v2.0 is fully backward compatible.

## Troubleshooting

### Agent Won't Start
```bash
# Check logs
tail -f ~/rag-agent/rag_agent.log

# Ensure virtual environment is activated
source ~/rag-agent/venv/bin/activate
```

### Projects Not Showing
```bash
# Check project directory
ls ~/.rag_projects/

# Restart agent
./rag_cli.sh restart
```

### Import Issues
If your YouTube Analyzer project wasn't imported:
1. Check that the directories exist
2. Manually create the project:
```bash
./rag_cli.sh projects create "YouTube Analyzer" "/path/to/project"
```

## Best Practices

1. **One Project Per Repository**: Create a project for each git repository
2. **Use Descriptive Names**: "YouTube Analyzer" instead of "project1"
3. **Set Objectives**: Track what you're working on
4. **Record Decisions**: Document architectural choices with reasoning
5. **Regular Context Export**: Use for AI pair programming

## Need Help?

- Check the updated [README.md](README.md)
- Review the [CHANGELOG.md](CHANGELOG.md)
- Examine the API documentation in the code

Welcome to RAG Agent v2.0! 🎉