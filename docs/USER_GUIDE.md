# ContextKeeper v3.0: The Ultimate User Guide

Welcome to ContextKeeper! This guide provides everything you need to know to harness the full power of the system, from initial setup to advanced workflows.

## 1. 🚀 Getting Started: Your First 5 Minutes

This section will get you up and running with a fully indexed project.

### Step 1: Installation
```bash
# 1. Clone the repository
git clone https://github.com/lostmind008/contextkeeper-v3.git
cd contextkeeper-v3

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.template .env
# Edit .env and add your keys:
# GEMINI_API_KEY=your-gemini-api-key
# SACRED_APPROVAL_KEY=a-long-secret-key-you-create
```

### Step 2: Start the ContextKeeper Service
```bash
# Start the main application
python src/rag_agent.py server
```
This command starts the backend server on `http://localhost:5556`. Keep this terminal window running.

### Step 3: Create and Index Your First Project (One-Step Onboarding)
The new streamlined workflow makes adding a project effortless.

```bash
# Open a NEW terminal window and run:
./scripts/contextkeeper.sh project add "/path/to/your/code" "My Awesome Project"
```
This single command will:
1.  Create the project in ContextKeeper.
2.  Start indexing all relevant files, showing you a real-time progress bar.
3.  Notify you upon completion.

### Step 4: Explore the Dashboard
Open your browser and navigate to:
`http://localhost:5556/analytics_dashboard_live.html`

You will see your new project card, now "Active" and ready for interaction.

## 2. 核心工作流程：日常使用 (Core Workflows: Day-to-Day Usage)

### Interacting with Your Project
Once your project is indexed, you can interact with it via the CLI or the real-time dashboard.

#### Using the Interactive Dashboard
The dashboard is the central hub for managing your projects.

*   **Global Search:** Use the search bar at the top to instantly find projects, Sacred Plans, or decisions.
*   **Focusing a Project:** Simply click on a project card. This will highlight it and load its specific governance data in the "Sacred Plans" section.
*   **Real-Time Feedback:** The dashboard uses WebSockets for instant updates. When you add a new project or a colleague focuses on one, the UI updates automatically without needing a refresh. Indexing progress is also shown in real-time.

#### Using the Command-Line Interface (CLI)
The CLI is powerful for scripting and quick actions.

*   **Focus on a Project:**
    ```bash
    # If you know the ID
    ./scripts/contextkeeper.sh project focus <project_id>

    # If you don't, a fuzzy finder will appear!
    ./scripts/contextkeeper.sh project focus
    ```
*   **Ask a Question:**
    ```bash
    # Get a quick answer from the knowledge base
    ./scripts/contextkeeper.sh query "How does the caching layer work?"

    # Get a detailed explanation from the LLM
    ./scripts/contextkeeper.sh query --llm "Explain our authentication strategy"
    ```

## 3. 🏛️ Governance with Sacred Plans

Sacred Plans are the heart of ContextKeeper's governance features, allowing you to define and enforce architectural rules.

### Managing Plans from the Dashboard
This is the recommended and most intuitive way to manage Sacred Plans.

1.  **Focus a Project:** Click on a project card in the dashboard.
2.  **View Plans:** The "Sacred Plans Governance" section will appear, listing all plans for that project.
3.  **Approve a Plan:**
    *   Click the "Approve" button next to a "draft" plan.
    *   A secure modal will appear.
    *   Enter your name, the verification code from the plan file, and your `SACRED_APPROVAL_KEY`.
    *   Acknowledge the security warning and confirm.
    *   The plan's status will update to "Approved" in real-time.

### Managing Plans from the CLI
For scripting or terminal-native users.

*   **Create a Plan:**
    1.  Write your architectural rules in a Markdown file (e.g., `api_design.md`).
    2.  Submit it to ContextKeeper:
        ```bash
        ./scripts/contextkeeper.sh sacred create <project_id> "API Design Guidelines" api_design.md
        ```
*   **Approve a Plan:**
    ```bash
    ./scripts/contextkeeper.sh sacred approve <plan_id>
    # You will be prompted for your name, verification code, and approval key.
    ```

## 4. 📊 Analytics and Insights

ContextKeeper now includes a powerful analytics service to provide insights into your project's governance health.

*   **Accessing Metrics:** Use the `/analytics/sacred` endpoint to get detailed metrics.
    ```bash
    curl http://localhost:5556/analytics/sacred
    ```
*   **What it Tracks:** The service calculates the total number of sacred plans, their approval status, and provides an overall alignment score.
*   **Data Flow:** The `AnalyticsService` uses a `SacredMetricsCalculator` to compute these metrics, which are then cached for 5 minutes to ensure high performance.

## 5. 🔌 API and Integration

### Key API Endpoints
*   `POST /projects/create-and-index`: Creates and indexes a project asynchronously.
*   `GET /tasks/{task_id}`: Checks the status of a background task (like indexing).
*   `GET /search?q=...`: Powers the global search on the dashboard.
*   `GET /analytics/sacred`: Provides governance metrics.
*   `POST /sacred/plans/{id}/approve`: Approves a Sacred Plan.

### Real-Time Events (WebSockets)
Your client can listen for the following events from the Socket.IO server:
*   `indexing_progress`: `{ "project_id": "...", "progress": 25 }`
*   `indexing_complete`: `{ "project_id": "..." }`
*   `indexing_failed`: `{ "project_id": "...", "error": "..." }`
*   `focus_changed`: `{ "project_id": "..." }`

## 6. 🔧 Troubleshooting

*   **Server won't start:** Check if port 5556 is already in use (`lsof -i :5556`).
*   **No results from queries:** Ensure project indexing is complete. Check the project card on the dashboard for "Active" status.
*   **Plan approval fails:** Double-check your `SACRED_APPROVAL_KEY` in the `.env` file and ensure you are entering the correct verification code.

---

**Happy coding with ContextKeeper! 🚀**
