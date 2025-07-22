#!/usr/bin/env node

/**
 * MCP Server for Enhanced RAG Agent
 * Provides Claude Code and other MCP clients with access to your development context
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';

const RAG_AGENT_BASE_URL = 'http://localhost:5555';

class RAGMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'rag-knowledge-agent',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
  }

  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'get_project_context',
            description: 'Get comprehensive context for the current or specified project including recent activity, objectives, and potential drift',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Optional project ID. If not provided, uses focused or active project'
                },
                include_terminal_activity: {
                  type: 'boolean',
                  description: 'Whether to include recent terminal commands (default: true)',
                  default: true
                },
                include_drift_analysis: {
                  type: 'boolean', 
                  description: 'Whether to include objective drift analysis (default: true)',
                  default: true
                }
              }
            }
          },
          {
            name: 'list_projects',
            description: 'List all projects with their current status (active, paused, archived, focused)',
            inputSchema: {
              type: 'object',
              properties: {
                status_filter: {
                  type: 'string',
                  enum: ['active', 'paused', 'archived', 'focused', 'all'],
                  description: 'Filter projects by status (default: active)',
                  default: 'active'
                }
              }
            }
          },
          {
            name: 'search_knowledge',
            description: 'Search the RAG knowledge base across all tracked projects',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Natural language query to search for in codebase and documentation'
                },
                project_id: {
                  type: 'string',
                  description: 'Optional: limit search to specific project'
                },
                max_results: {
                  type: 'number',
                  description: 'Maximum number of results to return (default: 10)',
                  default: 10
                }
              },
              required: ['query']
            }
          },
          {
            name: 'get_project_objectives',
            description: 'Get current objectives for a project and their completion status',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Project ID to get objectives for'
                },
                include_completed: {
                  type: 'boolean',
                  description: 'Whether to include completed objectives (default: false)',
                  default: false
                }
              }
            }
          },
          {
            name: 'add_project_decision',
            description: 'Record an important project decision for future reference',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Project ID to record decision for'
                },
                decision: {
                  type: 'string',
                  description: 'The decision that was made'
                },
                context: {
                  type: 'string',
                  description: 'Context and reasoning behind the decision'
                },
                importance: {
                  type: 'string',
                  enum: ['low', 'normal', 'high', 'critical'],
                  description: 'Importance level of the decision (default: normal)',
                  default: 'normal'
                }
              },
              required: ['project_id', 'decision']
            }
          },
          {
            name: 'check_objective_drift',
            description: 'Analyze if recent development activity aligns with project objectives',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Project ID to analyze'
                },
                hours: {
                  type: 'number',
                  description: 'Number of hours to analyze (default: 24)',
                  default: 24
                }
              }
            }
          },
          {
            name: 'get_recent_terminal_activity',
            description: 'Get recent terminal commands and activity for context',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Optional: filter by project ID'
                },
                hours: {
                  type: 'number',
                  description: 'Hours of history to retrieve (default: 8)',
                  default: 8
                },
                focused_only: {
                  type: 'boolean',
                  description: 'Only show activity from focused terminals (default: false)',
                  default: false
                }
              }
            }
          },
          {
            name: 'set_project_focus',
            description: 'Set focus on a specific project to prioritize its context',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Project ID to focus on'
                }
              },
              required: ['project_id']
            }
          },
          {
            name: 'add_objective',
            description: 'Add a new objective to a project',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Project ID to add objective to'
                },
                objective: {
                  type: 'string',
                  description: 'The objective to add'
                }
              },
              required: ['project_id', 'objective']
            }
          }
        ]
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'get_project_context':
            return await this.getProjectContext(args);
          
          case 'list_projects':
            return await this.listProjects(args);
          
          case 'search_knowledge':
            return await this.searchKnowledge(args);
          
          case 'get_project_objectives':
            return await this.getProjectObjectives(args);
          
          case 'add_project_decision':
            return await this.addProjectDecision(args);
          
          case 'check_objective_drift':
            return await this.checkObjectiveDrift(args);
          
          case 'get_recent_terminal_activity':
            return await this.getRecentTerminalActivity(args);
          
          case 'set_project_focus':
            return await this.setProjectFocus(args);
          
          case 'add_objective':
            return await this.addObjective(args);
          
          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Unknown tool: ${name}`
            );
        }
      } catch (error) {
        if (error instanceof McpError) {
          throw error;
        }
        throw new McpError(
          ErrorCode.InternalError,
          `Tool execution failed: ${error.message}`
        );
      }
    });
  }

  async ragRequest(endpoint, method = 'GET', data = null) {
    try {
      const options = {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      };

      if (data) {
        options.body = JSON.stringify(data);
      }

      const response = await fetch(`${RAG_AGENT_BASE_URL}${endpoint}`, options);
      
      if (!response.ok) {
        throw new Error(`RAG Agent API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      throw new McpError(
        ErrorCode.InternalError,
        `Failed to communicate with RAG Agent: ${error.message}`
      );
    }
  }

  async getProjectContext(args) {
    const { project_id, include_terminal_activity = true, include_drift_analysis = true } = args;
    
    const context = await this.ragRequest(`/context${project_id ? `/${project_id}` : ''}`);
    
    // Format the context for AI consumption
    let formattedContext = `# Project Context\n\n`;
    
    if (context.project) {
      formattedContext += `**Project:** ${context.project.name}\n`;
      formattedContext += `**Status:** ${context.project.status}\n`;
      formattedContext += `**Root Path:** ${context.project.root_path}\n`;
      formattedContext += `**Last Active:** ${context.project.last_active}\n\n`;
    }

    if (context.objectives_status) {
      formattedContext += `## Current Objectives\n`;
      formattedContext += `**Progress:** ${context.objectives_status.completed}/${context.objectives_status.total} completed\n\n`;
      
      if (context.objectives_status.current && context.objectives_status.current.length > 0) {
        formattedContext += `**Active Objectives:**\n`;
        context.objectives_status.current.forEach((obj, index) => {
          formattedContext += `${index + 1}. ${obj.text}\n`;
        });
        formattedContext += `\n`;
      }
    }

    if (include_terminal_activity && context.recent_commands) {
      formattedContext += `## Recent Terminal Activity\n`;
      context.recent_commands.slice(-10).forEach(cmd => {
        const focusIndicator = cmd.is_focused ? '🎯 ' : '';
        formattedContext += `- ${focusIndicator}\`${cmd.command}\` (${cmd.working_dir})\n`;
      });
      formattedContext += `\n`;
    }

    if (include_drift_analysis && context.drift_analysis) {
      const drift = context.drift_analysis;
      formattedContext += `## Objective Alignment Analysis\n`;
      formattedContext += `**Status:** ${drift.status}\n`;
      if (drift.alignment_score !== undefined) {
        formattedContext += `**Alignment Score:** ${(drift.alignment_score * 100).toFixed(1)}%\n`;
      }
      
      if (drift.status === 'potential_drift') {
        formattedContext += `⚠️ **Warning:** Recent activity may not align with current objectives.\n`;
      }
      formattedContext += `\n`;
    }

    if (context.recent_decisions && context.recent_decisions.length > 0) {
      formattedContext += `## Recent Decisions\n`;
      context.recent_decisions.forEach(decision => {
        formattedContext += `- **${decision.decision}** (${decision.importance})\n`;
        if (decision.context) {
          formattedContext += `  ${decision.context}\n`;
        }
      });
    }

    return {
      content: [
        {
          type: 'text',
          text: formattedContext
        }
      ]
    };
  }

  async listProjects(args) {
    const { status_filter = 'active' } = args;
    
    const projects = await this.ragRequest('/projects');
    
    let filteredProjects = projects;
    if (status_filter !== 'all') {
      filteredProjects = projects.filter(p => p.status === status_filter);
    }

    let result = `# Projects (${status_filter})\n\n`;
    
    filteredProjects.forEach(project => {
      const statusIcon = {
        'active': '🟢',
        'paused': '⏸️', 
        'archived': '📦',
        'focused': '🎯'
      }[project.status] || '⚪';
      
      result += `${statusIcon} **${project.name}** (${project.project_id})\n`;
      result += `   Path: ${project.root_path}\n`;
      result += `   Objectives: ${project.objectives ? project.objectives.filter(o => !o.completed).length : 0} active\n`;
      result += `   Last Active: ${project.last_active}\n\n`;
    });

    return {
      content: [
        {
          type: 'text',
          text: result
        }
      ]
    };
  }

  async searchKnowledge(args) {
    const { query, project_id, max_results = 10 } = args;
    
    const searchData = { 
      question: query, 
      k: max_results 
    };
    
    if (project_id) {
      searchData.project_id = project_id;
    }

    const results = await this.ragRequest('/query', 'POST', searchData);
    
    if (results.error) {
      throw new McpError(ErrorCode.InternalError, results.error);
    }

    let formattedResults = `# Knowledge Search Results\n\n`;
    formattedResults += `**Query:** ${query}\n`;
    formattedResults += `**Results:** ${results.results.length}\n\n`;

    results.results.forEach((result, index) => {
      formattedResults += `## Result ${index + 1}\n`;
      formattedResults += `**File:** ${result.metadata.file}\n`;
      formattedResults += `**Type:** ${result.metadata.type}\n`;
      if (result.metadata.start_line) {
        formattedResults += `**Lines:** ${result.metadata.start_line}-${result.metadata.end_line}\n`;
      }
      formattedResults += `\n\`\`\`\n${result.content}\n\`\`\`\n\n`;
    });

    return {
      content: [
        {
          type: 'text',
          text: formattedResults
        }
      ]
    };
  }

  async getProjectObjectives(args) {
    const { project_id, include_completed = false } = args;
    
    const objectives = await this.ragRequest(`/projects/${project_id}/objectives`);
    
    let result = `# Project Objectives\n\n`;
    
    const activeObjectives = objectives.filter(obj => !obj.completed);
    const completedObjectives = objectives.filter(obj => obj.completed);
    
    if (activeObjectives.length > 0) {
      result += `## Active Objectives (${activeObjectives.length})\n`;
      activeObjectives.forEach((obj, index) => {
        result += `${index + 1}. ${obj.text}\n`;
        result += `   Added: ${obj.timestamp}\n\n`;
      });
    }

    if (include_completed && completedObjectives.length > 0) {
      result += `## Completed Objectives (${completedObjectives.length})\n`;
      completedObjectives.forEach((obj, index) => {
        result += `${index + 1}. ✅ ${obj.text}\n`;
        result += `   Completed: ${obj.completed_at}\n\n`;
      });
    }

    return {
      content: [
        {
          type: 'text',
          text: result
        }
      ]
    };
  }

  async addProjectDecision(args) {
    const { project_id, decision, context = '', importance = 'normal' } = args;
    
    await this.ragRequest('/decision', 'POST', {
      project_id,
      decision,
      context,
      importance
    });

    return {
      content: [
        {
          type: 'text',
          text: `✅ Decision recorded for project ${project_id}: "${decision}"`
        }
      ]
    };
  }

  async checkObjectiveDrift(args) {
    const { project_id, hours = 24 } = args;
    
    const analysis = await this.ragRequest(`/drift/${project_id}?hours=${hours}`);
    
    let result = `# Objective Drift Analysis\n\n`;
    result += `**Project:** ${project_id}\n`;
    result += `**Analysis Period:** ${hours} hours\n`;
    result += `**Status:** ${analysis.status}\n`;
    
    if (analysis.alignment_score !== undefined) {
      result += `**Alignment Score:** ${(analysis.alignment_score * 100).toFixed(1)}%\n\n`;
    }

    if (analysis.current_objectives) {
      result += `## Current Objectives\n`;
      analysis.current_objectives.forEach((obj, index) => {
        result += `${index + 1}. ${obj}\n`;
      });
      result += `\n`;
    }

    if (analysis.recent_focus) {
      result += `## Recent Activity Focus\n`;
      result += `Recent commands focused on: ${analysis.recent_focus.join(', ')}\n\n`;
    }

    if (analysis.status === 'potential_drift') {
      result += `⚠️ **Warning:** Recent development activity may not be aligned with current objectives. Consider:\n`;
      result += `- Reviewing current objectives\n`;
      result += `- Updating objectives if priorities have changed\n`;
      result += `- Refocusing on core objectives\n`;
    } else {
      result += `✅ **Good Alignment:** Recent activity appears aligned with objectives.\n`;
    }

    return {
      content: [
        {
          type: 'text',
          text: result
        }
      ]
    };
  }

  async getRecentTerminalActivity(args) {
    const { project_id, hours = 8, focused_only = false } = args;
    
    let endpoint = `/terminals/activity?hours=${hours}`;
    if (project_id) {
      endpoint += `&project_id=${project_id}`;
    }
    if (focused_only) {
      endpoint += `&focused_only=true`;
    }
    
    const activities = await this.ragRequest(endpoint);
    
    let result = `# Recent Terminal Activity\n\n`;
    result += `**Period:** Last ${hours} hours\n`;
    if (project_id) {
      result += `**Project:** ${project_id}\n`;
    }
    if (focused_only) {
      result += `**Filter:** Focused terminals only\n`;
    }
    result += `**Commands:** ${activities.length}\n\n`;

    activities.slice(0, 20).forEach((activity, index) => {
      const focusIndicator = activity.is_focused ? '🎯 ' : '';
      const timeAgo = this.formatTimeAgo(activity.timestamp);
      
      result += `${index + 1}. ${focusIndicator}\`${activity.command}\`\n`;
      result += `   📁 ${activity.working_dir}\n`;
      result += `   ⏰ ${timeAgo}\n\n`;
    });

    return {
      content: [
        {
          type: 'text',
          text: result
        }
      ]
    };
  }

  async setProjectFocus(args) {
    const { project_id } = args;
    
    await this.ragRequest(`/focus/${project_id}`, 'POST');

    return {
      content: [
        {
          type: 'text',
          text: `🎯 Project focus set to: ${project_id}`
        }
      ]
    };
  }

  async addObjective(args) {
    const { project_id, objective } = args;
    
    await this.ragRequest('/objectives', 'POST', {
      project_id,
      objective
    });

    return {
      content: [
        {
          type: 'text',
          text: `✅ Added objective to project ${project_id}: "${objective}"`
        }
      ]
    };
  }

  formatTimeAgo(timestamp) {
    const now = new Date();
    const then = new Date(timestamp);
    const diffMs = now - then;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    
    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${Math.floor(diffHours / 24)}d ago`;
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('RAG Knowledge Agent MCP server running on stdio');
  }
}

const server = new RAGMCPServer();
server.run().catch(console.error);