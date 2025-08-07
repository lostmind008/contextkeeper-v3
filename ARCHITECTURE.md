# ContextKeeper v3.0: System Architecture

This document provides a technical overview of the ContextKeeper v3.0 system architecture, reflecting its state as of August 2025.

## 1. Core Philosophy

The architecture is designed around a central, stateful **RAG (Retrieval-Augmented Generation) Agent** that serves as the single source of truth for all development context. All interactions, whether from the CLI, the dashboard, or other AI tools, are mediated through this agent. This ensures consistency and prevents state fragmentation.

## 2. High-Level Diagram

```
                               +-------------------------+
                               |   End Users & Tools     |
                               +-----------+-------------+
                                           |
                  +------------------------+------------------------+
                  |                        |                        |
         +--------v--------+      +--------v--------+      +--------v--------+
         |   Interactive   |      |  CLI Scripts    |      |  External AI    |
         |    Dashboard    |      | (contextkeeper) |      |   (Claude)      |
         +--------+--------+      +--------+--------+      +--------+--------+
                  |                        |                        |
+-----------------|------------------------+------------------------|-----------------+
| Real-Time Layer |                        |                        |                 |
| (WebSockets)    |                        |                        |                 |
+-----------------|------------------------+------------------------|-----------------+
                  |                        |                        |
                  |       +----------------+----------------+       |
                  |       |      HTTP RESTful API           |       |
                  |       +----------------+----------------+       |
                  |                        |                        |
         +--------v--------+      +--------v--------+      +--------v--------+
         | Real-Time Comms |      | RAG Agent (Flask)       |      | MCP Server      |
         |  (Socket.IO)    |      | (rag_agent.py)          |      | (Node.js)       |
         +-----------------+      +--------+--------+      +-----------------+
                                           |
                 +-------------------------+-------------------------+
                 |                         |                         |
        +--------v--------+       +--------v--------+       +--------v--------+
        |  `src/core`     |       |  `src/sacred`   |       |  `src/ck_analytics`|
        | Project Mgmt    |       | Governance      |       | Metrics Service |
        +--------+--------+       +--------+--------+       +--------+--------+
                 |                         |                         |
                 |                         |                         |
                 +-------------------------+-------------------------+
                                           |
                                  +--------v--------+
                                  |  ChromaDB       |
                                  |  Vector Store   |
                                  +-----------------+

```

## 3. Key Components

### Frontend / User-Facing
*   **Interactive Dashboard (`analytics_dashboard_live.html`)**: A single-page application providing a real-time, interactive view of the system. It communicates with the backend primarily via WebSockets for live updates and uses the REST API for initial data loading and actions.
*   **CLI (`scripts/contextkeeper.sh`)**: A powerful bash script for terminal-based interaction. It communicates directly with the RAG Agent's REST API.

### Backend / Service Layer
*   **RAG Agent (`rag_agent.py`)**: The core of the system. This is a Flask application that serves both a REST API and a WebSocket server. It orchestrates all business logic, from project management to RAG queries.
*   **Real-Time Layer (`Flask-SocketIO`)**: Integrated into the RAG Agent, this layer pushes real-time updates to connected clients (like the dashboard) for events such as indexing progress or focus changes.
*   **MCP Server (`mcp-server/enhanced_mcp_server.js`)**: A Node.js server that acts as a bridge for external AI tools like Claude, exposing ContextKeeper's functionality via the Model-Context-Protocol (MCP).

### Core Logic (`src/` directory)
The Python codebase is organized into a modular `src/` directory:
*   **`src/core`**: Manages fundamental entities like projects and decisions.
*   **`src/sacred`**: Implements the architectural governance features (Sacred Plans, drift detection).
*   **`src/ck_analytics`**: Contains the new analytics service for calculating governance and project metrics.
*   **`src/tracking`**: Handles Git activity tracking and other event monitoring.

### Data Storage
*   **ChromaDB**: The vector database used for all semantic search capabilities. Each project has its own isolated collection to prevent data leakage.
*   **File System**: Project configurations and Sacred Plans are stored as JSON and Markdown files on the local file system, making them version-controllable.

## 4. Data Flows

### Project Onboarding (Unified Workflow)
1.  A user runs `./scripts/contextkeeper.sh project add ...` or uses the dashboard modal.
2.  A `POST` request is sent to the `/projects/create-and-index` endpoint on the RAG Agent.
3.  The agent immediately creates the project configuration and returns a `202 Accepted` response with a unique `task_id`.
4.  A background task is spawned to start indexing the project files.
5.  During indexing, the `ingest_directory` function emits `indexing_progress` events via WebSocket.
6.  The dashboard listens for these events and updates the UI in real-time. The CLI polls the `/tasks/{task_id}` endpoint to show its progress bar.
7.  Upon completion, an `indexing_complete` event is emitted.

### Real-Time Dashboard Updates
1.  The dashboard opens a persistent WebSocket connection to the RAG Agent.
2.  When an action occurs (e.g., a project is focused via the CLI), the corresponding API endpoint (`/projects/{id}/focus`) emits a `focus_changed` event.
3.  All connected dashboard clients receive this event and update their UI accordingly (e.g., by highlighting the focused project card).

### Analytics Calculation
1.  A request is made to the `GET /analytics/sacred` endpoint.
2.  The RAG Agent routes this to the `AnalyticsService` in `src/ck_analytics/analytics_service.py`.
3.  The `AnalyticsService` uses the `SacredMetricsCalculator` to gather data from the `SacredLayerManager` and `ProjectManager`.
4.  It calculates metrics like plan counts, approval rates, and adherence scores.
5.  The results are cached for 5 minutes to ensure subsequent requests are fast.
6.  The calculated metrics are returned as a JSON response.

## 5. Security Considerations
*   **Authentication & Authorization**: Currently, the system relies on the security of the local machine it runs on. There is no user-based authentication layer.
*   **Secret Management**: API keys and the `SACRED_APPROVAL_KEY` are managed via an `.env` file.
*   **Data Redaction**: The `SecurityFilter` class automatically redacts sensitive patterns (like API keys) from file content before it is indexed.
*   **Path Filtering**: A robust `PathFilter` prevents the ingestion of sensitive directories (`.git`, `node_modules`) and files.
