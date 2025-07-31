# ContextKeeper v3.0 User Guide

Welcome to ContextKeeper! This guide will help you get up and running in minutes.

## 🚀 Quick Start

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
# Edit .env and add your Google API key:
# GOOGLE_API_KEY=your-api-key-here
# SACRED_APPROVAL_KEY=your-secret-key

# 5. Start ContextKeeper
python rag_agent.py start
```

### Your First Project

```bash
# Create a project
./scripts/rag_cli_v2.sh projects create myproject /path/to/your/code

# List all projects
./scripts/rag_cli_v2.sh projects list

# Focus on your project (makes it the default)
./scripts/rag_cli_v2.sh projects focus myproject
```

### Your First Query

```bash
# Ask a question about your code
./scripts/rag_cli_v2.sh ask "How does the authentication work?"

# Get an AI-enhanced response
./scripts/rag_cli_v2.sh ask --llm "Explain the database schema"
```

## 📋 Core Workflows

### Managing Projects

**Create a New Project**
```bash
./scripts/rag_cli_v2.sh projects create <name> <path>
# Example: ./scripts/rag_cli_v2.sh projects create webapp /home/user/webapp
```

**Focus on a Project** (set as default)
```bash
./scripts/rag_cli_v2.sh projects focus <project_id>
# Example: ./scripts/rag_cli_v2.sh projects focus proj_123abc
```

**List All Projects**
```bash
./scripts/rag_cli_v2.sh projects list
```

### Ingesting Code & Documents

**Ingest a Single File**
```bash
./scripts/rag_cli_v2.sh ingest /path/to/file.py
```

**Ingest a Directory**
```bash
./scripts/rag_cli_v2.sh ingest /path/to/directory
```

**Note**: ContextKeeper automatically filters out `node_modules`, `venv`, `.git`, and other common directories.

### Running Queries

**CLI Query**
```bash
# Basic query
./scripts/rag_cli_v2.sh ask "What does the UserService class do?"

# With more results
./scripts/rag_cli_v2.sh ask "Find all API endpoints" -k 10

# With AI enhancement
./scripts/rag_cli_v2.sh ask --llm "How can I add user authentication?"
```

**API Query**
```bash
# Basic query
curl -X POST http://localhost:5556/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the database schema?", "project_id": "proj_123"}'

# AI-enhanced query
curl -X POST http://localhost:5556/query_llm \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain the authentication flow", "project_id": "proj_123"}'
```

### Sacred Plans (Architectural Governance)

**Create a Sacred Plan**
```bash
# Create a plan file (example: auth_plan.md)
cat > auth_plan.md << EOF
# Authentication Architecture

## Overview
We will use OAuth2 with JWT tokens for authentication.

## Components
- AuthService: Handles login/logout
- TokenManager: JWT creation/validation
- UserStore: User data persistence

## Constraints
- Tokens expire after 1 hour
- Refresh tokens valid for 7 days
- No plaintext password storage
EOF

# Submit the plan
./scripts/rag_cli_v2.sh sacred create proj_123 "OAuth2 Authentication" auth_plan.md
```

**Approve a Sacred Plan** (requires 2-layer verification)
```bash
# Get the plan ID from creation output, then:
./scripts/rag_cli_v2.sh sacred approve plan_abc123
# Enter verification code when prompted
# Enter SACRED_APPROVAL_KEY from your .env
```

**Check for Drift**
```bash
./scripts/rag_cli_v2.sh sacred drift proj_123
```

### Using the Analytics Dashboard

Open your browser to: `http://localhost:5556/analytics_dashboard_live.html`

**Dashboard Features:**
- **Real-time Metrics**: Project stats, query volume, sacred compliance
- **Dark Mode**: Click the theme toggle (🌙/☀️)
- **Export Reports**: Click Export → Choose PDF, PNG, or JSON
- **Filter Projects**: Use the search bar or status dropdown
- **Keyboard Shortcuts**:
  - `Ctrl/Cmd + R`: Refresh data
  - `Ctrl/Cmd + D`: Toggle dark mode
  - `Ctrl/Cmd + E`: Open export menu

## 📝 CLI Command Reference

### Project Commands
```bash
# Create project
./scripts/rag_cli_v2.sh projects create <name> <path>

# List projects
./scripts/rag_cli_v2.sh projects list

# Focus project
./scripts/rag_cli_v2.sh projects focus <project_id>

# Show project details
./scripts/rag_cli_v2.sh projects show <project_id>
```

### Query Commands
```bash
# Basic query
./scripts/rag_cli_v2.sh ask "your question here"

# Query with options
./scripts/rag_cli_v2.sh ask "question" -k 10 --project proj_123

# AI-enhanced query
./scripts/rag_cli_v2.sh ask --llm "explain this concept"
```

### Sacred Layer Commands
```bash
# Create sacred plan
./scripts/rag_cli_v2.sh sacred create <project_id> "Plan Title" plan.md

# List sacred plans
./scripts/rag_cli_v2.sh sacred list [project_id]

# Approve plan
./scripts/rag_cli_v2.sh sacred approve <plan_id>

# Check drift
./scripts/rag_cli_v2.sh sacred drift <project_id>

# Query sacred plans
./scripts/rag_cli_v2.sh sacred query "architecture question"
```

### Decision & Objective Commands
```bash
# Track decision
./scripts/rag_cli_v2.sh decision "We chose PostgreSQL" "Better JSON support"

# Add objective
./scripts/rag_cli_v2.sh objective add "Implement user authentication"

# List objectives
./scripts/rag_cli_v2.sh objective list
```

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
  -d '{"name": "MyApp", "root_path": "/path/to/app"}'
```

### Queries
```bash
# Basic query
curl -X POST http://localhost:5556/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Find the main function", "project_id": "proj_123"}'

# AI-enhanced query
curl -X POST http://localhost:5556/query_llm \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain the API structure", "project_id": "proj_123"}'
```

### Sacred Plans
```bash
# Query sacred plans
curl -X POST http://localhost:5556/sacred/query \
  -H "Content-Type: application/json" \
  -d '{"query": "authentication plans", "project_id": "proj_123"}'

# Get sacred metrics
curl http://localhost:5556/analytics/sacred
```

## 🔧 Troubleshooting

### Common Issues & Fixes

**Server won't start**
```bash
# Check if port 5556 is in use
lsof -i :5556
# Kill the process if needed
kill -9 <PID>
```

**"No module named 'google.genai'"**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```

**Sacred plan approval fails**
- Check your `SACRED_APPROVAL_KEY` in `.env`
- Ensure you're entering the correct verification code
- Verification codes are case-sensitive

**No results from queries**
- Ensure you've ingested files: `./scripts/rag_cli_v2.sh ingest /your/project`
- Check project is focused: `./scripts/rag_cli_v2.sh projects list`
- Verify service is healthy: `curl http://localhost:5556/health`

## 💡 Best Practices

### Project Organisation
- Use descriptive project names: `webapp-frontend`, not `proj1`
- One project per repository/component
- Focus the project you're actively working on

### Sacred Plans
- Keep plans concise and specific
- Include clear constraints and boundaries
- Update plans when architecture evolves (supersede, don't edit)
- Review drift warnings promptly

### Performance Tips
- Ingest only necessary directories (exclude `build/`, `dist/`)
- Use specific queries rather than broad ones
- Clear old projects you're not using
- Restart the service weekly for optimal performance

### Query Tips
- Be specific: "UserService authentication" > "auth"
- Use code terminology: "class UserService" finds class definitions
- Try AI queries for explanations: `--llm` flag
- Increase results with `-k 20` for comprehensive searches

## 📚 Next Steps & Getting Help

### Explore Advanced Features
- **MCP Integration**: Connect to Claude Code (see README.md)
- **Git Integration**: Track commits and branches automatically
- **Custom Embeddings**: Configure alternative embedding models

### Getting Help
- **Documentation**: Check `/docs` folder for detailed guides
- **Troubleshooting**: See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
- **Issues**: Report bugs at [GitHub Issues](https://github.com/lostmind008/contextkeeper-v3/issues)
- **Community**: Join discussions at [GitHub Discussions](https://github.com/lostmind008/contextkeeper-v3/discussions)

### Quick Health Check
```bash
# Verify everything is working
curl http://localhost:5556/health
./scripts/rag_cli_v2.sh projects list
./scripts/rag_cli_v2.sh ask "test query"
```

---

**Happy coding with ContextKeeper! 🚀**

*Remember: ContextKeeper helps you maintain architectural context and prevent knowledge drift. Use sacred plans to protect your core architecture and let AI assistants work within your constraints.*