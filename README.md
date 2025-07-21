# 🧠 RAG Knowledge Agent - My First AI Agent!

A sophisticated AI agent that maintains persistent knowledge across coding sessions using vector search and intelligent code indexing.

## 🌟 What is this?

The RAG Knowledge Agent is an intelligent assistant that:
- **Remembers Everything**: Indexes your code and documentation automatically
- **Answers Questions**: Search your entire codebase semantically
- **Tracks Decisions**: Record architectural choices and find them later
- **Stays Current**: Watches files for changes and updates its knowledge
- **Protects Secrets**: Automatically redacts API keys and sensitive data

Built with ChromaDB for vector storage and Google's Gemini for embeddings.

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

Edit the `CONFIG` section in `rag_agent.py` to point to your project directories:
```python
"watch_dirs": [
    "/path/to/your/project/agents",
    "/path/to/your/project/backend", 
    "/path/to/your/project/tools"
]
```

**Note**: The agent is currently configured to watch the LostMindAI YouTube Analyzer project.

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

## 🚀 Features

- 🔍 **Automatic Code Indexing**: Watches your project files and updates knowledge base
- 🛡️ **Security**: Automatically redacts API keys and sensitive data
- 🧠 **Smart Chunking**: Preserves code structure for better search results
- 📡 **API Access**: Query via HTTP API at http://localhost:5555
- 🎯 **Project-Specific**: Tailored for your YouTube Analyzer development
- ⚡ **Fast Search**: Vector similarity search finds relevant code instantly
- 📝 **Multiple Formats**: Supports .py, .js, .jsx, .ts, .tsx, .md, .json, .yaml

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌───────────────┐
│   Your Code     │────▶│  RAG Agent   │────▶│   ChromaDB    │
│   (Watched)     │     │  (Indexer)   │     │  (Vectors)    │
└─────────────────┘     └──────────────┘     └───────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │ Google GenAI │
                        │ (Embeddings) │
                        └──────────────┘
```

## 📡 API Documentation

### Query Endpoint
```bash
POST http://localhost:5555/query
Content-Type: application/json

{
  "question": "What authentication system are we using?",
  "k": 5  # Number of results (optional, default: 10)
}
```

### Add Decision Endpoint
```bash
POST http://localhost:5555/decision
Content-Type: application/json

{
  "decision": "Using Redis for caching",
  "context": "Need fast session storage",
  "importance": "high"
}
```

### Health Check
```bash
GET http://localhost:5555/health
```

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
