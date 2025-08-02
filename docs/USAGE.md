# LostMind AI - ContextKeeper v3.0 Usage Guide

## Overview

ContextKeeper v3.0 provides AI-aware development context with beautiful Three.js dashboard, real-time analytics, and comprehensive project management through an intuitive interface.

## 🎨 Beautiful Dashboard

### Access the Dashboard
Open your browser and navigate to:
```
http://localhost:5556/analytics_dashboard_live.html
```

### Dashboard Features
- **Interactive Three.js Background**: 4000 animated particles with mouse interaction
- **Real-time Statistics**: Live project metrics and system health monitoring
- **Project Management**: Create, view, and focus projects with beautiful UI
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern Dark Theme**: Glass morphism effects with color-coded indicators

## Basic Workflow

### 1. Project Setup
```bash
# Create a new project
./scripts/rag_cli_v2.sh projects create "E-commerce Platform" /path/to/project

# Focus on the project
./scripts/rag_cli_v2.sh projects focus proj_abc123

# Check project status
./scripts/rag_cli_v2.sh projects list
```

### 2. Sacred Plan Creation
```bash
# Create architectural plan
./scripts/rag_cli_v2.sh sacred create proj_abc123 "Database Architecture" database_plan.md

# Create security plan
./scripts/rag_cli_v2.sh sacred create proj_abc123 "Security Guidelines" security_plan.md

# List sacred plans
./scripts/rag_cli_v2.sh sacred list proj_abc123
```

### 3. Plan Approval (2-Layer Verification)
```bash
# Generate verification code
./scripts/rag_cli_v2.sh sacred approve plan_def456

# This will:
# 1. Generate time-based verification code
# 2. Verify SACRED_APPROVAL_KEY from environment
# 3. Make plan immutable once approved
```

### 4. Development with Drift Detection
```bash
# Check alignment with sacred plans
./scripts/rag_cli_v2.sh sacred drift proj_abc123

# Query sacred context
./scripts/rag_cli_v2.sh sacred query proj_abc123 "authentication approach"

# Get development context
./scripts/rag_cli_v2.sh context export proj_abc123
```

## Available CLI Commands

### Project Management
```bash
# List all projects
./scripts/rag_cli_v2.sh projects list

# Create new project
./scripts/rag_cli_v2.sh projects create "Project Name" /path/to/project [description]

# Focus on project
./scripts/rag_cli_v2.sh projects focus <project_id>

# Pause project
./scripts/rag_cli_v2.sh projects pause <project_id>

# Resume project
./scripts/rag_cli_v2.sh projects resume <project_id>

# Archive project
./scripts/rag_cli_v2.sh projects archive <project_id>
```

### Decision Tracking
```bash
# Add architectural decision
./scripts/rag_cli_v2.sh decisions add "Using microservices" "Better scalability" "architecture,scaling"

# Interactive mode (if no arguments provided)
./scripts/rag_cli_v2.sh decisions add
```

### Objective Management
```bash
# Add development objective
./scripts/rag_cli_v2.sh objectives add <project_id> "Implement user authentication" "High priority" high

# Complete objective
./scripts/rag_cli_v2.sh objectives complete <project_id> <objective_id>

# List objectives
./scripts/rag_cli_v2.sh objectives list [project_id]
```

### Context and Analytics
```bash
# Export project context
./scripts/rag_cli_v2.sh context export [project_id]

# Get daily briefing
./scripts/rag_cli_v2.sh briefing

# Ask questions with LLM
./scripts/rag_cli_v2.sh ask "What authentication system are we using?"
```

### Sacred Layer Commands
```bash
# Create sacred plan
./scripts/rag_cli_v2.sh sacred create <project_id> "<title>" <plan_file>

# Approve sacred plan
./scripts/rag_cli_v2.sh sacred approve <plan_id>

# List sacred plans
./scripts/rag_cli_v2.sh sacred list <project_id>

# Check drift
./scripts/rag_cli_v2.sh sacred drift <project_id>

# Query sacred layer
./scripts/rag_cli_v2.sh sacred query <project_id> "<query>"
```

## Claude Code Integration

### Using MCP Tools

Once configured, use these tools in Claude Code:

#### 1. **get_development_context**
```
Get comprehensive development context for current project
/mcp get_development_context contextkeeper-sacred project_id=proj_abc123
```

#### 2. **check_development_drift**
```
Check if current development aligns with sacred plans
/mcp check_development_drift contextkeeper-sacred project_id=proj_abc123
```

#### 3. **query_with_llm**
```  
Get natural language explanations of technical decisions
/mcp query_with_llm contextkeeper-sacred question="Why did we choose PostgreSQL?"
```

#### 4. **intelligent_search**
```
Search across code, decisions, and sacred plans
/mcp intelligent_search contextkeeper-sacred query="user authentication"
```

#### 5. **analyze_git_activity**
```
Analyze recent git activity and changes
/mcp analyze_git_activity contextkeeper-sacred project_id=proj_abc123
```

#### 6. **manage_objectives**
```
Manage development objectives
/mcp manage_objectives contextkeeper-sacred action=add project_id=proj_abc123 title="Implement auth" priority=high
```

#### 7. **track_decision**
```
Record architectural decisions
/mcp track_decision contextkeeper-sacred decision="Using Redis for caching" reasoning="Performance reasons"
```

#### 8. **suggest_next_action**
```
Get AI-powered suggestions for next development steps
/mcp suggest_next_action contextkeeper-sacred project_id=proj_abc123
```

### AI-Aware Development

When working with Claude Code:

1. **Start with Context**: Ask Claude to get the development context before making suggestions
2. **Check Drift Regularly**: Use drift detection to ensure alignment with sacred plans
3. **Query Decisions**: Use LLM-enhanced queries to understand past decisions
4. **Export Context**: Provide full context for complex discussions

## API Endpoints

### Core Endpoints
```bash
# Health check
GET http://localhost:5556/health
# Response: {"status":"healthy","timestamp":"2025-08-02T17:00:18.547248"}

# List projects
GET http://localhost:5556/projects
# Returns: Array of project objects with metadata

# Query project context
POST http://localhost:5556/query
Content-Type: application/json
{
  "query": "authentication implementation",
  "project_id": "proj_123"
}

# Create project
POST http://localhost:5556/projects
Content-Type: application/json
{
  "name": "My Project",
  "root_path": "/path/to/project",
  "description": "Project description"
}
```

### Sacred Layer Endpoints
```bash
# Create sacred plan
POST http://localhost:5556/sacred/plans
Content-Type: application/json
{
  "project_id": "proj_123",
  "title": "Database Architecture",
  "file_path": "/path/to/plan.md"
}

# List sacred plans
GET http://localhost:5556/sacred/plans

# Approve sacred plan
POST http://localhost:5556/sacred/plans/<plan_id>/approve
Content-Type: application/json
{
  "approver": "John Doe",
  "verification_code": "ABC123",
  "secondary_verification": "your-approval-key"
}

# Query sacred layer
POST http://localhost:5556/sacred/query
Content-Type: application/json
{
  "query": "database architecture plans"
}
```

### Analytics Endpoints
```bash
# Analytics summary
GET http://localhost:5556/analytics/summary

# Beautiful dashboard
GET http://localhost:5556/analytics_dashboard_live.html

# Project drift analysis
GET http://localhost:5556/projects/<project_id>/drift

# Daily briefing
GET http://localhost:5556/daily-briefing
```

### Decision and Objective Endpoints
```bash
# Add decision
POST http://localhost:5556/decision
Content-Type: application/json
{
  "decision": "Using Redis for caching",
  "reasoning": "Performance reasons",
  "tags": ["performance", "caching"]
}

# Add objective
POST http://localhost:5556/projects/<project_id>/objectives
Content-Type: application/json
{
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication",
  "priority": "high"
}

# Complete objective
POST http://localhost:5556/projects/<project_id>/objectives/<objective_id>/complete
```

## Sacred Plan Examples

### Database Architecture Plan
```markdown
# Database Architecture - Sacred Plan

## Core Principles
- Use PostgreSQL as primary database
- Implement read replicas for scaling
- All migrations must be backward compatible

## Schema Design
- Use UUID primary keys for all entities
- Implement soft deletes with deleted_at timestamp
- All tables must have created_at and updated_at

## Security Requirements
- All sensitive data encrypted at rest
- Database connections must use TLS
- Implement row-level security where applicable
```

### API Design Sacred Plan
```markdown
# API Design Guidelines - Sacred Plan

## REST Principles
- Use standard HTTP methods (GET, POST, PUT, DELETE)
- Implement proper HTTP status codes
- Use JSON for request/response bodies

## Authentication
- JWT tokens for API authentication
- Refresh token rotation every 24 hours
- Rate limiting: 1000 requests/hour per user

## Error Handling
- Consistent error response format
- Never expose internal system details
- Implement proper logging for all errors
```

## Troubleshooting

### Server Issues
```bash
# Check server status
curl http://localhost:5556/health

# Start server in server-only mode (recommended)
python rag_agent.py server

# Check server logs
tail -f rag_agent.out
```

### Dashboard Issues
```bash
# Verify dashboard accessibility
curl -I http://localhost:5556/analytics_dashboard_live.html

# Check browser console for JavaScript errors
# Ensure Three.js is loading properly
```

### Sacred Plan Issues
```bash
# Check sacred plan status
./scripts/rag_cli_v2.sh sacred status plan_abc123

# View plan approval history
./scripts/rag_cli_v2.sh sacred history plan_abc123

# Recover from drift violations
./scripts/rag_cli_v2.sh sacred drift proj_abc123 --fix
```

### MCP Integration Issues
```bash
# Test MCP connectivity
curl -X POST http://localhost:5556/sacred/health

# Check MCP server logs
tail -f mcp-server/mcp-server.log

# Restart MCP server
pkill -f enhanced_mcp_server.js
node mcp-server/enhanced_mcp_server.js
```

### Performance Optimization
```bash
# Clear ChromaDB cache
rm -rf rag_knowledge_db/chroma_cache

# Check memory usage
ps aux | grep python

# Monitor API response times
curl -w "@curl-format.txt" http://localhost:5556/health
```

## Best Practices

### Dashboard Usage
1. **Regular Monitoring**: Check the dashboard daily for project health
2. **Mobile Access**: Use the responsive design on mobile devices
3. **Real-time Updates**: Dashboard refreshes every 30 seconds automatically
4. **Interactive Features**: Use hover effects and click interactions

### Sacred Plan Creation
1. **Be Specific**: Include concrete technical decisions, not vague principles
2. **Version Control**: Sacred plans should be in git alongside code
3. **Review Process**: Have team review before approval
4. **Living Documents**: Update plans when architecture evolves

### AI Collaboration
1. **Context First**: Always provide development context before asking for code
2. **Check Alignment**: Use drift detection before implementing suggestions
3. **Document Decisions**: Record architectural choices in sacred plans
4. **Review Regularly**: Monitor alignment during development sprints

### Team Usage
1. **Shared Plans**: Use shared sacred plans for team alignment
2. **Role-Based Access**: Control who can approve sacred plans
3. **Audit Trail**: Regular review of plan changes and approvals
4. **Training**: Ensure all team members understand Sacred Layer concepts

## Integration with Development Tools

### VS Code Integration
```bash
# Use ContextKeeper CLI from VS Code terminal
# Set up keybindings for common commands
# Use with GitHub Copilot for AI-aware suggestions
```

### CI/CD Integration
```bash
# Check drift in CI pipeline
./scripts/rag_cli_v2.sh sacred drift $PROJECT_ID --fail-on-violation

# Export context for automated code review
./scripts/rag_cli_v2.sh context export $PROJECT_ID --format json
```

### Monitoring and Alerts
```bash
# Set up drift detection alerts
./scripts/rag_cli_v2.sh sacred monitor alert email "team@company.com"

# Integrate with Slack notifications
./scripts/rag_cli_v2.sh sacred monitor alert slack "#dev-team"
```

For detailed API documentation, see [API_REFERENCE.md](../docs/api/API_REFERENCE.md).
For installation help, see [INSTALLATION.md](INSTALLATION.md).