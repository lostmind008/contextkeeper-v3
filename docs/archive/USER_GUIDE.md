# LostMind AI - ContextKeeper v3.0 User Guide

## Welcome to ContextKeeper! 🎉

ContextKeeper is a revolutionary AI-powered development context management system that helps you maintain clarity, consistency, and control over your development projects. With its beautiful Three.js dashboard, real-time analytics, and intelligent context tracking, ContextKeeper transforms how you manage development knowledge.

## 🎨 Getting Started with the Beautiful Dashboard

### First Steps
1. **Start ContextKeeper**: `python rag_agent.py server`
2. **Open Dashboard**: Navigate to `http://localhost:5556/analytics_dashboard_live.html`
3. **Experience the Magic**: Enjoy the interactive Three.js particle animation!

### Dashboard Features
- **Interactive Background**: 4000 animated particles that respond to your mouse
- **Real-time Stats**: Live project metrics and system health
- **Project Management**: Create, view, and focus projects with beautiful UI
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern Dark Theme**: Glass morphism effects with color-coded indicators

## 🚀 Core Workflows

### 1. Project Management

#### Creating Your First Project
```bash
# Create a new project
./scripts/rag_cli_v2.sh projects create "My Awesome App" /path/to/your/project

# The system will automatically:
# - Filter out irrelevant files (venv, node_modules, etc.)
# - Index your codebase for semantic search
# - Set up isolated project context
```

#### Managing Projects
```bash
# List all projects
./scripts/rag_cli_v2.sh projects list

# Focus on a specific project
./scripts/rag_cli_v2.sh projects focus proj_abc123

# Pause a project (temporarily stop tracking)
./scripts/rag_cli_v2.sh projects pause proj_abc123

# Resume a project
./scripts/rag_cli_v2.sh projects resume proj_abc123

# Archive a project (long-term storage)
./scripts/rag_cli_v2.sh projects archive proj_abc123
```

### 2. Asking Questions with LLM

#### Natural Language Queries
```bash
# Ask about your codebase
./scripts/rag_cli_v2.sh ask "What authentication system are we using?"

# Get architectural insights
./scripts/rag_cli_v2.sh ask "How is the database structured?"

# Understand specific features
./scripts/rag_cli_v2.sh ask "How does the user registration work?"
```

#### What You'll Get
- **Natural Language Responses**: Instead of raw code chunks, you get explanations
- **Context-Aware Answers**: Responses consider your project's architecture
- **Relevant Examples**: Code snippets that actually apply to your project
- **Architectural Insights**: Understanding of how different parts connect

### 3. Decision Tracking

#### Recording Architectural Decisions
```bash
# Add a decision with reasoning
./scripts/rag_cli_v2.sh decisions add "Using Redis for caching" "Performance reasons" "performance,caching"

# Interactive mode (if no arguments provided)
./scripts/rag_cli_v2.sh decisions add
# Then follow the prompts
```

#### Why Track Decisions?
- **Knowledge Preservation**: Never lose important architectural reasoning
- **Team Alignment**: Share context with new team members
- **Future Reference**: Understand why certain choices were made
- **AI Context**: Help AI assistants understand your architectural decisions

### 4. Objective Management

#### Setting Development Objectives
```bash
# Add an objective
./scripts/rag_cli_v2.sh objectives add proj_abc123 "Implement user authentication" "Add JWT-based auth" high

# List objectives
./scripts/rag_cli_v2.sh objectives list proj_abc123

# Complete an objective
./scripts/rag_cli_v2.sh objectives complete proj_abc123 obj_123
```

#### Objective Benefits
- **Progress Tracking**: Monitor development milestones
- **Team Coordination**: Align team efforts
- **AI Assistance**: Help AI understand your current priorities
- **Project Health**: Visual indicators of project progress

### 5. Sacred Plan Management

#### Creating Architectural Plans
```bash
# Create a sacred plan
./scripts/rag_cli_v2.sh sacred create proj_abc123 "Database Architecture" database_plan.md

# The system will:
# - Generate a verification code
# - Store the plan securely
# - Make it available for drift detection
```

#### Approving Sacred Plans
```bash
# Approve a plan (2-layer verification)
./scripts/rag_cli_v2.sh sacred approve plan_def456

# This requires:
# 1. Verification code (from plan creation)
# 2. Sacred approval key (from environment)
# 3. Approver name (for audit trail)
```

#### Checking Alignment
```bash
# Check if code aligns with sacred plans
./scripts/rag_cli_v2.sh sacred drift proj_abc123

# Query sacred context
./scripts/rag_cli_v2.sh sacred query proj_abc123 "authentication approach"
```

## 📊 Dashboard Deep Dive

### Understanding the Dashboard

#### Stats Cards
- **Active Projects**: Number of currently tracked projects
- **Focused Project**: Currently active project (if any)
- **Total Decisions**: Number of architectural decisions recorded
- **System Health**: Overall system status and performance

#### Project Grid
- **Project Cards**: Visual representation of each project
- **Status Indicators**: Color-coded project status (active, paused, archived)
- **Quick Actions**: Click to focus, view details, or manage projects
- **Real-time Updates**: Live data refresh every 30 seconds

#### Interactive Features
- **Particle Animation**: Move your mouse to interact with the background
- **Hover Effects**: Beautiful animations on cards and buttons
- **Modal System**: Create new projects with elegant forms
- **Toast Notifications**: Real-time feedback for your actions

### Dashboard Controls
- **Refresh**: Manually update dashboard data
- **Analytics**: Access detailed analytics (same as dashboard)
- **API Docs**: Quick access to API documentation
- **GitHub**: Link to project repository

## 🔗 Claude Code Integration

### Setting Up MCP Integration

1. **Configure Claude Code**:
   ```json
   {
     "contextkeeper-sacred": {
       "type": "stdio",
       "command": "node",
       "args": ["/path/to/contextkeeper/mcp-server/enhanced_mcp_server.js"],
       "env": {"RAG_AGENT_URL": "http://localhost:5556"}
     }
   }
   ```

2. **Available MCP Tools**:
   - `get_development_context` - Get comprehensive project context
   - `intelligent_search` - Search code, decisions, and plans
   - `analyze_git_activity` - Analyze recent changes
   - `check_development_drift` - Check alignment with sacred plans
   - `manage_objectives` - Manage development objectives
   - `track_decision` - Record architectural decisions
   - `suggest_next_action` - Get AI-powered suggestions
   - `get_code_context` - Get relevant code examples

### Using MCP Tools in Claude Code

#### Getting Context
```
/mcp get_development_context contextkeeper-sacred project_id=proj_abc123
```

#### Searching Code
```
/mcp intelligent_search contextkeeper-sacred query="user authentication"
```

#### Checking Drift
```
/mcp check_development_drift contextkeeper-sacred project_id=proj_abc123
```

#### Recording Decisions
```
/mcp track_decision contextkeeper-sacred decision="Using Redis for caching" reasoning="Performance reasons"
```

## 📈 Analytics and Insights

### Daily Briefing
```bash
# Get a comprehensive project overview
./scripts/rag_cli_v2.sh briefing

# Shows:
# - Total projects and their status
# - Pending objectives
# - Recent decisions
# - System health
```

### Context Export
```bash
# Export full project context
./scripts/rag_cli_v2.sh context export proj_abc123

# Returns comprehensive project data:
# - Project metadata
# - Recent decisions
# - Pending objectives
# - Sacred plans
# - Git activity
```

### API Access
```bash
# Health check
curl http://localhost:5556/health

# Project list
curl http://localhost:5556/projects

# Analytics summary
curl http://localhost:5556/analytics/summary

# Daily briefing
curl http://localhost:5556/daily-briefing
```

## 🛠️ Troubleshooting

### Common Issues

#### Server Not Starting
```bash
# Use server-only mode (recommended)
python rag_agent.py server

# Check logs
tail -f rag_agent.out

# Verify port availability
netstat -an | grep 5556
```

#### Dashboard Not Loading
```bash
# Verify server is running
curl http://localhost:5556/health

# Check dashboard route
curl -I http://localhost:5556/analytics_dashboard_live.html

# Check browser console for JavaScript errors
# Press F12 and check Console tab
```

#### CLI Commands Not Working
```bash
# Ensure script is executable
chmod +x scripts/rag_cli_v2.sh

# Check server is running
curl http://localhost:5556/health

# Use correct script name
./scripts/rag_cli_v2.sh projects list  # Not rag_cli.sh
```

#### API Key Issues
```bash
# Check environment variables
echo $GOOGLE_API_KEY
echo $GEMINI_API_KEY

# Test API access
curl -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GOOGLE_API_KEY" \
  https://generativelanguage.googleapis.com/v1beta/models
```

### Performance Optimization

#### Database Issues
```bash
# Clear corrupted database
rm -rf rag_knowledge_db
mkdir rag_knowledge_db

# Restart server
python rag_agent.py server
```

#### Memory Usage
```bash
# Monitor memory usage
ps aux | grep python

# Check disk space
df -h

# Monitor API response times
curl -w "@curl-format.txt" http://localhost:5556/health
```

## 🎯 Best Practices

### Project Management
1. **Start Small**: Create one project first to understand the workflow
2. **Use Descriptive Names**: Clear project names help with organization
3. **Regular Updates**: Keep project context current with regular updates
4. **Archive Old Projects**: Archive completed projects to reduce clutter

### Decision Tracking
1. **Be Specific**: Include concrete technical decisions, not vague principles
2. **Add Reasoning**: Always explain why decisions were made
3. **Use Tags**: Tag decisions for easy categorization and search
4. **Regular Reviews**: Periodically review and update decisions

### Sacred Plans
1. **Be Comprehensive**: Include all relevant architectural constraints
2. **Version Control**: Keep sacred plans in git alongside code
3. **Team Review**: Have team review before approval
4. **Living Documents**: Update plans when architecture evolves

### AI Collaboration
1. **Context First**: Always provide context before asking for code
2. **Check Alignment**: Use drift detection before implementing suggestions
3. **Document Decisions**: Record architectural choices in sacred plans
4. **Regular Monitoring**: Check alignment during development sprints

### Dashboard Usage
1. **Daily Check**: Review dashboard daily for project health
2. **Mobile Access**: Use responsive design on mobile devices
3. **Interactive Features**: Use hover effects and click interactions
4. **Real-time Updates**: Dashboard refreshes automatically every 30 seconds

## 🔮 Advanced Features

### Git Integration
- **Activity Tracking**: Monitor git commits and file changes
- **Context Sync**: Keep project context synchronized with code changes
- **Drift Detection**: Identify when code diverges from sacred plans

### Multi-Project Support
- **Complete Isolation**: Zero cross-contamination between projects
- **Independent Context**: Each project maintains its own knowledge base
- **Flexible Management**: Pause, resume, and archive projects as needed

### Security Features
- **Local-First**: All data stored locally, no external dependencies
- **Auto-Redaction**: Automatically detects and redacts sensitive data
- **Path Security**: Smart filtering prevents access to sensitive directories
- **Audit Trail**: Complete logging of all operations

## 📚 Additional Resources

### Documentation
- **API Reference**: [docs/api/API_REFERENCE.md](docs/api/API_REFERENCE.md)
- **Installation Guide**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

### Support
- **GitHub Issues**: [Report bugs and request features](https://github.com/lostmind008/contextkeeper-v3/issues)
- **Discussions**: [Community discussions](https://github.com/lostmind008/contextkeeper-v3/discussions)
- **Documentation**: [Comprehensive guides and examples](https://github.com/lostmind008/contextkeeper-v3/tree/main/docs)

---

**✨ Made with care by [LostMindAI](https://github.com/lostmind008) | Ready to transform your development workflow!** 