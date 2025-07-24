# ContextKeeper v3.0 Sacred Layer

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-16%2B-green.svg)](https://nodejs.org)

> AI-aware development context management with immutable architectural constraints

ContextKeeper is a RAG-powered development context awareness system that prevents AI agents from derailing from approved architectural plans through the Sacred Layer - an immutable plan storage system with 2-layer verification.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/lostmind008/contextkeeper.git
cd contextkeeper
./setup.sh

# Configure environment
cp .env.template .env
# Edit .env with your Google Cloud credentials and SACRED_APPROVAL_KEY

# Start Sacred Layer
python rag_agent.py start

# Create your first project
./scripts/rag_cli.sh projects create "My Project" /path/to/project
```

## ✨ Key Features

### 🛡️ Sacred Layer Protection
- **Immutable Plans**: Architectural constraints that cannot be modified once approved
- **2-Layer Verification**: Hash-based codes + environment key security
- **AI Guardrails**: Prevent AI agents from suggesting non-compliant changes

### 🎯 Intelligent Context Management
- **Multi-Project Support**: Isolated contexts for different projects
- **Git Integration**: Track development activity through git commits
- **Drift Detection**: Real-time monitoring of alignment with sacred plans

### 🔗 Claude Code Integration
- **8 MCP Tools**: Sacred-aware tools for seamless AI collaboration
- **Natural Language**: LLM-enhanced responses for technical queries
- **Real-time Context**: Automatic architectural constraint provision

## 📋 Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/INSTALLATION.md) | Complete setup instructions |
| [Usage Guide](docs/USAGE.md) | How to use ContextKeeper effectively |
| [API Reference](docs/api/API_REFERENCE.md) | Complete API documentation |
| [MCP Tools](docs/api/MCP_TOOLS_REFERENCE.md) | Claude Code integration guide |
| [Architecture](docs/ARCHITECTURE.md) | System design and components |

## 🏗️ Architecture

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Git Activity   │  │  Multi-Project  │  │  Sacred Layer   │
│  Tracker        │  │  RAG Agent      │  │  Manager        │
└─────────┬───────┘  └─────────┬───────┘  └─────────┬───────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│               ChromaDB Vector Storage                   │
│  • Project Collections (isolated)                      │
│  • Sacred Collections (immutable)                      │
│  • Decision & Objective Tracking                       │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Core Workflows

### Sacred Plan Management
```bash
# Create architectural plan
./scripts/rag_cli.sh sacred create proj_123 "Database Architecture" plan.md

# Approve with 2-layer verification
./scripts/rag_cli.sh sacred approve plan_abc123

# Check alignment
./scripts/rag_cli.sh sacred drift proj_123
```

### Claude Code Integration
```json
// Add to Claude Code MCP configuration
{
  "contextkeeper-sacred": {
    "type": "stdio",
    "command": "node",
    "args": ["/absolute/path/to/contextkeeper/mcp-server/enhanced_mcp_server.js"],
    "env": {"RAG_AGENT_URL": "http://localhost:5556"}
  }
}
```

## 📊 Project Structure

```
contextkeeper/
├── docs/                          # Documentation
│   ├── api/                      # API documentation
│   ├── guides/                   # User guides
│   ├── INSTALLATION.md           # Setup instructions
│   └── USAGE.md                  # Usage guide
├── examples/                      # Usage examples
├── mcp-server/                    # Claude Code integration
├── scripts/                       # CLI and setup scripts
├── tests/                         # Test suite
├── rag_agent.py                  # Main RAG orchestrator
├── sacred_layer_implementation.py # Sacred Layer core
├── git_activity_tracker.py       # Git integration
└── enhanced_drift_sacred.py      # Drift detection
```

## 🛠️ Development

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- Git
- Google Cloud account (for GenAI API)

### Running Tests
```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/sacred/ -v
```

### Contributing
We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📈 Use Cases

- **AI-Assisted Development**: Provide architectural context to AI coding assistants
- **Team Collaboration**: Shared architectural constraints across development teams  
- **Compliance Monitoring**: Ensure development aligns with approved designs
- **Knowledge Management**: Capture and preserve architectural decisions

## 🔐 Security

- **Local-only storage**: No data sent to external services (except Google GenAI for embeddings)
- **Immutable plans**: Sacred plans cannot be modified once approved
- **2-layer verification**: Prevents unauthorized plan changes
- **Audit trail**: Complete history of all sacred operations

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [ChromaDB](https://github.com/chroma-core/chroma) for vector storage
- Powered by [Google GenAI](https://ai.google.dev/) for embeddings
- Integrated with [Claude Code](https://claude.ai/code) via MCP

## 📞 Support

- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/lostmind008/contextkeeper/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/lostmind008/contextkeeper/discussions)

---

**Made with ❤️ by [LostMindAI](https://github.com/lostmind008)**