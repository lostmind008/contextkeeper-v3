# 🧠 ContextKeeper: RAG-Powered Development Context Awareness System
### *by LostMindAI*

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/lostmind008/contextkeeper/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

**ContextKeeper** is an enhanced AI agent that maintains persistent knowledge across multiple projects and coding sessions using vector search, intelligent code indexing, and comprehensive project management.

## 🌟 What's New in v3.0?

ContextKeeper v3.0 introduces the Sacred Layer and supports:
- **Sacred Layer**: Immutable architectural plans with 2-layer verification
- **Drift Detection**: Real-time monitoring of code alignment with sacred plans  
- **MCP Integration**: 8 sacred-aware tools for Claude Code integration
- **Multi-Project Management**: Track multiple projects simultaneously with independent configurations
- **Project Lifecycle**: Create, pause, resume, archive, and focus on different projects
- **Decision Tracking**: Record and retrieve architectural decisions with reasoning
- **Objective Management**: Set development goals and track completion
- **Context Export**: Generate rich context for AI assistants (Claude Code, GitHub Copilot)
- **Git Integration**: Track development activity through commits and changes
- **Project Isolation**: Each project maintains its own knowledge base

### Core Features (from v1.0)
- **Remembers Everything**: Indexes your code and documentation automatically
- **Answers Questions**: Search your entire codebase semantically
- **Stays Current**: Watches files for changes and updates its knowledge
- **Protects Secrets**: Automatically redacts API keys and sensitive data

Built with ChromaDB for vector storage and Google's Gemini for embeddings.

## Quick Start (5 minutes)

### 1. Install Dependencies

First, clone the repository:
```bash
git clone https://github.com/lostmind008/contextkeeper.git
cd contextkeeper
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

### 3. Start the Agent

No manual configuration needed! With v3.0, you can dynamically add projects:
```bash
# Start the agent
./rag_cli.sh start

# Create your first project
./rag_cli.sh projects create "My Project" /path/to/project

# The agent will automatically watch the project directories
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


## 🚀 Features

- 🔍 **Automatic Code Indexing**: Watches your project files and updates knowledge base
- 🛡️ **Security**: Automatically redacts API keys and sensitive data
- 🧠 **Smart Chunking**: Preserves code structure for better search results
- 📡 **API Access**: Query via HTTP API at http://localhost:5555
- 🎯 **Project-Agnostic**: Works with any development project
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

## 🔌 MCP Integration (v3.0)

ContextKeeper now includes a powerful MCP (Model Context Protocol) server that integrates directly with Claude Code, providing real-time development context and sacred plan protection.

### Quick Setup

1. **Add to Claude Code MCP Configuration**:
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

2. **Start ContextKeeper with Sacred Layer**:
   ```bash
   cd contextkeeper
   source venv/bin/activate
   python rag_agent.py start
   ```

### Available MCP Tools

The ContextKeeper MCP server provides 8 sacred-aware tools:

- **🔍 get_sacred_context** - Retrieve sacred architectural plans
- **⚠️ check_sacred_drift** - Real-time violation detection  
- **💬 query_with_llm** - Natural language responses from knowledge base
- **📋 export_development_context** - Complete project context
- **📊 get_development_context** - Comprehensive project status
- **🔎 intelligent_search** - Semantic search across plans and code
- **📝 create_sacred_plan** - Sacred plan creation workflow
- **❤️ health_check** - System status verification

### Benefits

- **AI Safety**: Sacred plans prevent AI agent derailment
- **Context Preservation**: Rich development context via MCP
- **Real-time Monitoring**: Drift detection operational
- **Natural Language**: Conversational explanations of technical decisions
- **Violation Prevention**: Sacred plan compliance enforced

## Next Steps

1. Update the `watch_dirs` in `rag_agent.py` to point to your actual project directories
2. Add the contextkeeper directory to your PATH for easy access
3. Consider setting up as a system service for automatic startup

---

## 🏢 About LostMindAI

**ContextKeeper** is developed and maintained by [LostMindAI](https://github.com/lostmind008), focused on building intelligent development tools that enhance programmer productivity through AI-powered context awareness.

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

Copyright 2025 LostMindAI. Apache 2.0 License provides patent protection and requires preservation of copyright and license notices.

## 🙏 Acknowledgments

Built with love by the LostMindAI team. Special thanks to the open-source community for the amazing tools that make this project possible: ChromaDB, Google Gemini, and Flask.
