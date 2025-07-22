#!/bin/bash
# enhanced_rag_cli.sh - Multi-project RAG agent with terminal monitoring
# Make executable: chmod +x enhanced_rag_cli.sh

# Configuration
RAG_DIR="$HOME/rag-agent"
PYTHON_CMD="$RAG_DIR/venv/bin/python3"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Icons for better UX
PROJECT_ICON="📁"
FOCUS_ICON="🎯"
PAUSE_ICON="⏸️"
ARCHIVE_ICON="📦"
TERMINAL_ICON="💻"
CONTEXT_ICON="🧠"
OBJECTIVE_ICON="🎯"
DECISION_ICON="📝"
DRIFT_ICON="⚠️"

# Ensure RAG agent is running
check_agent() {
    if ! curl -s http://localhost:5555/health > /dev/null 2>&1; then
        echo -e "${RED}❌ RAG Agent not running!${NC}"
        echo -e "${BLUE}Starting enhanced agent...${NC}"
        cd "$RAG_DIR" && nohup $PYTHON_CMD enhanced_rag_agent.py start > rag_agent.out 2>&1 &
        sleep 5
        if curl -s http://localhost:5555/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Enhanced agent started successfully${NC}"
        else
            echo -e "${RED}Failed to start agent. Check logs at $RAG_DIR/rag_agent.out${NC}"
            exit 1
        fi
    fi
}

# Project Management Commands
handle_projects() {
    check_agent
    case "$1" in
        list|ls|"")
            echo -e "${BLUE}${PROJECT_ICON} Projects:${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py projects list
            ;;
        create|new)
            shift
            if [ $# -eq 0 ]; then
                read -p "Project name: " PROJECT_NAME
                read -p "Root path: " ROOT_PATH
            else
                PROJECT_NAME="$1"
                ROOT_PATH="$2"
            fi
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py projects create "$PROJECT_NAME" "$ROOT_PATH"
            echo -e "${GREEN}✅ Created project: $PROJECT_NAME${NC}"
            ;;
        pause)
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                read -p "Project ID to pause: " PROJECT_ID
            fi
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py projects pause "$PROJECT_ID"
            echo -e "${YELLOW}${PAUSE_ICON} Paused project: $PROJECT_ID${NC}"
            ;;
        resume)
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                read -p "Project ID to resume: " PROJECT_ID
            fi
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py projects resume "$PROJECT_ID"
            echo -e "${GREEN}▶️ Resumed project: $PROJECT_ID${NC}"
            ;;
        archive)
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                read -p "Project ID to archive: " PROJECT_ID
            fi
            echo -e "${YELLOW}Are you sure you want to archive project $PROJECT_ID? (y/N)${NC}"
            read -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py projects archive "$PROJECT_ID"
                echo -e "${PURPLE}${ARCHIVE_ICON} Archived project: $PROJECT_ID${NC}"
            else
                echo -e "${BLUE}Archive cancelled${NC}"
            fi
            ;;
        *)
            echo "Project commands:"
            echo "  projects list                    - List all projects"
            echo "  projects create [name] [path]    - Create new project"
            echo "  projects pause [project_id]      - Pause project tracking"
            echo "  projects resume [project_id]     - Resume project tracking"
            echo "  projects archive [project_id]    - Archive project"
            ;;
    esac
}

# Focus Management
handle_focus() {
    check_agent
    case "$1" in
        "")
            echo -e "${BLUE}${FOCUS_ICON} Current Focus:${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py focus
            ;;
        set)
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                read -p "Project ID to focus on: " PROJECT_ID
            fi
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py focus "$PROJECT_ID"
            echo -e "${GREEN}${FOCUS_ICON} Focused on project: $PROJECT_ID${NC}"
            ;;
        terminals)
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                read -p "Project ID: " PROJECT_ID
            fi
            echo -e "${BLUE}${TERMINAL_ICON} Active terminals (select PIDs to focus):${NC}"
            # Get current terminal PIDs
            ps aux | grep -E "(bash|zsh|fish)" | grep -v grep | awk '{print $2 " " $11}'
            read -p "Enter terminal PIDs (space-separated): " TERMINAL_PIDS
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py focus terminals "$PROJECT_ID" $TERMINAL_PIDS
            echo -e "${GREEN}${FOCUS_ICON} Focused terminals set for project${NC}"
            ;;
        clear)
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py focus clear
            echo -e "${BLUE}Focus cleared${NC}"
            ;;
        *)
            echo "Focus commands:"
            echo "  focus                          - Show current focus"
            echo "  focus set [project_id]         - Focus on a project"
            echo "  focus terminals [project_id]   - Set focused terminals"
            echo "  focus clear                    - Clear focus"
            ;;
    esac
}

# Objectives Management
handle_objectives() {
    check_agent
    case "$1" in
        list|"")
            shift
            PROJECT_ID="$1"
            echo -e "${BLUE}${OBJECTIVE_ICON} Project Objectives:${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py objectives list "$PROJECT_ID"
            ;;
        add)
            shift
            PROJECT_ID="$1"
            shift
            OBJECTIVE="$*"
            if [ -z "$OBJECTIVE" ]; then
                read -p "New objective: " OBJECTIVE
            fi
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py objectives add "$PROJECT_ID" "$OBJECTIVE"
            echo -e "${GREEN}${OBJECTIVE_ICON} Added objective: $OBJECTIVE${NC}"
            ;;
        complete|done)
            shift
            PROJECT_ID="$1"
            OBJECTIVE_INDEX="$2"
            if [ -z "$OBJECTIVE_INDEX" ]; then
                read -p "Objective index to complete: " OBJECTIVE_INDEX
            fi
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py objectives complete "$PROJECT_ID" "$OBJECTIVE_INDEX"
            echo -e "${GREEN}✅ Marked objective as completed${NC}"
            ;;
        *)
            echo "Objectives commands:"
            echo "  objectives list [project_id]              - List objectives"
            echo "  objectives add [project_id] [objective]   - Add new objective"
            echo "  objectives complete [project_id] [index]  - Mark objective as done"
            ;;
    esac
}

# Context Management for AI Integration
handle_context() {
    check_agent
    case "$1" in
        ""|current)
            shift
            PROJECT_ID="$1"
            echo -e "${BLUE}${CONTEXT_ICON} Project Context:${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py context "$PROJECT_ID"
            ;;
        export)
            shift
            PROJECT_ID="$1"
            FORMAT="${2:-json}"
            echo -e "${BLUE}Exporting context for AI agents...${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py context export "$PROJECT_ID" "$FORMAT"
            ;;
        claude)
            # Special integration for Claude Code
            shift
            PROJECT_ID="$1"
            echo -e "${BLUE}${CONTEXT_ICON} Preparing context for Claude Code...${NC}"
            CONTEXT=$(cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py context export "$PROJECT_ID" "claude")
            echo "$CONTEXT" > /tmp/claude_context.md
            echo -e "${GREEN}✅ Context exported to /tmp/claude_context.md${NC}"
            echo -e "${CYAN}You can now reference this in Claude Code with:${NC}"
            echo -e "${YELLOW}cat /tmp/claude_context.md${NC}"
            ;;
        *)
            echo "Context commands:"
            echo "  context                           - Show current project context"
            echo "  context export [project_id]      - Export context for AI agents"
            echo "  context claude [project_id]      - Prepare context for Claude Code"
            ;;
    esac
}

# Terminal Activity Monitoring
handle_terminals() {
    check_agent
    case "$1" in
        ""|activity)
            echo -e "${BLUE}${TERMINAL_ICON} Recent Terminal Activity:${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py terminals activity
            ;;
        focused)
            echo -e "${BLUE}${TERMINAL_ICON} Focused Terminal Activity:${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py terminals focused
            ;;
        monitor)
            echo -e "${BLUE}Starting terminal monitoring...${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py terminals monitor
            ;;
        *)
            echo "Terminal commands:"
            echo "  terminals                         - Show recent terminal activity"
            echo "  terminals focused                 - Show focused terminal activity"
            echo "  terminals monitor                 - Start monitoring mode"
            ;;
    esac
}

# Drift Detection and Analysis
handle_drift() {
    check_agent
    case "$1" in
        ""|check)
            shift
            PROJECT_ID="$1"
            echo -e "${BLUE}${DRIFT_ICON} Checking objective drift...${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py drift check "$PROJECT_ID"
            ;;
        analyze)
            shift
            PROJECT_ID="$1"
            HOURS="${2:-24}"
            echo -e "${BLUE}${DRIFT_ICON} Analyzing activity patterns...${NC}"
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py drift analyze "$PROJECT_ID" "$HOURS"
            ;;
        *)
            echo "Drift analysis commands:"
            echo "  drift                             - Check for objective drift"
            echo "  drift analyze [project_id] [hrs] - Deep analysis of activity patterns"
            ;;
    esac
}

# Enhanced Daily Briefing
handle_briefing() {
    check_agent
    echo -e "${BLUE}🌅 Enhanced Daily Development Briefing${NC}\n"
    
    echo -e "${PURPLE}${PROJECT_ICON} Active Projects:${NC}"
    cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py projects list | grep -E "(🟢|🎯)"
    
    echo -e "\n${CYAN}${OBJECTIVE_ICON} Today's Objectives:${NC}"
    cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py objectives today
    
    echo -e "\n${YELLOW}${TERMINAL_ICON} Recent Activity:${NC}"
    cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py terminals activity --hours 24
    
    echo -e "\n${RED}${DRIFT_ICON} Drift Analysis:${NC}"
    cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py drift check
    
    echo -e "\n${GREEN}${CONTEXT_ICON} Ready for AI collaboration!${NC}"
}

# MCP Integration Helper
handle_mcp() {
    check_agent
    case "$1" in
        status)
            echo -e "${BLUE}MCP Integration Status:${NC}"
            curl -s http://localhost:5555/mcp/status | jq '.'
            ;;
        context)
            shift
            PROJECT_ID="$1"
            echo -e "${BLUE}Exporting MCP context...${NC}"
            curl -s -X POST http://localhost:5555/mcp/context \
                -H "Content-Type: application/json" \
                -d "{\"project_id\": \"$PROJECT_ID\"}" | jq '.'
            ;;
        *)
            echo "MCP Integration commands:"
            echo "  mcp status                        - Show MCP integration status"
            echo "  mcp context [project_id]          - Get context for MCP tools"
            ;;
    esac
}

# Main command handling
case "$1" in
    projects|proj|p)
        shift
        handle_projects "$@"
        ;;
    focus|f)
        shift
        handle_focus "$@"
        ;;
    objectives|obj|o)
        shift
        handle_objectives "$@"
        ;;
    context|ctx|c)
        shift
        handle_context "$@"
        ;;
    terminals|term|t)
        shift
        handle_terminals "$@"
        ;;
    drift|d)
        shift
        handle_drift "$@"
        ;;
    briefing|brief|morning)
        handle_briefing
        ;;
    mcp)
        shift
        handle_mcp "$@"
        ;;
    
    # Legacy commands (backwards compatibility)
    ask|query|q)
        check_agent
        shift
        if [ $# -eq 0 ]; then
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py query
        else
            cd "$RAG_DIR" && $PYTHON_CMD enhanced_rag_agent.py query --question "$*"
        fi
        ;;
    add|decision)
        check_agent
        shift
        echo -e "${BLUE}Adding decision to knowledge base...${NC}"
        DECISION="$*"
        read -p "Context: " CONTEXT
        curl -s -X POST http://localhost:5555/decision \
            -H "Content-Type: application/json" \
            -d "{\"decision\": \"$DECISION\", \"context\": \"$CONTEXT\"}" > /dev/null
        echo -e "${GREEN}✅ Decision added${NC}"
        ;;
    status)
        if curl -s http://localhost:5555/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Enhanced RAG Agent is running${NC}"
            curl -s http://localhost:5555/health | jq '.'
        else
            echo -e "${RED}❌ RAG Agent is not running${NC}"
        fi
        ;;
    start)
        check_agent
        echo -e "${GREEN}✅ Enhanced agent is running${NC}"
        ;;
    stop)
        echo -e "${BLUE}Stopping Enhanced RAG Agent...${NC}"
        pkill -f "enhanced_rag_agent.py"
        echo -e "${GREEN}✅ Agent stopped${NC}"
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    logs)
        tail -f "$RAG_DIR/rag_agent.log"
        ;;
    help|*)
        echo -e "${BLUE}Enhanced RAG Knowledge Agent CLI${NC}"
        echo ""
        echo -e "${YELLOW}Multi-Project Management:${NC}"
        echo "  projects list                     - List all projects"
        echo "  projects create [name] [path]     - Create new project"
        echo "  projects pause [id]               - Pause project tracking"
        echo "  projects resume [id]              - Resume project tracking"
        echo "  projects archive [id]             - Archive project"
        echo ""
        echo -e "${YELLOW}Focus & Context Management:${NC}"
        echo "  focus                             - Show/set project focus"
        echo "  focus terminals [id]              - Set focused terminals"
        echo "  context [project_id]              - Get project context"
        echo "  context claude [id]               - Export for Claude Code"
        echo ""
        echo -e "${YELLOW}Objectives & Tracking:${NC}"
        echo "  objectives list [id]              - List project objectives"
        echo "  objectives add [id] [text]        - Add new objective"
        echo "  objectives complete [id] [index]  - Mark objective done"
        echo ""
        echo -e "${YELLOW}Activity & Drift Analysis:${NC}"
        echo "  terminals                         - Show terminal activity"
        echo "  drift check [id]                  - Check objective drift"
        echo "  briefing                          - Daily development briefing"
        echo ""
        echo -e "${YELLOW}AI Integration:${NC}"
        echo "  mcp status                        - MCP integration status"
        echo "  mcp context [id]                  - Export for MCP tools"
        echo ""
        echo -e "${YELLOW}Legacy Commands:${NC}"
        echo "  ask [question]                    - Query knowledge base"
        echo "  add [decision]                    - Add project decision"
        echo "  status                            - Check agent status"
        echo ""
        echo -e "${CYAN}Examples:${NC}"
        echo "  rag projects create \"My App\" ~/code/myapp"
        echo "  rag focus set proj_1234567890"
        echo "  rag objectives add proj_1234567890 \"Implement authentication\""
        echo "  rag context claude proj_1234567890"
        echo "  rag briefing"
        ;;
esac