# CLAUDE.md - Scripts (DEPRECATED)

This file provides context for Claude Code when working in this directory.

## ⚠️ IMPORTANT: These scripts are DEPRECATED
**All functionality has been migrated to the unified Python CLI:**
- **NEW**: `python ../contextkeeper_cli.py` (or `../contextkeeper`)
- **Interactive menu**: Run without arguments
- **Help**: `python ../contextkeeper_cli.py --help`

## Directory Purpose (Historical)
Contains legacy automation scripts that have been replaced by the unified CLI.

## Migration Guide
### Old Script → New CLI Command
- `./rag_cli_v2.sh projects create` → `python ../contextkeeper_cli.py project create`
- `./rag_cli_v2.sh projects focus` → `python ../contextkeeper_cli.py project focus`
- `./rag_cli_v2.sh ask` → `python ../contextkeeper_cli.py query ask`
- `./rag_cli_v2.sh sacred` → `python ../contextkeeper_cli.py sacred`
- `./contextkeeper_simple.sh` → `python ../contextkeeper_cli.py` (interactive)
- `./contextkeeper_manager.sh` → `python ../contextkeeper_cli.py` (interactive)

## Key Files (Legacy)
- **rag_cli_v2.sh** - DEPRECATED: Use `contextkeeper_cli.py`
- **contextkeeper.sh** - DEPRECATED: Use `contextkeeper_cli.py`
- **contextkeeper_simple.sh** - DEPRECATED: Use `contextkeeper_cli.py`
- **sacred_cli_integration.sh** - DEPRECATED: Use `contextkeeper_cli.py sacred`

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/
- New CLI: ../contextkeeper_cli.py
- Related: Main RAG agent (../src/core/rag_agent.py), Sacred Layer (../src/sacred/)