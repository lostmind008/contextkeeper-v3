# RAG Knowledge Agent - Setup & Usage Guide

## Quick Start (5 minutes)

### 1. Install Dependencies

First, make sure you're in the rag-agent directory:
```bash
cd ~/rag-agent
```

Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

Install required packages:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with your Google Cloud credentials:
```bash
# Google Cloud Configuration
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_VERTEXAI=True
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account.json
```

### 3. Configure the Agent

Edit the `CONFIG` section in `rag_agent.py` to point to your YouTube Analyzer project:
```python
"watch_dirs": [
    "./youtube-analyzer-app",  # Update these paths
    "./backend",
    "./frontend"
]
```

### 4. Make Scripts Executable

```bash
chmod +x rag_cli.sh
```

### 5. Start the Agent

```bash
python rag_agent.py start
```

Or use the CLI wrapper:
```bash
./rag_cli.sh start
```

## Usage Examples

### Query the knowledge base:
```bash
./rag_cli.sh ask "What authentication system did I use?"
```

### Add a decision:
```bash
./rag_cli.sh add "Using CrewAI for multi-agent system"
```

### Get morning briefing:
```bash
./rag_cli.sh morning
```

### YouTube Analyzer specific queries:
```bash
./rag_cli.sh youtube gemini  # Show Gemini integration
./rag_cli.sh youtube agents  # List all agents
```

## Features

- 🔍 **Automatic Code Indexing**: Watches your project files and updates knowledge base
- 🛡️ **Security**: Automatically redacts API keys and sensitive data
- 🧠 **Smart Chunking**: Preserves code structure for better search results
- 📡 **API Access**: Query via HTTP API at http://localhost:5555
- 🎯 **Project-Specific**: Tailored for your YouTube Analyzer development

## Troubleshooting

If the agent doesn't start:
1. Check your Google Cloud credentials in `.env`
2. Ensure you have Python 3.8+ installed
3. Check logs: `tail -f rag_agent.log`

## Integration with Claude

Add to your Claude Custom Instructions:
```
When context is near limit, query http://localhost:5555/query for project context.
```

## Next Steps

1. Update the `watch_dirs` in `rag_agent.py` to point to your actual project directories
2. Add the rag-agent directory to your PATH for easy access
3. Consider setting up as a system service for automatic startup
