# ContextKeeper v3.0 Upgrade: AI Agent TODO List

This document outlines the step-by-step tasks required to upgrade ContextKeeper from v2.0 to v3.0, incorporating the "Sacred Layer" and other key enhancements. Follow each step methodically, modifying the specified files as described.

## Phase 0: Preparation & Foundation

**Goal:** Prepare the development environment, add new dependencies, and set up the testing framework.

*   [ ] **Update Dependencies:** Add the following required packages to `requirements.txt`:
    ```
    gitpython>=3.1.0
    scikit-learn>=1.3.0
    numpy>=1.24.0
    flask-socketio>=5.3.0
    langchain-text-splitters>=0.0.1
    pytest>=7.4.0
    pytest-asyncio>=0.21.0
    ```
*   [ ] **Install Dependencies:** Run `pip install -r requirements.txt` in your virtual environment.
*   [ ] **Create Test Structure:** Create the necessary directories for testing:
    ```bash
    mkdir -p tests/sacred tests/git tests/drift
    touch tests/__init__.py
    ```
*   [ ] **Update Environment Configuration:** Add the new key for the Sacred Layer's secondary approval to your `.env` file.
    ```
    # .env
    export SACRED_APPROVAL_KEY='your-secret-approval-key'
    ```

## Phase 1: Git-Based Activity Tracking

**Goal:** Replace file-watching with more reliable Git-based tracking.

*   [ ] **Create `git_activity_tracker.py`:** Create a new file named `git_activity_tracker.py` and populate it with the full contents of the provided artifact.
*   [ ] **Integrate Git Tracker into Main Agent (`rag_agent.py`):**
    *   **Import necessary classes:**
        ```python
        # rag_agent.py
        from git_activity_tracker import GitActivityTracker, GitIntegratedRAGAgent
        ```
    *   **Initialize the Git integration in `ProjectKnowledgeAgent.__init__`:**
        ```python
        # In ProjectKnowledgeAgent.__init__ method
        self.git_integration = GitIntegratedRAGAgent(self, self.project_manager)
        for project in self.project_manager.get_active_projects():
            try:
                self.git_integration.init_git_tracking(project.project_id)
                logger.info(f"Git tracking initialized for {project.name}")
            except Exception as e:
                logger.warning(f"Could not initialize git tracking for {project.name}: {e}")
        ```
*   [ ] **Add Git API Endpoints (`rag_agent.py`):**
    *   **Add the following endpoints to the `RAGServer._setup_routes` method:**
        ```python
        @self.app.route('/projects/<project_id>/git/activity', methods=['GET'])
        def get_git_activity(project_id):
            hours = int(request.args.get('hours', 24))
            if project_id not in self.agent.git_integration.git_trackers:
                return jsonify({'error': 'Git not initialized for project'}), 404
            
            activity = self.agent.git_integration.git_trackers[project_id].analyze_activity(hours)
            # Note: The dataclasses from git_activity_tracker need to be JSON serializable.
            # A helper function might be needed here if they are not.
            return jsonify(activity.__dict__)

        @self.app.route('/projects/<project_id>/git/sync', methods=['POST'])
        async def sync_from_git(project_id):
            try:
                await self.agent.git_integration.update_project_from_git(project_id)
                return jsonify({'status': 'synced', 'timestamp': datetime.now().isoformat()})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        ```

## Phase 2: Sacred Layer & Enhanced Drift Detection

**Goal:** Implement the core "Sacred Layer" for immutable, verifiable plans and enhance drift detection to compare against these plans.

*   [ ] **Create `sacred_layer_implementation.py`:** Create the file and populate it with the full contents of the provided artifact.
*   [ ] **Create `enhanced_drift_sacred.py`:** Create the file and populate it with the full contents of the provided artifact.
*   [ ] **Integrate Sacred Layer into Main Agent (`rag_agent.py`):**
    *   **Import necessary classes:**
        ```python
        # rag_agent.py
        from sacred_layer_implementation import SacredIntegratedRAGAgent
        from enhanced_drift_sacred import add_sacred_drift_endpoint
        ```
    *   **Initialize the Sacred Layer integration in `ProjectKnowledgeAgent.__init__`:**
        ```python
        # In ProjectKnowledgeAgent.__init__ method
        self.sacred_integration = SacredIntegratedRAGAgent(self)
        ```
    *   **Add Sacred Layer API Endpoints to `RAGServer._setup_routes`:**
        ```python
        # Add these new endpoints
        @self.app.route('/sacred/plans', methods=['POST'])
        async def create_sacred_plan():
            data = request.json
            result = await self.agent.sacred_integration.create_sacred_plan(
                data['project_id'],
                data['title'],
                data.get('file_path') or data.get('content')
            )
            return jsonify(result)

        @self.app.route('/sacred/plans/<plan_id>/approve', methods=['POST'])
        async def approve_sacred_plan(plan_id):
            data = request.json
            result = await self.agent.sacred_integration.approve_sacred_plan(
                plan_id,
                data['approver'],
                data['verification_code'],
                data['secondary_verification']
            )
            return jsonify(result)

        @self.app.route('/sacred/query', methods=['POST'])
        async def query_sacred_plans():
            data = request.json
            result = await self.agent.sacred_integration.query_sacred_context(
                data['project_id'],
                data['query']
            )
            return jsonify(result)
        ```
    *   **Register the Sacred Drift Endpoint in `RAGServer.__init__`:**
        ```python
        # In RAGServer.__init__, after self._setup_routes()
        add_sacred_drift_endpoint(
            self.app, 
            self.agent, 
            self.agent.project_manager,
            self.agent.sacred_integration.sacred_manager
        )
        ```
*   [ ] **Integrate Sacred CLI Commands:**
    *   Create the file `sacred_cli_integration.sh` from the artifact.
    *   Modify your main CLI script (`rag_cli.sh` or a successor) to include the sacred commands. Add this to the main `case` statement:
        ```bash
        # In main CLI script
        source ./sacred_cli_integration.sh # Add this near the top

        # In the main case statement for command handling
        sacred|s)
            shift
            handle_sacred "$@"
            ;;
        ```

## Phase 3: MCP Server Integration

**Goal:** Expose sacred-aware context securely to AI tools like Claude Code.

*   [ ] **Create `enhanced_mcp_server.js`:** Create the file and populate it from the artifact.
*   [ ] **Verify `package.json`:** Ensure `mcp-server/package.json` includes `@modelcontextprotocol/sdk` and `node-fetch`.
*   [ ] **Install Node Dependencies:** Run `npm install` inside the `mcp-server` directory.

## Phase 4: Analytics Dashboard

**Goal:** Create a visual interface for monitoring project health and sacred plan adherence.

*   [ ] **Create `analytics_dashboard.html`:** Create the file and populate it from the artifact.
*   [ ] **Add Analytics Endpoint (`rag_agent.py`):** The dashboard needs an endpoint to fetch data. Add a basic one to `RAGServer._setup_routes`:
    ```python
    @self.app.route('/analytics/summary', methods=['GET'])
    def get_analytics_summary():
        # This should be expanded with real data from git/drift analysis
        summary = self.agent.project_manager.get_project_summary()
        # Add more analytics data here in the future
        return jsonify(summary)
    ```

## Phase 5: Finalization and Documentation

**Goal:** Update all user-facing documentation to reflect the v3.0 changes.

*   [ ] **Update `CHANGELOG.md`:** Add a new entry for `[3.0.0]` detailing all the new features (Git Integration, Sacred Layer, Drift Detection, etc.).
*   [ ] **Update `README.md`:**
    *   Update the version badge to 3.0.0.
    *   Add sections explaining the Sacred Layer and Git-based tracking.
    *   Add the new `sacred` commands to the usage examples.
*   [ ] **Update `CLAUDE.md`:**
    *   Update the project overview to describe the Sacred Layer.
    *   Add the new `sacred` CLI commands to the "Key Commands" section.
    *   Describe the new MCP server tools (`get_sacred_context`, etc.).
