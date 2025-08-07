# ContextKeeper v3.0 User Guide

**Complete guide to using ContextKeeper v3.0 with multi-project support, sacred architectural governance, and real-time analytics.**

## Table of Contents

- [🚀 Quick Start](#-quick-start)
- [📋 Core Workflows](#-core-workflows)
- [📝 CLI Command Reference](#-cli-command-reference)
- [🎯 Sacred Layer (Architectural Governance)](#-sacred-layer-architectural-governance)
- [📊 Analytics Dashboard](#-analytics-dashboard)
- [🔌 API Quick Reference](#-api-quick-reference)
- [🔧 Troubleshooting](#-troubleshooting)
- [💡 Best Practices](#-best-practices)
- [🆘 Getting Help](#-getting-help)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Cloud API key (for embeddings and AI features)
- 4GB+ RAM recommended
- 2GB+ disk space

### Install & First Run (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/lostmind008/contextkeeper-v3.git
cd contextkeeper

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.template .env
# Edit .env and add your keys:
# GOOGLE_API_KEY=your-api-key-here
# SACRED_APPROVAL_KEY=your-secret-key

# 5. Start ContextKeeper
python rag_agent.py server  # Use 'server', not 'start'

# 6. Verify installation
curl http://localhost:5556/health
# Should return: {"status":"healthy"}
```

### Your First Project

```bash
# Create a project
python contextkeeper_cli.py projects create "My Project" /path/to/your/code

# Or use the shorthand:
./contextkeeper projects create "My Project" /path/to/your/code

# List all projects
python contextkeeper_cli.py projects list

# Focus on your project (makes it the default)
python contextkeeper_cli.py projects focus <project_id>
```

### Your First Query

```bash
# Ask a question about your code
python contextkeeper_cli.py ask "How does the authentication work?"

# Get an AI-enhanced response
python contextkeeper_cli.py ask "Explain the database schema" --llm

# Interactive mode
python contextkeeper_cli.py chat
```

### Access the Dashboard

Open your browser and go to: `http://localhost:5556/dashboard`

The dashboard provides:
- Real-time project metrics with 3D visualisation
- Interactive chat interface
- Sacred plan monitoring
- Project health analytics

## 📋 Core Workflows

### Managing Projects

**Create a New Project**
```bash
# Basic creation
python contextkeeper_cli.py projects create "E-commerce API" /path/to/project

# With description
python contextkeeper_cli.py projects create "Mobile App" /path/to/app "React Native customer app"
```

**List and Focus Projects**
```bash
# List all projects
python contextkeeper_cli.py projects list

# Focus on a project (sets it as default)
python contextkeeper_cli.py projects focus <project_id>

# Show project details
python contextkeeper_cli.py projects show <project_id>
```

**Project Status and Updates**
```bash
# Get project status
python contextkeeper_cli.py projects status <project_id>

# Update project index
python contextkeeper_cli.py projects update <project_id>

# Archive project
python contextkeeper_cli.py projects archive <project_id>
```

### Ingesting Code & Documents

ContextKeeper automatically indexes your code when you create a project, but you can also:

```bash
# Index a specific file
python contextkeeper_cli.py ingest /path/to/file.py

# Index a directory
python contextkeeper_cli.py ingest /path/to/directory

# Re-index current project
python contextkeeper_cli.py projects update
```

**Supported Files:**
- Source code: `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.go`, `.rs`, etc.
- Documentation: `.md`, `.txt`, `.rst`
- Configuration: `.json`, `.yaml`, `.toml`
- Web: `.html`, `.css`

### Running Queries

**Basic Queries**
```bash
# Simple question
python contextkeeper_cli.py ask "What does the UserService class do?"

# Find specific patterns
python contextkeeper_cli.py ask "Find all API endpoints"

# Get more results
python contextkeeper_cli.py ask "Show database models" --top-k 10
```

**AI-Enhanced Queries**
```bash
# Get AI explanations and suggestions
python contextkeeper_cli.py ask "How can I add user authentication?" --llm

# Complex analysis
python contextkeeper_cli.py ask "Analyse the security vulnerabilities" --llm

# Code generation help
python contextkeeper_cli.py ask "Generate unit tests for AuthService" --llm
```

**Interactive Chat Mode**
```bash
# Start interactive session
python contextkeeper_cli.py chat

# Commands within chat:
# /help - Show chat commands
# /focus <project_id> - Switch project
# /sacred - Sacred layer commands
# /export - Export conversation
# /quit - Exit chat
```

## 📝 CLI Command Reference

### Project Commands

```bash
# Project Management
python contextkeeper_cli.py projects create <name> <path> [description]
python contextkeeper_cli.py projects list
python contextkeeper_cli.py projects focus <project_id>
python contextkeeper_cli.py projects show <project_id>
python contextkeeper_cli.py projects status <project_id>
python contextkeeper_cli.py projects update <project_id>
python contextkeeper_cli.py projects archive <project_id>
python contextkeeper_cli.py projects remove <project_id>
```

### Query Commands

```bash
# Basic Queries
python contextkeeper_cli.py ask "your question"
python contextkeeper_cli.py ask "question" --top-k 10
python contextkeeper_cli.py ask "question" --project <project_id>

# AI-Enhanced Queries
python contextkeeper_cli.py ask "question" --llm
python contextkeeper_cli.py ask "question" --llm --model gemini-pro
```

### Sacred Layer Commands

```bash
# Sacred Plan Management
python contextkeeper_cli.py sacred create <project_id> "Plan Title" plan.md
python contextkeeper_cli.py sacred list [project_id]
python contextkeeper_cli.py sacred approve <plan_id>
python contextkeeper_cli.py sacred drift <project_id>
python contextkeeper_cli.py sacred query <project_id> "architecture question"
```

### Decision & Objective Commands

```bash
# Track Decisions
python contextkeeper_cli.py decision add "Decision title" "Reasoning" "tag1,tag2"
python contextkeeper_cli.py decision list

# Manage Objectives
python contextkeeper_cli.py objective add <project_id> "Objective" "Description" high
python contextkeeper_cli.py objective complete <project_id> <objective_id>
python contextkeeper_cli.py objective list [project_id]
```

### Utility Commands

```bash
# Health and Status
python contextkeeper_cli.py health
python contextkeeper_cli.py version

# Export and Backup
python contextkeeper_cli.py export [project_id]
python contextkeeper_cli.py backup
```

## 🎯 Sacred Layer (Architectural Governance)

The Sacred Layer provides architectural governance through immutable plans and drift detection.

### Core Concepts

**Sacred Plans** are architectural decisions that:
- Cannot be changed once approved (immutable)
- Require two-factor approval
- Are automatically monitored for drift
- Guide development decisions

### Creating Sacred Plans

1. **Write a plan file** (example: `auth_plan.md`):
```markdown
# Authentication Architecture

## Overview
OAuth2 + JWT implementation with Redis session storage.

## Components
- AuthService: Handles authentication logic
- TokenService: JWT token management
- UserRepository: User data persistence

## Constraints
- All passwords must be hashed with bcrypt
- JWT tokens expire after 1 hour
- Redis used for session management only
```

2. **Submit the plan**:
```bash
python contextkeeper_cli.py sacred create proj_123 "OAuth2 Authentication" auth_plan.md
```

3. **Approve the plan**:
```bash
# Get the plan ID from creation output, then:
python contextkeeper_cli.py sacred approve <plan_id>
# Enter verification code when prompted
# Enter SACRED_APPROVAL_KEY from your .env
```

### Monitoring and Drift Detection

```bash
# Check for architectural drift
python contextkeeper_cli.py sacred drift <project_id>

# Query sacred plans
python contextkeeper_cli.py sacred query <project_id> "How should authentication work?"

# List all sacred plans
python contextkeeper_cli.py sacred list <project_id>
```

### Sacred Plan Workflow

1. **Create** → Write plan file and submit
2. **Review** → Team reviews the architectural decision
3. **Approve** → Two-factor approval makes it immutable
4. **Monitor** → Automatic drift detection during development
5. **Query** → Reference during development decisions

## 📊 Analytics Dashboard

Access the dashboard at: `http://localhost:5556/dashboard`

### Features

**Real-time Metrics**
- Active projects count
- Query volume and response times
- Sacred plan compliance
- Code coverage analysis

**3D Visualisation**
- Interactive particle system (4000+ particles)
- Project relationships mapping
- Code complexity visualisation
- Architecture drift indicators

**Interactive Chat**
- Built-in chat interface
- Context-aware responses
- Sacred layer integration
- Export conversations

### Performance Considerations

- Dashboard may lag on older devices due to 3D animations
- Disable animations in settings if needed
- Use mobile-optimised view on smaller screens

## 🔌 API Quick Reference

### Health Check
```bash
curl http://localhost:5556/health
# Response: {"status":"healthy"}
```

### Projects
```bash
# List all projects
curl http://localhost:5556/projects

# Create project
curl -X POST http://localhost:5556/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"My Project","path":"/path/to/code"}'
```

### Queries
```bash
# Basic query
curl -X POST http://localhost:5556/query \
  -H "Content-Type: application/json" \
  -d '{"question":"How does auth work?","project_id":"proj_123"}'

# AI-enhanced query
curl -X POST http://localhost:5556/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Explain auth","use_llm":true,"project_id":"proj_123"}'
```

### Sacred Plans
```bash
# Query sacred plans
curl -X POST http://localhost:5556/sacred/query \
  -H "Content-Type: application/json" \
  -d '{"query":"authentication approach","project_id":"proj_123"}'

# Get sacred metrics
curl http://localhost:5556/sacred/metrics?project_id=proj_123
```

## 🔧 Troubleshooting

### Common Issues

**Server won't start**
```bash
# Check if port 5556 is in use
lsof -i :5556
# Kill the process if needed
kill -9 <PID>

# Ensure you're in the virtual environment
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```

**No query results**
- Ensure you've indexed files: `python contextkeeper_cli.py ingest /your/project`
- Check project is focused: `python contextkeeper_cli.py projects list`
- Verify project path is correct in project creation

**Sacred plan approval fails**
- Check SACRED_APPROVAL_KEY in .env
- Ensure verification code is correct
- Verify plan file exists and is readable

**Dashboard not loading**
- Clear browser cache
- Check browser console for errors
- Verify server is running on port 5556
- Try incognito/private browsing mode

### Getting Logs

```bash
# Check server logs
python rag_agent.py server --debug

# Check CLI logs
python contextkeeper_cli.py --verbose <command>
```

### Quick Health Check

```bash
# Verify everything is working
python contextkeeper_cli.py health
python contextkeeper_cli.py projects list
python contextkeeper_cli.py ask "test query"
```

## 💡 Best Practices

### Project Organisation

- **Use descriptive project names**: "E-commerce API" not "proj1"
- **Focus on one project at a time** for better results
- **Update project indexes** after major code changes
- **Archive completed projects** to keep workspace clean

### Sacred Plans

- **Start with core architectural decisions** (auth, database, API design)
- **Keep plans focused and specific** (one concern per plan)
- **Review plans as a team** before approval
- **Monitor drift regularly** during development

### Query Optimization

- **Be specific in your questions**: "How does JWT validation work?" vs "How does auth work?"
- **Use tags and filters** when searching large codebases
- **Try both basic and AI-enhanced queries** for different insights
- **Use the chat interface** for iterative exploration

### Performance Tips

- **Exclude large files** (logs, builds, node_modules) during project creation
- **Update project indexes** instead of re-creating projects
- **Use project focus** to limit search scope
- **Monitor dashboard performance** on older devices

## 🆘 Getting Help

### Documentation
- [Installation Guide](INSTALLATION.md) - Detailed setup instructions
- [API Documentation](API_REFERENCE.md) - Complete API reference
- [Sacred Layer Guide](SACRED_LAYER.md) - Architectural governance details
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions

### Community & Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share experiences
- **Wiki**: Community-contributed guides and examples

### Quick Support Commands

```bash
# System information
python contextkeeper_cli.py health --verbose

# Export project state for bug reports
python contextkeeper_cli.py export <project_id> --debug

# Check logs
tail -f logs/contextkeeper.log
```

### Emergency Recovery

If your installation is completely broken:

```bash
# Reset virtual environment
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Reset project database
rm -rf chromadb/
python rag_agent.py server
```

---

**Last Updated**: August 2025 | **Version**: 3.0 | **Status**: Production Ready

For the latest updates and advanced features, visit our [GitHub repository](https://github.com/lostmind008/contextkeeper-v3).