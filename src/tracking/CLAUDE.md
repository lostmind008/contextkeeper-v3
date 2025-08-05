# CLAUDE.md - Event & Activity Tracking

This file provides context for Claude Code when working with tracking components.

## Directory Purpose
Contains modules for tracking development activities, git commits, and real-time events. Provides temporal context for the RAG system to understand project evolution.

## Key Files
- **`git_activity_tracker.py`** - Git repository monitoring
  - Tracks commits, branches, and changes
  - Analyzes uncommitted modifications
  - Provides git context for queries
  - Integrates with project timeline

## Tracking Features
- Real-time development event capture
- Git commit history analysis
- Branch activity monitoring
- Uncommitted change detection
- Temporal weighting for retrieval

## Event Types Tracked
- Code changes and commits
- Build and test results
- Deployment activities
- Errors and exceptions
- Architectural decisions
- Performance metrics

## Dependencies
- **External**: gitpython (if used), subprocess
- **Internal**: project_manager for event storage
- **Git**: Repository access and monitoring

## Common Tasks
- Add new event types
- Enhance git integration
- Improve temporal analysis
- Add activity aggregation

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/src/
- Event Storage: ../core/project_manager.py
- Analytics: ../analytics/analytics_integration.py