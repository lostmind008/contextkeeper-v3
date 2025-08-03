# LostMind AI - ContextKeeper v3.0 Usage Guide
## Overview
ContextKeeper v3.0 provides AI-aware development context with beautiful Three.js dashboard, real-time analytics, and comprehensive project management through an intuitive interface.
## 🎨 Beautiful Dashboard
### Access the Dashboard
Navigate to [http://localhost:5556/dashboard](http://localhost:5556/dashboard) to access the stunning Three.js analytics dashboard.
![Dashboard Preview](https://via.placeholder.com/800x400?text=Three.js+Analytics+Dashboard)
**Key Features:**
- **Real-time 3D Visualizations**: Interactive project metrics with particle effects
- **Dark/Light Mode**: Toggle with the moon/sun icon
- **Export Capabilities**: Generate PDF reports, PNG snapshots, or JSON data
- **Responsive Design**: Optimized for desktop and mobile viewing
- **Performance Metrics**: Live updates every 5 seconds
## 🚀 Quick Start Commands
### Start the System
```bash
# Activate environment and start
source venv/bin/activate
python rag_agent.py start
# Verify health
curl http://localhost:5556/health
```
### Project Management
```bash
# Create new project
./scripts/rag_cli_v2.sh projects create myapp /path/to/myapp
# List all projects
./scripts/rag_cli_v2.sh projects list
# Switch active project
./scripts/rag_cli_v2.sh projects focus myapp
```
### Sacred Layer Operations
```bash
# Create sacred plan
./scripts/rag_cli_v2.sh sacred create proj_123 "Auth Architecture" auth_plan.md
# Approve plan (requires 2-layer verification)
./scripts/rag_cli_v2.sh sacred approve plan_abc123
# Check architectural drift
./scripts/rag_cli_v2.sh sacred drift proj_123
```
## 🎯 Advanced Usage Patterns
### Analytics Dashboard Features
**Navigation:**
- Click project cards to drill down into details
- Use the search bar to filter projects by name or status
- Toggle metrics display with the settings panel
**Export Options:**
- **PDF Report**: Complete project analytics with charts
- **PNG Snapshot**: High-resolution dashboard image
- **JSON Data**: Raw analytics data for external tools
**Keyboard Shortcuts:**
- `Ctrl/Cmd + R`: Refresh dashboard data
- `Ctrl/Cmd + D`: Toggle dark/light mode
- `Ctrl/Cmd + E`: Open export menu
- `Ctrl/Cmd + S`: Save current view settings
### Sacred Layer Best Practices
**Creating Effective Sacred Plans:**
1. **Be Specific**: Define exact architectural constraints
2. **Include Rationale**: Explain why the decision was made
3. **Set Boundaries**: Clearly define what can and cannot change
4. **Verification Steps**: Include how to check compliance
**Example Sacred Plan Structure:**
```markdown
# Sacred Plan: API Authentication
## Context
We need consistent authentication across all API endpoints.
## Decision
Implement OAuth2 with JWT tokens for all authenticated endpoints.
## Constraints
- All tokens must expire within 1 hour
- Refresh tokens valid for 7 days maximum  
- No plaintext password storage
## Implementation
- Use passport.js middleware
- Store tokens in Redis
- Implement refresh token rotation
## Verification
- Check all endpoints require authentication header
- Verify token expiration handling
- Audit password storage methods
```
### Multi-Project Workflows
**Bulk Operations:**
```bash
# Update all projects
./scripts/rag_cli_v2.sh projects bulk-update /path/to/projects/
# Compare projects
./scripts/rag_cli_v2.sh projects compare project1 project2
# Export all project data
./scripts/rag_cli_v2.sh analytics export-all --format json
```
**Project Templates:**
```bash
# Create from template
./scripts/rag_cli_v2.sh projects create-from-template react-app myapp
# Save as template
./scripts/rag_cli_v2.sh projects save-template myapp react-template
```
## 🔍 Query Optimization
### Natural Language Queries
**Effective Query Patterns:**
```bash
# Good: Specific and contextual
./scripts/rag_cli_v2.sh ask "How does the JWT middleware validate tokens in the auth module?"
# Better: Include file context
./scripts/rag_cli_v2.sh ask "In middleware/auth.js, how are expired tokens handled?"
# Best: Combine with AI enhancement
./scripts/rag_cli_v2.sh ask --llm "Explain the authentication flow and suggest improvements"
```
**Query Types:**
- **Code Search**: Find specific functions, classes, or patterns
- **Architecture Questions**: Understand system design and relationships
- **Change Impact**: Assess effects of proposed modifications
- **Best Practices**: Get recommendations for improvements
### API Query Examples
**Basic REST API Usage:**
```bash
# Health check
curl http://localhost:5556/health
# Basic query
curl -X POST http://localhost:5556/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Find all user management functions", "k": 10}'
# AI-enhanced query
curl -X POST http://localhost:5556/query_llm \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain the database schema design", "project_id": "proj_123"}'
```
**Sacred Layer API:**
```bash
# Query sacred plans
curl -X POST http://localhost:5556/sacred/query \
  -H "Content-Type: application/json" \
  -d '{"query": "authentication plans", "project_id": "proj_123"}'
# Check drift status
curl -X POST http://localhost:5556/sacred/drift \
  -H "Content-Type: application/json" \
  -d '{"project_id": "proj_123"}'
```
## 📊 Analytics & Monitoring
### Dashboard Metrics
**Project Health Indicators:**
- **Code Coverage**: Percentage of codebase indexed and searchable
- **Sacred Compliance**: Alignment with approved architectural plans
- **Query Performance**: Average response times and accuracy
- **Git Activity**: Recent commits, branches, and development velocity
**Real-time Updates:**
- Dashboard refreshes every 5 seconds
- Notifications for drift detection
- Live project status indicators
- Performance alerts
### Export & Reporting
**Automated Reports:**
```bash
# Generate weekly report
./scripts/rag_cli_v2.sh analytics report --weekly --format pdf
# Custom date range
./scripts/rag_cli_v2.sh analytics report --from 2024-01-01 --to 2024-01-31
# Specific metrics
./scripts/rag_cli_v2.sh analytics report --metrics "compliance,performance,coverage"
```
## 🛠️ Integration Patterns
### Claude Code MCP Integration
**Available Tools:**
- `get_sacred_context`: Retrieve approved architectural plans
- `check_sacred_drift`: Validate changes against sacred plans
- `query_with_llm`: Enhanced contextual queries
- `intelligent_search`: Semantic code search
- `export_development_context`: Complete project context
**Usage in Claude Code:**
```bash
# These tools appear automatically in Claude Code when ContextKeeper is running
# Example usage within Claude Code:
# "Use the intelligent_search tool to find authentication-related code"
# "Check if my changes comply with sacred plans using check_sacred_drift"
```
### CI/CD Integration
**Pre-commit Hooks:**
```bash
# Check sacred compliance before commit
./scripts/rag_cli_v2.sh sacred drift $(git rev-parse --show-toplevel)
if [ $? -ne 0 ]; then
  echo "⚠️  Sacred plan drift detected. Review changes."
  exit 1
fi
```
**GitHub Actions Example:**
```yaml
name: ContextKeeper Sacred Compliance
on: [push, pull_request]
jobs:
  sacred-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check Sacred Compliance
        run: |
          source venv/bin/activate
          ./scripts/rag_cli_v2.sh sacred drift ${{ github.workspace }}
```
## 🎨 Customization Options
### Dashboard Themes
**Built-in Themes:**
- **Dark Mode**: Sleek dark interface with neon accents
- **Light Mode**: Clean bright interface with subtle shadows
- **Auto Mode**: Follows system preference
**Custom Styling:**
- Modify `static/css/dashboard.css` for custom themes
- Particle effects configurable via `static/js/dashboard.js`
- Color schemes defined in CSS custom properties
### Query Enhancement
**Custom Embeddings:**
```bash
# Configure in .env
EMBEDDING_MODEL=custom-model-name
EMBEDDING_DIMENSIONS=1536
```
**Response Formatting:**
```bash
# Customize response templates
cp templates/response_template.md custom_template.md
# Edit custom_template.md
export RESPONSE_TEMPLATE=custom_template.md
```
## 🔧 Troubleshooting & Performance
### Common Issues
**Dashboard Not Loading:**
```bash
# Check if static files are served correctly
curl http://localhost:5556/static/css/dashboard.css
# Verify Three.js library availability
ls static/js/three.min.js
```
**Slow Query Performance:**
```bash
# Check database size
du -sh chroma_db/
# Optimize embeddings
./scripts/rag_cli_v2.sh maintenance optimize-embeddings
# Clear cache
./scripts/rag_cli_v2.sh maintenance clear-cache
```
### Performance Optimization
**Resource Management:**
- Monitor memory usage: `ps aux | grep rag_agent`
- Database cleanup: `./scripts/rag_cli_v2.sh maintenance cleanup --days 30`
- Index optimization: `./scripts/rag_cli_v2.sh maintenance reindex`
**Query Optimization:**
- Use specific queries over broad searches
- Limit result count with `-k` parameter
- Enable query caching for repeated questions
## 🎯 Production Deployment
### Configuration
**Environment Variables:**
```env
# Production settings
RAG_AGENT_HOST=0.0.0.0
RAG_AGENT_PORT=5556
ENVIRONMENT=production
DEBUG=false
# Security
SACRED_APPROVAL_KEY=your-secure-key-here
JWT_SECRET=your-jwt-secret
# Performance
QUERY_CACHE_SIZE=1000
EMBEDDING_BATCH_SIZE=100
```
**Security Considerations:**
- Use HTTPS in production
- Implement rate limiting
- Secure API endpoints
- Regular key rotation
### Monitoring
**Health Checks:**
```bash
# Automated health monitoring
while true; do
  curl -f http://localhost:5556/health || echo "Service down at $(date)"
  sleep 60
done
```
**Log Analysis:**
```bash
# Monitor logs
tail -f rag_agent.log | grep ERROR
# Performance metrics
./scripts/rag_cli_v2.sh analytics performance --live
```
---
## 🚀 Next Steps
1. **Explore the Dashboard**: Navigate to the Three.js analytics interface
2. **Create Sacred Plans**: Establish architectural governance
3. **Integrate with CI/CD**: Automate compliance checking
4. **Customize Themes**: Adapt the interface to your preferences
5. **Monitor Performance**: Use analytics for optimization
**Pro Tips:**
- Use sacred plans for critical architectural decisions
- Export regular reports for stakeholder updates
- Leverage Claude Code integration for enhanced development
- Monitor drift alerts for architectural compliance
*ContextKeeper v3.0 - Beautiful, intelligent, and powerful development context management.* 🎨✨