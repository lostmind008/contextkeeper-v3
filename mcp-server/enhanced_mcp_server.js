#!/usr/bin/env node

/**
 * Enhanced MCP Server for ContextKeeper
 * Provides advanced development context to Claude Code and other AI assistants
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
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';

const execAsync = promisify(exec);

const RAG_AGENT_BASE_URL = process.env.RAG_AGENT_URL || 'http://localhost:5555';

class EnhancedContextKeeperMCP {
  constructor() {
    this.server = new Server(
      {
        name: 'contextkeeper-enhanced',
        version: '2.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    this.cache = new Map();
  }

  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          // Project Context Tools
          {
            name: 'get_development_context',
            description: 'Get comprehensive development context including project status, git activity, objectives, decisions, and drift analysis',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Optional project ID. Uses focused project if not provided'
                },
                include_git: {
                  type: 'boolean',
                  description: 'Include git activity analysis (default: true)',
                  default: true
                },
                include_drift: {
                  type: 'boolean',
                  description: 'Include drift analysis (default: true)',
                  default: true
                },
                hours: {
                  type: 'number',
                  description: 'Hours of history to analyze (default: 24)',
                  default: 24
                }
              }
            }
          },
          
          // Intelligent Search
          {
            name: 'intelligent_search',
            description: 'Search with semantic understanding across code, decisions, objectives, and git history',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Natural language search query'
                },
                search_types: {
                  type: 'array',
                  items: {
                    type: 'string',
                    enum: ['code', 'decisions', 'objectives', 'git_activity', 'all']
                  },
                  description: 'Types of content to search (default: all)',
                  default: ['all']
                },
                project_id: {
                  type: 'string',
                  description: 'Optional: limit to specific project'
                },
                max_results: {
                  type: 'number',
                  description: 'Maximum results per type (default: 5)',
                  default: 5
                }
              },
              required: ['query']
            }
          },

          // Git Integration
          {
            name: 'analyze_git_activity',
            description: 'Analyze git activity, uncommitted changes, and branch status',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Project ID to analyze'
                },
                include_uncommitted: {
                  type: 'boolean',
                  description: 'Include uncommitted changes (default: true)',
                  default: true
                },
                include_branches: {
                  type: 'boolean',
                  description: 'Include branch analysis (default: true)',
                  default: true
                }
              }
            }
          },

          // Drift Detection
          {
            name: 'check_development_drift',
            description: 'Analyze if current development aligns with objectives and get recommendations',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Project ID to analyze'
                },
                hours: {
                  type: 'number',
                  description: 'Hours of activity to analyze (default: 24)',
                  default: 24
                },
                include_recommendations: {
                  type: 'boolean',
                  description: 'Include actionable recommendations (default: true)',
                  default: true
                }
              }
            }
          },

          // Project Management
          {
            name: 'manage_objectives',
            description: 'Add, update, or complete project objectives',
            inputSchema: {
              type: 'object',
              properties: {
                action: {
                  type: 'string',
                  enum: ['add', 'complete', 'update', 'list'],
                  description: 'Action to perform'
                },
                project_id: {
                  type: 'string',
                  description: 'Project ID'
                },
                objective_id: {
                  type: 'string',
                  description: 'Objective ID (for complete/update actions)'
                },
                title: {
                  type: 'string',
                  description: 'Objective title (for add/update)'
                },
                description: {
                  type: 'string',
                  description: 'Objective description'
                },
                priority: {
                  type: 'string',
                  enum: ['low', 'medium', 'high'],
                  description: 'Priority level',
                  default: 'medium'
                }
              },
              required: ['action']
            }
          },
          
          // Decision Tracking
          {
            name: 'track_decision',
            description: 'Record an architectural or implementation decision with context',
            inputSchema: {
              type: 'object',
              properties: {
                decision: {
                  type: 'string',
                  description: 'The decision made'
                },
                reasoning: {
                  type: 'string',
                  description: 'Why this decision was made'
                },
                alternatives_considered: {
                  type: 'array',
                  items: { type: 'string' },
                  description: 'Other options that were considered'
                },
                tags: {
                  type: 'array',
                  items: { type: 'string' },
                  description: 'Tags for categorization (e.g., architecture, security)',
                  default: []
                },
                project_id: {
                  type: 'string',
                  description: 'Project ID (optional, uses focused project)'
                }
              },
              required: ['decision', 'reasoning']
            }
          },

          // Development Flow
          {
            name: 'suggest_next_action',
            description: 'Get AI-powered suggestions for what to work on next based on objectives and current state',
            inputSchema: {
              type: 'object',
              properties: {
                project_id: {
                  type: 'string',
                  description: 'Project ID'
                },
                consider_blockers: {
                  type: 'boolean',
                  description: 'Consider potential blockers (default: true)',
                  default: true
                }
              }
            }
          },

          // Code Generation Context
          {
            name: 'get_code_context',
            description: 'Get relevant code examples and patterns for implementing a feature',
            inputSchema: {
              type: 'object',
              properties: {
                feature_description: {
                  type: 'string',
                  description: 'What you want to implement'
                },
                project_id: {
                  type: 'string',
                  description: 'Project ID'
                },
                include_similar: {
                  type: 'boolean',
                  description: 'Include similar implementations (default: true)',
                  default: true
                }
              },
              required: ['feature_description']
            }
          },

          // Daily Workflow
          {
            name: 'daily_briefing',
            description: 'Get a comprehensive daily briefing with all projects, objectives, and recommendations',
            inputSchema: {
              type: 'object',
              properties: {
                include_all_projects: {
                  type: 'boolean',
                  description: 'Include all projects, not just active (default: false)',
                  default: false
                }
              }
            }
          }
        ]
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        // Check cache for expensive operations
        const cacheKey = `${name}-${JSON.stringify(args)}`;
        if (this.shouldCache(name) && this.cache.has(cacheKey)) {
          const cached = this.cache.get(cacheKey);
          if (Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.result;
          }
        }

        let result;
        switch (name) {
          case 'get_development_context':
            result = await this.getDevelopmentContext(args);
            break;
          
          case 'intelligent_search':
            result = await this.intelligentSearch(args);
            break;

          case 'analyze_git_activity':
            result = await this.analyzeGitActivity(args);
            break;

          case 'check_development_drift':
            result = await this.checkDevelopmentDrift(args);
            break;

          case 'manage_objectives':
            result = await this.manageObjectives(args);
            break;

          case 'track_decision':
            result = await this.trackDecision(args);
            break;
          
          case 'suggest_next_action':
            result = await this.suggestNextAction(args);
            break;

          case 'get_code_context':
            result = await this.getCodeContext(args);
            break;

          case 'daily_briefing':
            result = await this.dailyBriefing(args);
            break;
          
          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Unknown tool: ${name}`
            );
        }

        // Cache expensive operations
        if (this.shouldCache(name)) {
          this.cache.set(cacheKey, {
            result,
            timestamp: Date.now()
          });
        }

        return result;
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

  shouldCache(toolName) {
    const cacheableTools = [
      'get_development_context',
      'analyze_git_activity',
      'check_development_drift',
      'daily_briefing'
    ];
    return cacheableTools.includes(toolName);
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
        `Failed to communicate with ContextKeeper: ${error.message}`
      );
    }
  }

  async getDevelopmentContext(args) {
    const { project_id, include_git = true, include_drift = true, hours = 24 } = args;
    
    // Get project context
    const context = await this.ragRequest(
      project_id ? `/projects/${project_id}/context` : '/context'
    );

    let formattedContext = `# Development Context\n\n`;

    if (context.project) {
      formattedContext += `## Project: ${context.project.name}\n`;
      formattedContext += `Status: ${context.project.status}\n`;
      formattedContext += `Last Active: ${this.formatTimeAgo(context.project.last_active)}\n\n`;
    }

    // Add objectives with progress
    if (context.pending_objectives && context.pending_objectives.length > 0) {
      formattedContext += `## Active Objectives (${context.pending_objectives.length})\n`;
      for (const obj of context.pending_objectives) {
        formattedContext += `### ${obj.priority.toUpperCase()}: ${obj.title}\n`;
        if (obj.description) {
          formattedContext += `${obj.description}\n`;
        }
        formattedContext += `Created: ${this.formatTimeAgo(obj.created_at)}\n\n`;
      }
    }

    // Add recent decisions
    if (context.recent_decisions && context.recent_decisions.length > 0) {
      formattedContext += `## Recent Decisions\n`;
      for (const decision of context.recent_decisions.slice(0, 5)) {
        formattedContext += `### ${decision.decision}\n`;
        if (decision.reasoning) {
          formattedContext += `**Reasoning:** ${decision.reasoning}\n`;
        }
        if (decision.tags && decision.tags.length > 0) {
          formattedContext += `**Tags:** ${decision.tags.join(', ')}\n`;
        }
        formattedContext += `*${this.formatTimeAgo(decision.timestamp)}*\n\n`;
      }
    }

    // Add git activity if requested
    if (include_git && project_id) {
      try {
        const gitActivity = await this.getGitSummary(project_id, hours);
        if (gitActivity) {
          formattedContext += gitActivity;
        }
      } catch (error) {
        console.error('Failed to get git activity:', error);
      }
    }

    // Add drift analysis if requested
    if (include_drift && project_id) {
      try {
        const driftAnalysis = await this.ragRequest(`/projects/${project_id}/drift?hours=${hours}`);
        if (driftAnalysis.analysis) {
          formattedContext += `## Objective Alignment\n`;
          formattedContext += `**Status:** ${driftAnalysis.analysis.status}\n`;
          formattedContext += `**Alignment Score:** ${(driftAnalysis.analysis.alignment_score * 100).toFixed(0)}%\n\n`;

          if (driftAnalysis.analysis.recommendations) {
            formattedContext += `### Recommendations\n`;
            for (const rec of driftAnalysis.analysis.recommendations) {
              formattedContext += `- ${rec}\n`;
            }
            formattedContext += '\n';
          }
        }
      } catch (error) {
        console.error('Failed to get drift analysis:', error);
      }
    }

    // Add statistics
    formattedContext += `## Project Statistics\n`;
    formattedContext += `- Total Decisions: ${context.statistics?.total_decisions || 0}\n`;
    formattedContext += `- Total Objectives: ${context.statistics?.total_objectives || 0}\n`;
    formattedContext += `- Completed Objectives: ${context.statistics?.completed_objectives || 0}\n`;

    return {
      content: [
        {
          type: 'text',
          text: formattedContext
        }
      ]
    };
  }

  async intelligentSearch(args) {
    const { query, search_types = ['all'], project_id, max_results = 5 } = args;
    
    // Perform search
    const searchResults = await this.ragRequest('/query', 'POST', {
      question: query,
      k: max_results * 3, // Get more to filter by type
      project_id
    });

    if (searchResults.error) {
      throw new McpError(ErrorCode.InternalError, searchResults.error);
    }

    // Categorize results by type
    const categorized = {
      code: [],
      decisions: [],
      objectives: [],
      git_activity: [],
      other: []
    };

    for (const result of searchResults.results || []) {
      const type = result.metadata?.type || 'other';
      const category = categorized[type] || categorized.other;
      
      if (search_types.includes('all') || search_types.includes(type)) {
        category.push(result);
      }
    }

    // Format results
    let formattedResults = `# Search Results for: "${query}"\n\n`;

    for (const [type, results] of Object.entries(categorized)) {
      if (results.length > 0) {
        formattedResults += `## ${type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ')}\n\n`;

        for (const result of results.slice(0, max_results)) {
          if (type === 'code') {
            formattedResults += `### ${result.metadata.file}\n`;
            if (result.metadata.start_line) {
              formattedResults += `Lines ${result.metadata.start_line}-${result.metadata.end_line}\n`;
            }
            formattedResults += `\`\`\`\n${result.content}\n\`\`\`\n\n`;
          } else {
            formattedResults += `### ${result.content.split('\n')[0]}\n`;
            formattedResults += `${result.content}\n\n`;
          }
        }
      }
    }

    return {
      content: [
        {
          type: 'text',
          text: formattedResults
        }
      ]
    };
  }

  async analyzeGitActivity(args) {
    const { project_id, include_uncommitted = true, include_branches = true } = args;
    
    if (!project_id) {
      throw new McpError(ErrorCode.InvalidParams, 'project_id is required');
    }

    // Get project info
    const project = await this.ragRequest(`/projects/${project_id}/context`);
    if (!project.project) {
      throw new McpError(ErrorCode.InvalidParams, 'Project not found');
    }

    const projectPath = project.project.root_path;
    let analysis = `# Git Activity Analysis\n\n`;

    try {
      // Get current branch
      const { stdout: branch } = await execAsync('git branch --show-current', { cwd: projectPath });
      analysis += `## Current Branch: ${branch.trim()}\n\n`;

      // Get recent commits
      const { stdout: commits } = await execAsync(
        'git log --oneline --decorate --graph -10',
        { cwd: projectPath }
      );
      analysis += `## Recent Commits\n\`\`\`\n${commits}\`\`\`\n\n`;

      if (include_uncommitted) {
        // Get uncommitted changes
        const { stdout: status } = await execAsync('git status --short', { cwd: projectPath });
        if (status.trim()) {
          analysis += `## Uncommitted Changes\n\`\`\`\n${status}\`\`\`\n\n`;

          // Get diff summary
          try {
            const { stdout: diff } = await execAsync('git diff --stat', { cwd: projectPath });
            if (diff.trim()) {
              analysis += `## Diff Summary\n\`\`\`\n${diff}\`\`\`\n\n`;
            }
          } catch (error) {
            // No diff is okay
          }
        }
      }

      if (include_branches) {
        // Get all branches
        const { stdout: branches } = await execAsync(
          'git branch -a --format="%(refname:short) (%(committerdate:relative))"',
          { cwd: projectPath }
        );
        analysis += `## All Branches\n\`\`\`\n${branches}\`\`\`\n`;
      }

    } catch (error) {
      analysis += `\n⚠️ Git analysis error: ${error.message}\n`;
    }

    return {
      content: [
        {
          type: 'text',
          text: analysis
        }
      ]
    };
  }

  async checkDevelopmentDrift(args) {
    const { project_id, hours = 24, include_recommendations = true } = args;
    
    if (!project_id) {
      throw new McpError(ErrorCode.InvalidParams, 'project_id is required');
    }

    const driftAnalysis = await this.ragRequest(`/projects/${project_id}/drift?hours=${hours}`);

    if (!driftAnalysis.analysis) {
      return {
        content: [
          {
            type: 'text',
            text: 'No drift analysis available'
          }
        ]
      };
    }

    let report = driftAnalysis.report || `# Drift Analysis\n\n`;
    
    // Add visual representation
    const { alignment_score, status, objective_progress } = driftAnalysis.analysis;
    
    report += `\n## Visual Summary\n`;
    report += this.createProgressBar('Overall Alignment', alignment_score);

    if (objective_progress) {
      report += `\n### Objective Progress\n`;
      for (const [obj, progress] of Object.entries(objective_progress)) {
        report += this.createProgressBar(obj, progress);
      }
    }

    if (!include_recommendations) {
      // Remove recommendations section
      const recIndex = report.indexOf('Recommendations:');
      if (recIndex > -1) {
        report = report.substring(0, recIndex);
      }
    }

    return {
      content: [
        {
          type: 'text',
          text: report
        }
      ]
    };
  }

  async suggestNextAction(args) {
    const { project_id, consider_blockers = true } = args;
    
    // Get project context
    const context = await this.ragRequest(
      project_id ? `/projects/${project_id}/context` : '/context'
    );

    // Get drift analysis
    const driftAnalysis = project_id ?
      await this.ragRequest(`/projects/${project_id}/drift?hours=24`) : null;

    let suggestions = `# Suggested Next Actions\n\n`;

    // Analyze pending objectives
    const pendingObjectives = context.pending_objectives || [];
    const highPriorityObjectives = pendingObjectives.filter(o => o.priority === 'high');
    const lowProgressObjectives = [];

    if (driftAnalysis?.analysis?.objective_progress) {
      for (const [obj, progress] of Object.entries(driftAnalysis.analysis.objective_progress)) {
        if (progress < 0.3) {
          const objective = pendingObjectives.find(o => o.title === obj);
          if (objective) {
            lowProgressObjectives.push(objective);
          }
        }
      }
    }

    // Priority 1: High priority with low progress
    const urgentObjectives = highPriorityObjectives.filter(o =>
      lowProgressObjectives.some(lo => lo.title === o.title)
    );
    
    if (urgentObjectives.length > 0) {
      suggestions += `## 🚨 Urgent: High Priority with Low Progress\n`;
      for (const obj of urgentObjectives) {
        suggestions += `### ${obj.title}\n`;
        suggestions += `${obj.description || 'No description'}\n`;
        suggestions += `**Why now:** High priority objective with minimal progress\n\n`;
      }
    }

    // Priority 2: Low progress objectives
    if (lowProgressObjectives.length > 0 && urgentObjectives.length === 0) {
      suggestions += `## 📊 Focus Needed: Low Progress Objectives\n`;
      for (const obj of lowProgressObjectives.slice(0, 3)) {
        suggestions += `### ${obj.title}\n`;
        suggestions += `${obj.description || 'No description'}\n`;
        suggestions += `**Priority:** ${obj.priority}\n\n`;
      }
    }

    // Priority 3: Continue current momentum
    if (driftAnalysis?.analysis?.aligned_count > 0) {
      suggestions += `## ✅ Continue Current Work\n`;
      suggestions += `Your recent activity aligns well with objectives. `;
      suggestions += `Consider continuing your current approach.\n\n`;
    }

    // Consider blockers
    if (consider_blockers) {
      // Check for uncommitted changes
      try {
        const gitStatus = await this.analyzeGitActivity({
          project_id,
          include_uncommitted: true,
          include_branches: false
        });

        if (gitStatus.content[0].text.includes('Uncommitted Changes')) {
          suggestions += `## ⚠️ Potential Blocker: Uncommitted Changes\n`;
          suggestions += `You have uncommitted changes. Consider:\n`;
          suggestions += `- Review and commit current changes\n`;
          suggestions += `- Stash changes if switching context\n\n`;
        }
      } catch (error) {
        // Git check failed, not critical
      }
    }

    // Add decision points
    if (context.recent_decisions && context.recent_decisions.length > 0) {
      const recentDecision = context.recent_decisions[0];
      suggestions += `## 💡 Recent Decision Context\n`;
      suggestions += `Your recent decision: "${recentDecision.decision}"\n`;
      suggestions += `Consider how your next action aligns with this.\n`;
    }

    return {
      content: [
        {
          type: 'text',
          text: suggestions
        }
      ]
    };
  }

  // Helper methods
  formatTimeAgo(timestamp) {
    const now = new Date();
    const then = new Date(timestamp);
    const diffMs = now - then;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffDays > 0) return `${diffDays}d ago`;
    if (diffHours > 0) return `${diffHours}h ago`;
    if (diffMins > 0) return `${diffMins}m ago`;
    return 'just now';
  }

  createProgressBar(label, progress) {
    const width = 30;
    const filled = Math.round(progress * width);
    const empty = width - filled;
    const bar = '█'.repeat(filled) + '░'.repeat(empty);
    const percentage = (progress * 100).toFixed(0);
    return `${label}\n[${bar}] ${percentage}%\n\n`;
  }

  async getGitSummary(projectId, hours) {
    // This would integrate with the git activity tracker
    // For now, return a placeholder
    return `## Git Activity (Last ${hours}h)\n*Git integration pending*\n\n`;
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Enhanced ContextKeeper MCP server running on stdio');
  }
}

const server = new EnhancedContextKeeperMCP();
server.run().catch(console.error);