# LostMind AI - ContextKeeper v3.0

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-16%2B-green.svg)](https://nodejs.org)

**ContextKeeper** is a revolutionary AI-powered development context management system. It provides intelligent context tracking, architectural decision management, and AI-driven insights to maintain clarity and consistency across your development projects.

> **✅ CURRENT STATUS (August 2025)**: v3.0.0 - Production Ready! Features a real-time interactive dashboard, simplified onboarding, and powerful governance analytics.

## ✨ Key Features

- **🎨 Real-Time Interactive Dashboard**: A beautiful and responsive UI with live updates via WebSockets.
- **🚀 One-Step Project Onboarding**: Create and index a new project with a single, simple command.
- **🏛️ UI-Based Governance**: Manage and approve Sacred Plans directly from the dashboard.
- **📊 Powerful Governance Analytics**: Get detailed metrics on your project's architectural health.
- **🤖 LLM Integration**: Natural language responses powered by Google Gemini.
- **🔍 Global Search**: Instantly find projects, plans, and decisions from the dashboard.
- **🎯 Multi-Project Support**: Complete project isolation with zero cross-contamination.
- **🔐 Auto Security**: Automatically redacts API keys and sensitive data.

## 🚀 Quick Start (2 minutes!)

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/lostmind008/contextkeeper-pro-v3.git
cd contextkeeper-pro-v3/contextkeeper

# Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the template and edit the new .env file
cp .env.template .env
# Add your Google API key and define a SACRED_APPROVAL_KEY (required; no default)
```

The `SACRED_APPROVAL_KEY` environment variable must be set in your shell or `.env` file. There is no default value and
ContextKeeper will raise an error if this key is missing.

### 3. Start ContextKeeper
```bash
# Start the main application server
python src/rag_agent.py server
```
Keep this service running. It powers both the CLI and the dashboard.

### 4. Add Your First Project
```bash
# Open a new terminal window
# Use the new, streamlined 'project add' command
./scripts/contextkeeper.sh project add "/path/to/your/code" "My Awesome Project"
```
This single command creates the project and fully indexes its contents, showing you a progress bar.

### 5. Explore the Dashboard
Open your browser and navigate to `http://localhost:5556/analytics_dashboard_live.html`. You'll see your project, fully indexed and ready to go!

## 🏗️ Architecture

The v3 architecture is designed for scalability and real-time interaction.

```
┌─────────────────┐      ┌────────────────┐      ┌──────────────────┐
│   Dashboard     ├──────┤  WebSockets  ├──────┤   RAG Agent API  │
│ (React/HTML)    │      │ (Socket.IO)  │      │  (Flask Server)  │
└─────────────────┘      └──────┬───────┘      └─────────┬────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│ src/core/project_manager.py ├──┤  src/sacred/...  ├──┤ src/ck_analytics/... │
└─────────────────────────────┘  └──────────────────┘  └──────────────────────┘
              │                       │                       │
              └───────────────┐       │       ┌───────────────┘
                              ▼       ▼       ▼
                       ┌───────────────────────────┐
                       │   ChromaDB Vector Store   │
                       └───────────────────────────┘
```
- **Real-Time Layer**: The dashboard communicates with the backend via WebSockets, allowing for instant UI updates.
- **Analytics Service**: A new, dedicated service (`src/ck_analytics/`) calculates and serves governance and project metrics.
- **Modular `src` Layout**: The codebase is now organized into a `src` directory for better maintainability.

## 📂 Project Structure
The project structure has been refactored for clarity.

```
contextkeeper-v3/
├── src/
│   ├── ck_analytics/
│   ├── core/
│   ├── sacred/
│   └── tracking/
├── scripts/
│   └── contextkeeper.sh  # Main CLI script
├── tests/
├── docs/
│   ├── USER_GUIDE.md
│   ├── ARCHITECTURE.md
│   └── api/
│       └── API_REFERENCE.md
├── analytics_dashboard_live.html
├── rag_agent.py
└── README.md
```

## 📚 Documentation
For more detailed information, please refer to the following documents:
- **[USER_GUIDE.md](docs/USER_GUIDE.md)**: Comprehensive instructions for all features.
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: A technical deep-dive into the system's design.
- **[API_REFERENCE.md](docs/api/API_REFERENCE.md)**: Complete documentation for all API endpoints and WebSocket events.

## 📜 License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
