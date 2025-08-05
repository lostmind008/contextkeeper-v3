# CLAUDE.md - Analytics Integration

This file provides context for Claude Code when working with analytics components.

## Directory Purpose
Contains analytics integration modules that provide real-time metrics, visualization data, and project insights for the dashboard and reporting systems.

## Key Files
- **`analytics_integration.py`** - Analytics data aggregation
  - Project metrics calculation
  - Event aggregation and summarization
  - Time-series data preparation
  - Dashboard API endpoints

## Analytics Features
- Real-time project activity metrics
- Code change frequency analysis
- Decision and objective tracking
- Event severity distribution
- Sacred plan adherence scores

## Data Flow
```
Events/Decisions → Analytics Engine → Aggregation → Dashboard API → Three.js Visualization
```

## Dependencies
- **External**: numpy, pandas (if used)
- **Internal**: project_manager for state data
- **Frontend**: analytics_dashboard_live.html

## Common Tasks
- Add new metric calculations
- Optimize aggregation performance
- Enhance time-series analysis
- Add export capabilities

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/src/
- Dashboard: ../../analytics_dashboard_live.html
- Core Integration: ../core/rag_agent.py