# CLAUDE.md - Core System Components

This file provides context for Claude Code when working with core system components.

## Directory Purpose
Contains the foundational components of ContextKeeper that orchestrate all system operations. These files form the backbone of the RAG agent and project management system.

## Key Files
- **`rag_agent.py`** (2022 lines) - Main orchestrator with Flask API server
  - Manages ChromaDB collections and embeddings
  - Provides all API endpoints for system operations
  - Handles LLM queries and response generation

- **`project_manager.py`** (503 lines) - Multi-project state management
  - Manages project lifecycle (create, focus, archive)
  - Tracks decisions, objectives, and events
  - Persists state to filesystem

## Architectural Context
These components implement the core architectural decisions:
- Project isolation via separate ChromaDB collections
- Event-driven architecture for real-time tracking
- Sacred layer integration for governance
- Git-aware context management

## Dependencies
- **External**: flask, chromadb, google.generativeai
- **Internal**: sacred_layer_implementation, git_activity_tracker
- **Data**: projects/ directory, rag_knowledge_db/

## Common Issues
- Server must use `python rag_agent.py server` (not 'start')
- Collections dictionary may need manual refresh
- Project focus state affects query quality

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/src/
- Sacred Layer: ../sacred/sacred_layer_implementation.py
  - Analytics: ../ck_analytics/analytics_integration.py
