# CLAUDE.md - Utility Scripts & Fixes

This file provides context for Claude Code when working with utility scripts.

## Directory Purpose
Contains one-time fixes, patches, debugging utilities, and maintenance scripts. These scripts were critical during development but are now archived here for reference and potential reuse.

## Script Categories

### Fix Scripts (fix*.py, apply*.py)
- Various patches for isolation issues
- Project indexing fixes
- API response improvements
- Method addition patches

### Debug Scripts (debug*.py)
- Isolation debugging tools
- Project content inspection
- Performance diagnostics

### Test Scripts (moved to ../tests/)
- All test_*.py files relocated
- Run_*.py test runners moved

### Utility Scripts
- add_analytics_endpoint.py - Analytics setup
- patch_rag_agent.py - Agent patching
- comprehensive_project_fix.py - Major fixes

## Usage Notes
- These scripts are historical artifacts
- Most functionality now integrated into core
- Keep for reference and emergency fixes
- New utilities should have governance headers

## Common Patterns
```python
# Most scripts follow this pattern:
1. Import rag_agent components
2. Apply specific fix or patch
3. Verify the change
4. Log the result
```

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/src/
- Core System: ../core/rag_agent.py
- Shell Scripts: ../../scripts/