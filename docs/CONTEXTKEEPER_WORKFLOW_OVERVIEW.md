# ContextKeeper Workflow Overview

**Generated**: 2025-07-29  
**Version**: 3.0.0 Enhanced

## System Architecture

ContextKeeper is a RAG (Retrieval-Augmented Generation) powered development context system that helps AI assistants understand your codebase and development history.

### Key Components

1. **MCP Server** (`enhanced_mcp_server.js`)
   - Provides 9 tools to Claude Code and other AI assistants
   - Communicates with RAG Agent on port 5556
   - Implements 5-minute caching for expensive operations

2. **RAG Agent** (`rag_agent.py`)
   - Python Flask application running on port 5556
   - Manages vector database (ChromaDB) for semantic search
   - Integrates with Google Gemini for AI enhancements

3. **Storage Systems**
   - **ChromaDB**: Vector database for semantic search
   - **Project Configs**: JSON files in `~/.rag_projects/`
   - **Git Repository**: Direct git integration for activity tracking

## The 9 MCP Tools

### Context & Analysis Tools
1. **get_development_context** - Comprehensive project status with git activity, objectives, and decisions
2. **intelligent_search** - Semantic search across code, decisions, and documentation
3. **analyze_git_activity** - Detailed git commit and branch analysis
4. **check_development_drift** - Monitors if development aligns with objectives

### Project Management Tools
5. **manage_objectives** - Add, update, complete, and list project objectives
6. **track_decision** - Record architectural decisions with reasoning
7. **suggest_next_action** - AI-powered suggestions for what to work on next

### Development Support Tools
8. **get_code_context** - Find relevant code patterns for new features
9. **daily_briefing** - Comprehensive overview of all projects

## Typical Development Workflow

### 1. Start Your Day
```javascript
// Get comprehensive briefing
daily_briefing()

// Or get specific project context
get_development_context({
  project_id: "myproject",
  hours: 48
})
```

### 2. Plan Your Work
```javascript
// Check what needs doing
suggest_next_action()

// Search for relevant code
intelligent_search({
  query: "authentication implementation"
})

// Get implementation guidance
get_code_context({
  feature_description: "add password reset"
})
```

### 3. Track Progress
```javascript
// Add new objective
manage_objectives({
  action: "add",
  title: "Implement password reset",
  priority: "high"
})

// Record decisions
track_decision({
  decision: "Use email-based password reset",
  reasoning: "Most secure and user-friendly approach"
})
```

### 4. Monitor Alignment
```javascript
// Check if on track
check_development_drift()

// Review git activity
analyze_git_activity()
```

## Data Flow

1. **Ingestion**: Code files are processed and embedded using Google Gemini
2. **Storage**: Embeddings stored in ChromaDB, metadata in JSON configs
3. **Query**: Natural language queries trigger semantic search
4. **Enhancement**: Results enhanced with Gemini LLM for better context
5. **Delivery**: MCP tools deliver formatted responses to AI assistants

## Setup Requirements

1. **RAG Agent** must be running:
   ```bash
   cd contextkeeper
   source venv/bin/activate
   python rag_agent.py start
   ```

2. **MCP Server** configured in Claude Code:
   ```bash
   claude mcp add contextkeeper "node /path/to/enhanced_mcp_server.js" \
     --env RAG_AGENT_URL=http://localhost:5556
   ```

3. **Google Cloud** credentials for Gemini API access

## Key Features

- **Semantic Search**: Find code by meaning, not just keywords
- **Context Awareness**: Understands project history and decisions
- **Git Integration**: Tracks development activity automatically
- **Objective Management**: Keep development aligned with goals
- **AI Enhancement**: Natural language responses powered by Gemini
- **Caching**: 5-minute cache for expensive operations

## Visual Diagrams

See the `/docs/diagrams/` folder for:
- `ContextKeeper Architecture Overview.png` - System architecture
- `MCP Tools Workflow.png` - Tool interaction patterns
- `ContextKeeper Data Flow.png` - How data moves through the system
- `MCP Tools Overview.png` - Mind map of all 9 tools

## Important Notes

1. The documentation previously referenced a "Sacred Layer" MCP server with different tools. The actual implementation is the "Enhanced" MCP server with the 9 tools listed above.

2. There is no separate Sacred Layer JavaScript implementation - the sacred functionality exists in the Python backend but is not exposed through the current MCP tools.

3. All 9 tools are fully functional and integrate with the RAG Agent backend for rich development context.

## Getting Started

1. Start the RAG Agent
2. Ensure MCP server is configured in Claude Code
3. Begin with `daily_briefing` to understand project state
4. Use `suggest_next_action` for AI-guided development
5. Track progress with `manage_objectives` and `track_decision`

This system provides a comprehensive development context layer that makes AI assistants truly understand your codebase and development patterns.