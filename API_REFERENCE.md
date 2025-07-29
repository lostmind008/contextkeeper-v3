# API Reference

**Base URL**: `http://localhost:5556`
**Status**: ✅ All endpoints operational and tested

## Core Endpoints

### Project Management
```http
GET    /projects              # List all projects
POST   /projects              # Create new project
PUT    /projects/<id>/focus    # Set active project
PUT    /projects/<id>/pause    # Pause project
PUT    /projects/<id>/resume   # Resume project
PUT    /projects/<id>/archive  # Archive project
```

### Knowledge & Context
```http
POST   /query                 # Query knowledge base (raw results)
POST   /query_llm             # Query with natural language responses
POST   /decisions             # Add decision
POST   /objectives            # Add objective  
POST   /context/export        # Export context for AI agents
GET    /briefing              # Get project status
```

## Sacred Layer Endpoints

### Sacred Plan Management
```http
POST   /sacred/plans          # Create sacred plan
POST   /sacred/plans/<id>/approve  # Approve plan (2-layer verification)
GET    /sacred/plans          # List sacred plans
POST   /sacred/query          # Query sacred plans
GET    /sacred/drift/<project_id>  # Check drift status
```

### Git Integration
```http
GET    /projects/<id>/git/activity  # Get Git activity
POST   /projects/<id>/git/sync      # Sync from Git
```

### Health & Status
```http
GET    /health                      # System health check
GET    /sacred/health               # Sacred layer health
```

## Request/Response Examples

### Create Sacred Plan
```bash
curl -X POST http://localhost:5556/sacred/plans \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "proj_123",
    "title": "Authentication Architecture", 
    "file_path": "/path/to/plan.md"
  }'
```

### Approve Sacred Plan (2-Layer Verification)
```bash
curl -X POST http://localhost:5556/sacred/plans/plan_abc123/approve \
  -H "Content-Type: application/json" \
  -d '{
    "approver": "sumitm1",
    "verification_code": "abc12345-20250724",
    "secondary_verification": "your-secret-key"
  }'
```

### Check Drift Status
```bash
curl "http://localhost:5556/sacred/drift/proj_123?hours=24"
```

### Query with LLM Enhancement
```bash
curl -X POST http://localhost:5556/query_llm \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the sacred layer?",
    "k": 5,
    "project_id": "optional_project_id"
  }'
```

**Response**:
```json
{
  "question": "What is the sacred layer?",
  "answer": "The Sacred Layer is a system designed to ensure that approved plans cannot be modified...",
  "sources": ["/path/to/source1.py", "/path/to/source2.py"],
  "context_used": 5,
  "timestamp": "2025-07-24T16:30:17.357805"
}
```

### Compare Raw vs Enhanced Query
```bash
# Raw query (returns JSON chunks)
curl -X POST http://localhost:5556/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the sacred layer?", "k": 5}'

# Enhanced query (returns natural language)
curl -X POST http://localhost:5556/query_llm \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the sacred layer?", "k": 5}'
```

## MCP Server Integration (Phase 3)

### MCP Tools Available
The ContextKeeper MCP server provides 8 sacred-aware tools for Claude Code integration:

1. **get_sacred_context** - Retrieve sacred architectural plans
2. **check_sacred_drift** - Real-time violation detection
3. **query_with_llm** - Natural language responses from knowledge base
4. **export_development_context** - Complete project context
5. **get_development_context** - Comprehensive project status
6. **intelligent_search** - Semantic search across plans and code
7. **create_sacred_plan** - Sacred plan creation workflow
8. **health_check** - System status verification

### MCP Server Configuration
**Location**: `mcp-server/enhanced_mcp_server.js`  
**Protocol**: STDIO for Claude Code compatibility  
**Port**: Connected to Sacred Layer on port 5556  

### Claude Code Integration Configuration
Add this to your Claude Code MCP configuration:
```json
"contextkeeper-sacred": {
  "type": "stdio",
  "command": "node",
  "args": [
    "/Users/sumitm1/Documents/myproject/Ongoing Projects/ContextKeeper Pro/ContextKeeper v3 Upgrade/contextkeeper/mcp-server/enhanced_mcp_server.js"
  ],
  "env": {
    "RAG_AGENT_URL": "http://localhost:5556"
  }
}
```

### MCP Tool Usage Examples

#### Get Sacred Context
```json
{
  "tool": "get_sacred_context",
  "arguments": {
    "project_id": "proj_123",
    "query": "authentication architecture"
  }
}
```

#### Check Sacred Drift
```json
{
  "tool": "check_sacred_drift", 
  "arguments": {
    "project_id": "proj_123"
  }
}
```

#### Create Sacred Plan
```json
{
  "tool": "create_sacred_plan",
  "arguments": {
    "project_id": "proj_123",
    "title": "Database Schema",
    "content": "# Database Architecture\n\nApproved schema design..."
  }
}
```