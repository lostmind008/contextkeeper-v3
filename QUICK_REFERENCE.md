# RAG Agent Quick Reference

## 🚀 Getting Started

1. **First Time Setup**:
   ```bash
   cd contextkeeper
   ./setup.sh
   ```

2. **Edit Configuration**:
   - Edit `.env` with your Google Cloud credentials
   - Update `rag_agent.py` CONFIG section with your project paths

3. **Start the Agent**:
   ```bash
   python rag_agent.py start
   ```

## 📝 Common Commands

```bash
# Query knowledge base
./rag_cli.sh ask "What payment system are we using?"

# Add a decision
./rag_cli.sh add "Using Stripe for payments"

# Morning briefing
./rag_cli.sh morning

# Check status
./rag_cli.sh status

# View logs
./rag_cli.sh logs
```

## 🎯 Sacred Layer Commands (v3.0)

```bash
# Create sacred plan
./rag_cli.sh sacred create <project_id> "Plan Title" plan.md

# Approve sacred plan (requires 2-layer verification)
./rag_cli.sh sacred approve <plan_id>

# Check drift from sacred plans
./rag_cli.sh sacred drift <project_id>

# Query sacred plans
./rag_cli.sh sacred query <project_id> "search query"
```

## 🔧 API Access

```bash
# Query via API
curl -X POST http://localhost:5555/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show Gemini integration code"}'

# Add decision via API
curl -X POST http://localhost:5555/decision \
  -H "Content-Type: application/json" \
  -d '{"decision": "Using Gemini 2.5", "context": "Better multimodal support"}'
```

## 🐛 Troubleshooting

- **Agent not starting**: Check `.env` file and Google Cloud credentials
- **No results**: Make sure your project directories exist in CONFIG
- **Permission errors**: Run `chmod +x rag_cli.sh setup.sh`
- **Import errors**: Activate virtual environment: `source venv/bin/activate`

## 💡 Tips

1. The agent watches your files automatically - just save and it updates
2. All API keys and passwords are automatically redacted
3. Use the morning briefing to quickly get context when starting work
4. Add decisions as you make them - they'll help Claude stay consistent

## 📚 Files in this directory

- `rag_agent.py` - Main agent code
- `rag_cli.sh` - Command line wrapper
- `sacred_layer_implementation.py` - Sacred Layer core functionality
- `git_activity_tracker.py` - Git integration for activity tracking
- `enhanced_drift_sacred.py` - Drift detection system
- `requirements.txt` - Python dependencies
- `setup.sh` - Quick setup script
- `.env.template` - Environment variable template
- `README.md` - Detailed documentation

Happy coding! 🚀
