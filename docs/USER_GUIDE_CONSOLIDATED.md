# ContextKeeper User Guide

**Version**: 3.0  
**Last Updated**: August 2025  
**Status**: Production Ready

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Using the Chat Interface](#using-the-chat-interface)
5. [Command Line Interface](#command-line-interface)
6. [Sacred Layer](#sacred-layer)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

## Quick Start

Get ContextKeeper running in under 2 minutes:

```bash
# 1. Activate your virtual environment
source venv/bin/activate

# 2. Start the agent
python rag_agent.py start

# 3. Verify it's working
curl http://localhost:5556/health
# Should return: {"status":"healthy"}

# 4. Access the chat interface
open http://localhost:5556
```

That's it! You now have a running instance with:
- ✅ Chat interface at http://localhost:5556
- ✅ REST API endpoints available
- ✅ Command line tools ready
- ✅ Sacred layer protection active

## Installation & Setup

### Prerequisites

- Python 3.8+
- Git
- 4GB+ RAM recommended
- Internet connection for initial model downloads

### First-Time Setup

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd contextkeeper
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your settings
   nano .env
   ```

5. **Initialise Database**
   ```bash
   python rag_agent.py init
   ```

### Environment Variables

Create a `.env` file with these essential settings:

```env
# API Configuration
GOOGLE_API_KEY=your_google_api_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Database Settings
CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=contextkeeper_v3

# Server Settings
RAG_AGENT_PORT=5556
RAG_AGENT_HOST=0.0.0.0

# Sacred Layer
SACRED_APPROVAL_KEY=your_sacred_key_here
```

## Core Concepts

### The Knowledge Base

ContextKeeper maintains a comprehensive knowledge base of your project that includes:

- **Code Files**: All source code with semantic understanding
- **Documentation**: README files, API docs, architecture notes
- **Git History**: Commits, branches, and development timeline
- **Decisions**: Architecture decisions and their rationale
- **Sacred Plans**: Immutable architectural decisions

### Sacred Layer

The Sacred Layer is ContextKeeper's unique feature that provides:

- **Immutable Plans**: Critical architectural decisions that cannot be changed
- **Drift Detection**: Alerts when development diverges from approved plans
- **2-Layer Verification**: Dual approval process for critical changes
- **AI Guardrails**: Prevents AI agents from making unauthorised changes

### Project Isolation

Each project gets its own:
- ChromaDB collection
- Sacred plan storage
- Git activity tracking
- Independent configuration

## Using the Chat Interface

### Accessing the Interface

1. Start ContextKeeper: `python rag_agent.py start`
2. Open your browser to: `http://localhost:5556`
3. Start chatting about your codebase!

### Chat Features

**Natural Language Queries**
```
"How does authentication work in this project?"
"Show me the API endpoints for user management"
"What are the recent changes to the database schema?"
```

**Code Search**
```
"Find functions that handle password validation"
"Show me all the React components in the dashboard"
"What files contain error handling logic?"
```

**Architecture Questions**
```
"What is the overall system architecture?"
"How do the microservices communicate?"
"What are the sacred architectural decisions?"
```

**Development Context**
```
"What have I been working on recently?"
"Show me the latest commits and their purpose"
"What are the current priorities?"
```

### Chat Commands

The chat interface supports special commands:

- `!health` - Check system status
- `!projects` - List all tracked projects
- `!sacred` - Show sacred plans for current project
- `!drift` - Check for architectural drift
- `!clear` - Clear chat history

## Command Line Interface

### Basic Commands

```bash
# Health check
./scripts/rag_cli_v2.sh health

# List projects
./scripts/rag_cli_v2.sh projects list

# Query the knowledge base
./scripts/rag_cli_v2.sh ask "How does authentication work?"

# Get project status
./scripts/rag_cli_v2.sh projects status my_project
```

### Sacred Layer Commands

```bash
# Create a sacred plan
./scripts/rag_cli_v2.sh sacred create proj_123 "Authentication Method" auth_plan.md

# Approve a sacred plan
./scripts/rag_cli_v2.sh sacred approve plan_abc123

# Check for drift
./scripts/rag_cli_v2.sh sacred drift proj_123

# List all sacred plans
./scripts/rag_cli_v2.sh sacred list proj_123
```

### Project Management

```bash
# Add a new project
./scripts/rag_cli_v2.sh projects add my_new_project /path/to/project

# Update project knowledge
./scripts/rag_cli_v2.sh projects update my_project

# Remove a project
./scripts/rag_cli_v2.sh projects remove my_project

# Export project data
./scripts/rag_cli_v2.sh projects export my_project output.json
```

## Sacred Layer

### What Are Sacred Plans?

Sacred plans are immutable architectural decisions that:
- Cannot be changed without explicit approval
- Serve as guardrails for AI development
- Maintain system integrity over time
- Document critical design decisions

### Creating Sacred Plans

1. **Identify Critical Decisions**
   - Authentication methods
   - Database schema changes
   - API design patterns
   - Security protocols

2. **Create the Plan**
   ```bash
   ./scripts/rag_cli_v2.sh sacred create project_id "Plan Title" plan_file.md
   ```

3. **Get Approval**
   Sacred plans require 2-layer verification:
   - Technical review
   - Stakeholder approval

### Sacred Plan Structure

```markdown
# Sacred Plan: [Title]

## Context
Why this decision is needed.

## Decision
What was decided.

## Consequences
Implications of this decision.

## Implementation
How to implement this decision.

## Verification
How to verify compliance.
```

### Drift Detection

ContextKeeper automatically monitors for drift:

```bash
# Check current drift status
./scripts/rag_cli_v2.sh sacred drift my_project

# Get detailed drift report
curl -X POST http://localhost:5556/sacred/drift \
  -H "Content-Type: application/json" \
  -d '{"project_id": "my_project"}'
```

## Advanced Features

### REST API

ContextKeeper provides a comprehensive REST API:

```bash
# Health check
GET /health

# Query with natural language
POST /query_llm
{
  "question": "How does authentication work?",
  "k": 5
}

# Get project list
GET /projects

# Sacred layer operations
POST /sacred/create
POST /sacred/approve
POST /sacred/drift
```

### Integration with Claude Code

ContextKeeper includes MCP (Model Context Protocol) server integration:

1. **Available Tools**:
   - `get_sacred_context`
   - `check_sacred_drift`
   - `query_with_llm`
   - `export_development_context`
   - `intelligent_search`

2. **Setup**:
   ```bash
   # MCP server runs automatically with ContextKeeper
   # Tools appear in Claude Code interface
   ```

### Multi-Project Support

```bash
# Switch between projects
./scripts/rag_cli_v2.sh projects switch project_name

# Compare projects
./scripts/rag_cli_v2.sh projects compare proj1 proj2

# Bulk operations
./scripts/rag_cli_v2.sh projects bulk-update /path/to/projects/
```

### Analytics Dashboard

Access the analytics dashboard at: `http://localhost:5556/dashboard`

Features:
- Project health metrics
- Query patterns
- Sacred layer compliance
- Git activity visualisation

## Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Find what's using port 5556
lsof -i :5556

# Kill the process
kill -9 <PID>

# Or use a different port
export RAG_AGENT_PORT=5557
python rag_agent.py start
```

**2. Database Connection Issues**
```bash
# Reset the database
rm -rf ./chroma_db
python rag_agent.py init

# Check permissions
chmod -R 755 ./chroma_db
```

**3. Empty Query Results**
```bash
# Re-index the project
./scripts/rag_cli_v2.sh projects update my_project

# Check if files were indexed
./scripts/rag_cli_v2.sh projects status my_project
```

**4. Sacred Layer Not Working**
```bash
# Verify sacred key is set
echo $SACRED_APPROVAL_KEY

# Check sacred layer health
curl http://localhost:5556/sacred/health
```

### Performance Issues

**Slow Queries**
- Reduce the number of results: `{"k": 3}` instead of `{"k": 10}`
- Use more specific questions
- Check available RAM

**High Memory Usage**
- Restart the service periodically
- Reduce the number of tracked projects
- Clear old embeddings

### Getting Help

1. **Check Logs**
   ```bash
   tail -f rag_agent.log
   ```

2. **System Health Check**
   ```bash
   ./scripts/rag_cli_v2.sh health --verbose
   ```

3. **Debug Mode**
   ```bash
   DEBUG=1 python rag_agent.py start
   ```

## Best Practices

### Project Organisation

1. **Use Descriptive Project Names**
   ```bash
   # Good
   ./scripts/rag_cli_v2.sh projects add "ecommerce-api" /path/to/api

   # Avoid
   ./scripts/rag_cli_v2.sh projects add "proj1" /path/to/api
   ```

2. **Regular Updates**
   ```bash
   # Update after significant changes
   git commit -m "Major refactor"
   ./scripts/rag_cli_v2.sh projects update my_project
   ```

3. **Sacred Plan Guidelines**
   - Create sacred plans for architectural decisions
   - Keep plans focused and specific
   - Include implementation guidance
   - Regular drift checks

### Query Optimisation

1. **Be Specific**
   ```bash
   # Good
   "How does the JWT authentication middleware work?"
   
   # Less effective
   "How does auth work?"
   ```

2. **Use Context**
   ```bash
   # Provide context for better results
   "In the user management module, how are passwords validated?"
   ```

3. **Iterative Refinement**
   - Start with broad questions
   - Narrow down based on results
   - Use follow-up questions

### Maintenance

1. **Regular Health Checks**
   ```bash
   # Weekly health check
   ./scripts/rag_cli_v2.sh health --full
   ```

2. **Database Maintenance**
   ```bash
   # Monthly database cleanup
   python rag_agent.py cleanup --older-than 30d
   ```

3. **Sacred Layer Review**
   ```bash
   # Quarterly sacred plan review
   ./scripts/rag_cli_v2.sh sacred list --all --review
   ```

### Security

1. **Protect API Keys**
   - Never commit `.env` files
   - Use environment-specific keys
   - Rotate keys regularly

2. **Sacred Layer Security**
   - Use strong sacred approval keys
   - Limit sacred plan access
   - Regular drift monitoring

3. **Network Security**
   - Run on localhost for development
   - Use HTTPS in production
   - Implement rate limiting

---

## Getting Started Checklist

- [ ] Clone repository
- [ ] Set up virtual environment
- [ ] Install dependencies
- [ ] Configure `.env` file
- [ ] Run health check
- [ ] Access chat interface
- [ ] Test CLI commands
- [ ] Create first project
- [ ] Test sacred layer
- [ ] Read best practices

## Support

For issues and questions:
1. Check this user guide
2. Review the troubleshooting section
3. Check project logs
4. Run health diagnostics
5. Consult the API reference documentation

ContextKeeper v3.0 - Your intelligent codebase companion with Sacred Layer protection.