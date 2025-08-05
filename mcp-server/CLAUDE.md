# CLAUDE.md - MCP Server

This file provides context for Claude Code when working in this directory.

## Directory Purpose
Contains the Node.js MCP (Model Context Protocol) server that bridges Claude Code with the ContextKeeper v3 RAG system. This server exposes tools for intelligent search, sacred layer management, and development context retrieval.

## Key Files
- **enhanced_mcp_server.js** - Main MCP server implementation with tool definitions
- **package.json** - Node.js dependencies and scripts
- **package-lock.json** - Locked dependency versions

## Dependencies
- **From parent**: RAG Agent (rag_agent.py) must be running on localhost:5556
- **External**: Node.js runtime, MCP protocol libraries
- **Network**: HTTP communication with Flask backend

## Common Tasks
- Start MCP server: `node enhanced_mcp_server.js`
- Debug tool responses: Check server logs for tool execution
- Update tool definitions: Modify tool handlers in enhanced_mcp_server.js
- Test connectivity: Verify Flask backend is accessible

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/
- Related: Main RAG agent (../rag_agent.py), Tests (../tests/), Scripts (../scripts/)