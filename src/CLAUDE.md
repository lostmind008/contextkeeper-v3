# CLAUDE.md - Source Code Directory

This file provides context for Claude Code when working in the src/ directory structure.

## Directory Purpose
Contains all Python source code organized by functional domain following governance protocols. This structure prevents code sprawl and maintains clear separation of concerns.

## Directory Structure
```
src/
├── core/           # Core system components (project_manager)
├── sacred/         # Sacred layer implementation and drift detection
├── analytics/      # Analytics integration and dashboards
├── tracking/       # Event and git activity tracking
├── scripts/        # Utility scripts, fixes, and patches
└── utils/          # Shared utilities and helpers
```

## Key Principles
- Each subdirectory has specific functional responsibility
- Core system files have comprehensive governance headers
- All imports use relative paths within src/
- Scripts directory contains one-time fixes and utilities

## Dependencies
- Python 3.8+ with type hints
- External: flask, chromadb, google.genai
- Internal: Cross-module imports via relative paths

## Common Tasks
- Add new features in appropriate subdirectory
- Include governance headers for files > 100 lines
- Update imports when moving files
- Document architectural decisions in headers

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/
- Core components: ./core/rag_agent.py, ./core/project_manager.py
- Sacred governance: ./sacred/sacred_layer_implementation.py