# How to Use ContextKeeper v3.0 - Quick User Guide

This guide shows you how to use ContextKeeper to its full potential at the current stage of development (August 2025).

## 🚀 Getting Started

### Step 1: Start ContextKeeper
```bash
# Always use these commands
cd /Users/sumitm1/contextkeeper-pro-v3/contextkeeper
source venv/bin/activate
python rag_agent.py server  # Use 'server' not 'start' to avoid crashes
```

### Step 2: Open the Dashboard
```bash
# Open in your browser
open http://localhost:5556/analytics_dashboard_live.html
```

You'll see:
- Beautiful Three.js animated background
- Project statistics
- Your projects grid
- Purple chat button (bottom-right)

## 📁 Creating and Setting Up a Project

### Method 1: Dashboard (Partially Working)
1. Click "Create New Project" button
2. Enter project name AND path (e.g., `/Users/sumitm1/my-code-project`)
3. Click Create
4. **IMPORTANT**: Dashboard creates the project but does NOT index files

### Method 2: CLI (Recommended for Now)
```bash
# Create project
./scripts/rag_cli_v2.sh projects create "My Project" /path/to/your/code

# Note the project_id returned (e.g., proj_abc123)

# Focus on the project
./scripts/rag_cli_v2.sh projects focus proj_abc123

# Index the files (CRITICAL - DO NOT SKIP!)
python rag_agent.py ingest --path /path/to/your/code
```

## 💬 Using the Chat Interface

### From Dashboard:
1. Click the purple chat button (bottom-right)
2. Chat panel slides in from the right
3. Use quick actions or type questions
4. Examples:
   - "What is this project about?"
   - "How does authentication work?"
   - "Show me the database schema"

### Via API:
```bash
curl -X POST http://localhost:5556/query_llm \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain the main functionality",
    "k": 5,
    "project_id": "proj_abc123"
  }'
```

## ⚠️ Critical Requirements for Good Results

### 1. Your Project Must Have Real Code
- ✅ Good: Python, JavaScript, TypeScript, Markdown files
- ❌ Bad: Binary files, images, videos, base64 data

### 2. Always Index After Creation
- Creating a project does NOT index files
- Must run: `python rag_agent.py ingest --path /your/project`
- Without indexing, chat responses will be empty/poor

### 3. Focus on the Right Project
- Multiple projects? Make sure you're querying the right one
- Check focused project in dashboard stats

## 🎯 Current Limitations & Workarounds

### What Works Well:
- ✅ Chat interface with history
- ✅ Project creation (with manual path entry)
- ✅ Query your indexed code
- ✅ Beautiful dashboard UI
- ✅ Event tracking

### What's Missing:
- ❌ File browser for project paths (must type manually)
- ❌ Automatic indexing (must run command)
- ❌ Re-index button in UI (use CLI)
- ❌ Progress indicators
- ❌ Project status (can't see if indexed)

## 📝 Complete Workflow Example

```bash
# 1. Start ContextKeeper
cd /Users/sumitm1/contextkeeper-pro-v3/contextkeeper
source venv/bin/activate
python rag_agent.py server

# 2. Create a new project (CLI method)
./scripts/rag_cli_v2.sh projects create "MyApp" /Users/sumitm1/my-app
# Returns: Created project proj_xyz789

# 3. Focus on it
./scripts/rag_cli_v2.sh projects focus proj_xyz789

# 4. Index the files (ESSENTIAL!)
python rag_agent.py ingest --path /Users/sumitm1/my-app
# Wait for completion (2-5 minutes)

# 5. Open dashboard
open http://localhost:5556/analytics_dashboard_live.html

# 6. Click chat button and ask questions!
```

## 🆘 Troubleshooting

### "The provided context states that it is from project..."
- **Cause**: Project has no indexed content
- **Fix**: Run indexing command

### Chat gives generic/empty responses
- **Cause**: Wrong project focused or no meaningful code files
- **Fix**: Check project has .py/.js/.md files, re-index

### Create Project shows success but project doesn't appear
- **Cause**: Dashboard doesn't auto-refresh
- **Fix**: Refresh the page manually

### Server crashes with "Segmentation fault"
- **Fix**: Use `python rag_agent.py server` not `start`

## 📚 For Developers

Remember to update `LOGBOOK.md` after any changes:
```bash
# Get timestamp
mcp__time__get_current_time --timezone "Australia/Sydney"

# Add to LOGBOOK.md:
[2025-08-04 HH:MM AEST] - [Component] - [Action] - [Details]
```

---

**Note**: This represents the current state as of August 2025. The system is functional but requires some manual steps. Future updates will add file browsers, auto-indexing, and better project management UI.