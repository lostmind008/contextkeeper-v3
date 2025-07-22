# Changelog

All notable changes to the RAG Knowledge Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-07-22

### Added
- Multi-project support with ProjectManager class
- Project lifecycle management (create, pause, resume, archive, focus)
- Decision tracking system for architectural choices
- Objective tracking with completion status
- Context export functionality for AI agents
- Git-based activity tracking (replacing terminal monitoring concept)
- Project configuration persistence
- Enhanced CLI commands for project management
- Comprehensive project status and briefing commands

### Changed
- Migrated from hardcoded watch directories to dynamic project-based configuration
- Enhanced RAG agent to support multiple concurrent projects
- Updated CLI interface with project-aware commands
- Improved documentation to reflect multi-project capabilities

### Removed
- Hardcoded YouTube Analyzer project paths
- Single-project limitation

### Security
- All sensitive data filtering remains intact
- Project isolation ensures no cross-project data leakage

## [1.0.0] - 2025-07-01

### Initial Release
- ChromaDB vector storage for code knowledge
- Google GenAI embeddings integration
- Watchdog-based file monitoring
- Security filter for sensitive data
- Intelligent code chunking
- Flask API server
- CLI interface for queries
- YouTube Analyzer project integration