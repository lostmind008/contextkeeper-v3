# ContextKeeper v3 Overview

ContextKeeper is a multi-project RAG (Retrieval Augmented Generation) knowledge agent that maintains persistent knowledge across coding sessions.

## Key Features

- **Sacred Layer**: Architectural constraint enforcement with two-layer verification
- **Multi-Project Support**: Manages multiple projects with isolated knowledge bases
- **Git Integration**: Tracks development activity and commit history  
- **MCP Server**: Provides tools for AI assistants like Claude Code
- **Path Filtering**: Intelligently excludes unnecessary files (venv, node_modules, etc.)

## Architecture

ContextKeeper uses ChromaDB for vector storage with Google GenAI embeddings (gemini-embedding-001). The Sacred Layer provides immutable architectural plans that act as guardrails for development decisions.

## Current Status

As of July 2025, ContextKeeper v3 is fully operational with all infrastructure fixes completed:
- Sacred Layer endpoints working (no more 500 errors)
- CLI interface functional with rag_cli_v2.sh
- API running on port 5556
- Google GenAI API compatibility resolved