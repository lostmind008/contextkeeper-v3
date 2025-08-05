# CLAUDE.md - Scripts

This file provides context for Claude Code when working in this directory.

## Directory Purpose
Contains automation scripts and CLI tools for ContextKeeper v3 operations, including project management, sacred layer operations, and system administration tasks.

## Key Files
- **rag_cli_v2.sh** - Primary CLI interface for project management and queries
- **rag_cli.sh** - Legacy CLI (deprecated, use v2)
- **start_system.sh** - System startup automation
- **backup_sacred.sh** - Sacred layer backup operations
- **maintenance.sh** - System maintenance tasks

## Dependencies
- **From parent**: RAG Agent accessible, ChromaDB running, Sacred Layer operational
- **External**: bash shell, curl for API calls, jq for JSON processing
- **Permissions**: Execute permissions on shell scripts

## Common Tasks
- Create project: `./rag_cli_v2.sh projects create "Name" /path/to/project`
- Focus project: `./rag_cli_v2.sh projects focus <project_id>`
- Query knowledge: `./rag_cli_v2.sh ask "question" --project <project_id>`
- Sacred operations: `./rag_cli_v2.sh sacred create|approve|drift`
- System startup: `./start_system.sh`

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/
- Related: Main RAG agent (../rag_agent.py), Sacred Layer (../sacred_layer_implementation.py), Tests (../tests/)