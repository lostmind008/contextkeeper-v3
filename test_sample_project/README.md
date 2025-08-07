# Test Sample Project

This is a test project to verify ContextKeeper's file indexing capabilities.

## Features
- Source code in Python
- Documentation files
- Configuration files
- Virtual environments (should be ignored)
- Package manager files (should be ignored)

## Project Structure
```
test_sample_project/
├── src/              # Source code
├── docs/             # Documentation
├── tests/            # Test files
├── venv/             # Virtual environment (SHOULD BE IGNORED)
├── myvenv/           # Another venv (SHOULD BE IGNORED)
├── node_modules/     # Node packages (SHOULD BE IGNORED)
├── __pycache__/      # Python cache (SHOULD BE IGNORED)
└── .git/             # Git repository (SHOULD BE IGNORED)
```

## Testing Focus
This project tests whether ContextKeeper correctly:
1. Indexes relevant source files
2. Ignores virtual environments
3. Ignores package manager directories
4. Handles various file formats