# ContextKeeper v3.0 Sacred Layer - Usage Guide

## Overview

ContextKeeper v3.0 provides AI-aware development context with immutable architectural constraints through the Sacred Layer system.

## Basic Workflow

### 1. Project Setup
```bash
# Create a new project
./scripts/rag_cli.sh projects create "E-commerce Platform" /path/to/project

# Focus on the project
./scripts/rag_cli.sh projects focus proj_abc123

# Check project status
./scripts/rag_cli.sh projects list
```

### 2. Sacred Plan Creation
```bash
# Create architectural plan
./scripts/rag_cli.sh sacred create proj_abc123 "Database Architecture" database_plan.md

# Create security plan
./scripts/rag_cli.sh sacred create proj_abc123 "Security Guidelines" security_plan.md

# List sacred plans
./scripts/rag_cli.sh sacred list proj_abc123
```

### 3. Plan Approval (2-Layer Verification)
```bash
# Generate verification code
./scripts/rag_cli.sh sacred approve plan_def456

# This will:
# 1. Generate time-based verification code
# 2. Verify SACRED_APPROVAL_KEY from environment
# 3. Make plan immutable once approved
```

### 4. Development with Drift Detection
```bash
# Check alignment with sacred plans
./scripts/rag_cli.sh sacred drift proj_abc123

# Query sacred context
./scripts/rag_cli.sh sacred query proj_abc123 "authentication approach"

# Get development context
./scripts/rag_cli.sh context export proj_abc123
```

## Claude Code Integration

### Using MCP Tools

Once configured, use these tools in Claude Code:

#### 1. **get_sacred_context**
```
Get architectural constraints for current project
/mcp get_sacred_context contextkeeper-sacred project_id=proj_abc123
```

#### 2. **check_sacred_drift**
```
Check if current development aligns with sacred plans
/mcp check_sacred_drift contextkeeper-sacred project_id=proj_abc123
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

### AI-Aware Development

When working with Claude Code:

1. **Start with Sacred Context**: Ask Claude to get the sacred context before making suggestions
2. **Check Drift Regularly**: Use drift detection to ensure alignment
3. **Query Decisions**: Use LLM-enhanced queries to understand past decisions
4. **Export Context**: Provide full context for complex discussions

## Advanced Features

### Git Activity Tracking
```bash
# View recent activity
./scripts/rag_cli.sh git activity proj_abc123

# Sync git activity with project knowledge
./scripts/rag_cli.sh git sync proj_abc123
```

### Decision and Objective Tracking
```bash
# Add architectural decision
./scripts/rag_cli.sh decisions add "Using microservices" "Better scalability" "architecture,scaling"

# Add development objective
./scripts/rag_cli.sh objectives add "Implement user authentication" high

# Complete objective
./scripts/rag_cli.sh objectives complete obj_123
```

### Continuous Monitoring
```bash
# Start continuous drift monitoring
./scripts/rag_cli.sh sacred monitor start proj_abc123

# Check monitoring status
./scripts/rag_cli.sh sacred monitor status

# Stop monitoring
./scripts/rag_cli.sh sacred monitor stop
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

### Sacred Plan Issues
```bash
# Check sacred plan status
./scripts/rag_cli.sh sacred status plan_abc123

# View plan approval history
./scripts/rag_cli.sh sacred history plan_abc123

# Recover from drift violations
./scripts/rag_cli.sh sacred drift proj_abc123 --fix
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

### Performance Optimisation
```bash
# Clear ChromaDB cache
rm -rf rag_knowledge_db/chroma_cache

# Optimise embeddings
./scripts/rag_cli.sh admin optimize-embeddings

# Check memory usage
./scripts/rag_cli.sh admin stats
```

## Best Practices

### Sacred Plan Creation
1. **Be Specific**: Include concrete technical decisions, not vague principles
2. **Version Control**: Sacred plans should be in git alongside code
3. **Review Process**: Have team review before approval
4. **Living Documents**: Update plans when architecture evolves

### AI Collaboration
1. **Context First**: Always provide sacred context before asking for code
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
./scripts/rag_cli.sh sacred drift $PROJECT_ID --fail-on-violation

# Export context for automated code review
./scripts/rag_cli.sh context export $PROJECT_ID --format json
```

### Monitoring and Alerts
```bash
# Set up drift detection alerts
./scripts/rag_cli.sh sacred monitor alert email "team@company.com"

# Integrate with Slack notifications
./scripts/rag_cli.sh sacred monitor alert slack "#dev-team"
```

For detailed API documentation, see [API_REFERENCE.md](../API_REFERENCE.md).
For installation help, see [INSTALLATION.md](INSTALLATION.md).