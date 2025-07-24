# API Reference

**Base URL**: `http://localhost:5555`

## v2.0 Endpoints (Current)

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

## v3.0 Sacred Endpoints (Target)

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

## Request/Response Examples

### Create Sacred Plan
```bash
curl -X POST http://localhost:5555/sacred/plans \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "proj_123",
    "title": "Authentication Architecture", 
    "file_path": "/path/to/plan.md"
  }'
```

### Approve Sacred Plan (2-Layer Verification)
```bash
curl -X POST http://localhost:5555/sacred/plans/plan_abc123/approve \
  -H "Content-Type: application/json" \
  -d '{
    "approver": "sumitm1",
    "verification_code": "abc12345-20250724",
    "secondary_verification": "your-secret-key"
  }'
```

### Check Drift Status
```bash
curl "http://localhost:5555/sacred/drift/proj_123?hours=24"
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