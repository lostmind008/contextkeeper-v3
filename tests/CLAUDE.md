# CLAUDE.md - Tests

This file provides context for Claude Code when working in this directory.

## Directory Purpose
Contains comprehensive test suites for ContextKeeper v3, including unit tests, integration tests, and sacred layer verification tests. Ensures system reliability and architectural compliance.

## Key Files
- **sacred/** - Sacred layer architectural tests and compliance checks
- **api/** - Flask API endpoint tests and validation
- **integration/** - End-to-end system integration tests
- **test_multiproject.py** - Multi-project isolation and management tests
- **conftest.py** - PyTest configuration and shared fixtures

## Dependencies
- **From parent**: RAG Agent running, ChromaDB accessible, Sacred Layer operational
- **External**: pytest, requests library, test data fixtures
- **Environment**: Test ChromaDB collections, isolated test environment

## Common Tasks
- Run all tests: `pytest tests/ -v`
- Run sacred tests: `pytest tests/sacred/ -v`
- Run API tests: `pytest tests/api/ -v`
- Run integration tests: `pytest tests/integration/ -v`
- Individual test: `python tests/sacred/test_sacred_layer.py`

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/
- Related: Main RAG agent (../rag_agent.py), Sacred Layer (../sacred_layer_implementation.py), Scripts (../scripts/)