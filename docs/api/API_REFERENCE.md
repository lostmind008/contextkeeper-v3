# API Reference

**Base URL**: `http://localhost:5556`  
**Status**: ✅ All endpoints operational (August 2025)
**Version**: 3.1.0

## 1. Core Endpoints

### Project Management
```http
# Unified project creation and indexing (asynchronous)
POST   /projects/create-and-index
# Body: { "name": "...", "root_path": "..." }
# Returns 202 Accepted: { "task_id": "...", "project_id": "..." }

# Check status of a background task (like indexing)
GET    /tasks/<task_id>
# Returns: { "status": "indexing", "progress": 25 }

# List all projects
GET    /projects

# Set active project (emits 'focus_changed' WebSocket event)
POST   /projects/<project_id>/focus
```

### Knowledge & Context
```http
# Global search across projects, plans, and decisions
GET    /search?q=<query>

# Query knowledge base with LLM enhancement
POST   /query_llm
# Body: { "question": "...", "project_id": "..." }

# Add an architectural decision
POST   /decision
# Body: { "decision": "...", "reasoning": "...", "project_id": "..." }
```

## 2. Sacred Layer & Governance

### Sacred Plan Management
```http
# Create a new sacred plan
POST   /sacred/plans
# Body: { "project_id": "...", "title": "...", "file_path": "..." }

# Approve a sacred plan (2-layer verification)
POST   /sacred/plans/<plan_id>/approve
# Body: { "approver": "...", "verification_code": "...", "secondary_verification": "..." }

# List sacred plans for a project
GET    /sacred/plans?project_id=<project_id>

# Query sacred plans
POST   /sacred/query
# Body: { "query": "...", "project_id": "..." }

# Check for architectural drift
GET    /sacred/drift/<project_id>
```

### Analytics
```http
# Get detailed governance and sacred metrics
GET    /analytics/sacred
```

## 3. Real-Time Events (WebSockets)

Connect to the Socket.IO server at the base URL. The server emits the following events:

### `indexing_progress`
Fired periodically during project indexing.
- **Payload**: `{ "project_id": string, "progress": int }`
- **Example**: `{ "project_id": "proj_123", "progress": 45 }`

### `indexing_complete`
Fired when a project has been successfully indexed.
- **Payload**: `{ "project_id": string }`
- **Example**: `{ "project_id": "proj_123" }`

### `indexing_failed`
Fired if an error occurs during indexing.
- **Payload**: `{ "project_id": string, "error": string }`
- **Example**: `{ "project_id": "proj_123", "error": "Permission denied" }`

### `focus_changed`
Fired when a project's focus is changed via the API.
- **Payload**: `{ "project_id": string }`
- **Example**: `{ "project_id": "proj_456" }`


## 4. Health & Status
```http
# System health check
GET    /health
```

## 5. Request/Response Examples

### Create & Index a Project
```bash
curl -X POST http://localhost:5556/projects/create-and-index \
  -H "Content-Type: application/json" \
  -d '{"name": "WebApp", "root_path": "/path/to/webapp"}'
```
**Response (202 Accepted)**:
```json
{
  "task_id": "task_abc123",
  "project_id": "proj_xyz789"
}
```

### Check Task Status
```bash
curl http://localhost:5556/tasks/task_abc123
```
**Response**:
```json
{
  "status": "indexing",
  "progress": 75
}
```

### Global Search
```bash
curl "http://localhost:5556/search?q=auth"
```
**Response**:
```json
{
  "projects": [{ "id": "proj_1", "name": "Authentication Service" }],
  "plans": [{ "plan_id": "plan_2", "title": "OAuth2 Authentication Plan" }],
  "decisions": []
}
```

### Get Sacred Analytics
```bash
curl http://localhost:5556/analytics/sacred
```
**Response**:
```json
{
  "overall_metrics": {
    "total_plans": 10,
    "compliance_rate": 80.0
  },
  "project_metrics": [
    {
      "project_name": "WebApp",
      "adherence_score": 95.5
    }
  ]
}
```
