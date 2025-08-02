# ContextKeeper v3.0 - Common Issues & Solutions

## 🚨 Most Common Issues

### 1. "No project context specified" Error

**Problem**: When running queries, you get an error saying no project context is specified.

**Solution**:
```bash
# Follow this exact sequence:
1. Create project: ./scripts/rag_cli_v2.sh projects create "name" /path
2. Focus project: ./scripts/rag_cli_v2.sh projects focus <project_id>
3. Index files: python rag_agent.py ingest --path /path
4. Query: ./scripts/rag_cli_v2.sh ask "your question"
```

### 2. No Results from Queries

**Problem**: Queries return empty results even though project exists.

**Root Cause**: Files haven't been indexed after project creation.

**Solution**:
```bash
# Must index files after creating project
python rag_agent.py ingest --path /path/to/project

# This can take 2-3 minutes for large projects
# Check progress in logs: tail -f rag_agent.log
```

### 3. Wrong CLI Version

**Problem**: Commands don't work or show outdated help.

**Solution**:
- Use `rag_cli_v2.sh` NOT `rag_cli.sh`
- The v2 CLI has project management commands
- Update scripts: `chmod +x scripts/*.sh`

### 4. Port Already in Use

**Problem**: Agent fails to start with "address already in use" error.

**Solution**:
```bash
# Check what's using port 5556
lsof -i :5556

# Kill the process if needed
kill -9 <PID>

# Or use a different port
python rag_agent.py server --port 5557
```

### 5. Indexing Timeout

**Problem**: Ingestion times out after 2 minutes.

**Solution**:
- This is normal for large projects
- The indexing continues in background
- Check completion in logs: `grep "Ingested" rag_agent.log`
- For very large projects, index in batches

### 6. Google API Errors

**Problem**: 403 errors or authentication failures.

**Solution**:
```bash
# Check your .env file
cat .env | grep GOOGLE_API_KEY

# Verify API key is valid
# Ensure Gemini API is enabled in Google Cloud Console
# Check quota limits haven't been exceeded
```

## 📋 Quick Diagnostic Checklist

Run these commands to diagnose issues:

```bash
# 1. Check agent is running
curl http://localhost:5556/health

# 2. List projects
./scripts/rag_cli_v2.sh projects list

# 3. Check focused project
curl http://localhost:5556/projects | jq '.focused_project'

# 4. Test query endpoint
curl -X POST http://localhost:5556/query_llm \
  -H "Content-Type: application/json" \
  -d '{"question": "test", "k": 5}'

# 5. Check logs for errors
tail -50 rag_agent.log | grep ERROR
```

## 🔧 Environment Issues

### Virtual Environment Not Active

**Symptoms**: Import errors, module not found

**Fix**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Denied Errors

**Fix**:
```bash
chmod +x scripts/*.sh
chmod +x setup.sh
```

## 📞 Getting Help

If these solutions don't work:

1. Check the detailed logs: `tail -100 rag_agent.log`
2. Look for specific error messages
3. Ensure all dependencies are installed
4. Verify your project path exists and contains files
5. Check GitHub issues for similar problems

## 🎯 Prevention Tips

1. Always follow the create → focus → index → query workflow
2. Wait for indexing to complete before querying
3. Use absolute paths for projects
4. Keep your API keys secure and valid
5. Monitor the rag_agent.log for issues