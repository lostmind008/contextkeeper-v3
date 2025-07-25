#!/bin/bash
# rag_cli_v2.sh - Enhanced CLI for Multi-Project RAG Knowledge Agent v2.0
# Make executable: chmod +x rag_cli_v2.sh

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
DECISION_ICON="💡"
OBJECTIVE_ICON="🎯"
CONTEXT_ICON="🧠"

# Ensure RAG agent is running
check_agent() {
    if ! curl -s http://localhost:5555/health > /dev/null 2>&1; then
        echo -e "${RED}❌ RAG Agent not running!${NC}"
        echo -e "${BLUE}Starting agent...${NC}"
        cd "$RAG_DIR" && nohup $PYTHON_CMD rag_agent.py start > rag_agent.out 2>&1 &
        sleep 5
        if curl -s http://localhost:5555/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Agent started successfully${NC}"
        else
            echo -e "${RED}Failed to start agent. Check logs at $RAG_DIR/rag_agent.out${NC}"
            exit 1
        fi
    fi
}

# Project management commands
handle_projects() {
    check_agent
    case "$1" in
        list|ls|"")
            echo -e "${BLUE}${PROJECT_ICON} Projects:${NC}"
            curl -s http://localhost:5555/projects | python3 -m json.tool
            ;;
        create)
            shift
            if [ $# -lt 2 ]; then
                echo "Usage: rag projects create \"Project Name\" /path/to/project [description]"
                exit 1
            fi
            PROJECT_NAME="$1"
            ROOT_PATH="$2"
            DESCRIPTION="${3:-}"
            
            RESPONSE=$(curl -s -X POST http://localhost:5555/projects \
                -H "Content-Type: application/json" \
                -d "{\"name\": \"$PROJECT_NAME\", \"root_path\": \"$ROOT_PATH\", \"description\": \"$DESCRIPTION\"}")
            
            echo -e "${GREEN}✅ Created project:${NC}"
            echo "$RESPONSE" | python3 -m json.tool
            ;;
        focus)
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                echo "Usage: rag projects focus <project_id>"
                exit 1
            fi
            curl -s -X POST "http://localhost:5555/projects/$PROJECT_ID/focus"
            echo -e "${GREEN}✅ Focused on project: $PROJECT_ID${NC}"
            ;;
        pause)
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                echo "Usage: rag projects pause <project_id>"
                exit 1
            fi
            curl -s -X PUT "http://localhost:5555/projects/$PROJECT_ID/status" \
                -H "Content-Type: application/json" \
                -d '{"status": "paused"}'
            echo -e "${YELLOW}⏸️  Paused project: $PROJECT_ID${NC}"
            ;;
        resume)
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                echo "Usage: rag projects resume <project_id>"
                exit 1
            fi
            curl -s -X PUT "http://localhost:5555/projects/$PROJECT_ID/status" \
                -H "Content-Type: application/json" \
                -d '{"status": "active"}'
            echo -e "${GREEN}▶️  Resumed project: $PROJECT_ID${NC}"
            ;;
        archive)
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                echo "Usage: rag projects archive <project_id>"
                exit 1
            fi
            echo -e "${YELLOW}Are you sure you want to archive project $PROJECT_ID? (y/N)${NC}"
            read -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                curl -s -X PUT "http://localhost:5555/projects/$PROJECT_ID/status" \
                    -H "Content-Type: application/json" \
                    -d '{"status": "archived"}'
                echo -e "${PURPLE}📦 Archived project: $PROJECT_ID${NC}"
            else
                echo -e "${BLUE}Archive cancelled${NC}"
            fi
            ;;
        *)
            echo "Project commands:"
            echo "  rag projects list                      List all projects"
            echo "  rag projects create <name> <path>      Create new project"
            echo "  rag projects focus <id>                Set active project"
            echo "  rag projects pause <id>                Pause project"
            echo "  rag projects resume <id>               Resume project"
            echo "  rag projects archive <id>              Archive project"
            ;;
    esac
}

# Decision management
handle_decisions() {
    check_agent
    case "$1" in
        add|"")
            shift
            if [ $# -eq 0 ]; then
                read -p "Decision: " DECISION
                read -p "Reasoning: " REASONING
                read -p "Tags (comma-separated): " TAGS_INPUT
            else
                DECISION="$1"
                REASONING="${2:-}"
                TAGS_INPUT="${3:-}"
            fi
            
            # Convert tags to JSON array
            if [ -n "$TAGS_INPUT" ]; then
                TAGS=$(echo "$TAGS_INPUT" | python3 -c "import sys, json; print(json.dumps(sys.stdin.read().strip().split(',')))")
            else
                TAGS="[]"
            fi
            
            RESPONSE=$(curl -s -X POST http://localhost:5555/decision \
                -H "Content-Type: application/json" \
                -d "{\"decision\": \"$DECISION\", \"reasoning\": \"$REASONING\", \"tags\": $TAGS}")
            
            echo -e "${GREEN}✅ Added decision${NC}"
            echo "$RESPONSE" | python3 -m json.tool
            ;;
        *)
            echo "Decision commands:"
            echo "  rag decisions add [decision] [reasoning] [tags]"
            ;;
    esac
}

# Objective management
handle_objectives() {
    check_agent
    PROJECT_ID="$2"
    
    case "$1" in
        add)
            shift; shift
            if [ -z "$PROJECT_ID" ]; then
                PROJECTS=$(curl -s http://localhost:5555/projects)
                FOCUSED_ID=$(echo "$PROJECTS" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('focused_project', ''))")
                if [ -z "$FOCUSED_ID" ]; then
                    echo -e "${RED}No focused project. Please specify project ID or focus a project first.${NC}"
                    exit 1
                fi
                PROJECT_ID=$FOCUSED_ID
            fi
            
            if [ $# -eq 0 ]; then
                read -p "Objective title: " TITLE
                read -p "Description: " DESCRIPTION
                read -p "Priority (low/medium/high): " PRIORITY
            else
                TITLE="$1"
                DESCRIPTION="${2:-}"
                PRIORITY="${3:-medium}"
            fi
            
            RESPONSE=$(curl -s -X POST "http://localhost:5555/projects/$PROJECT_ID/objectives" \
                -H "Content-Type: application/json" \
                -d "{\"title\": \"$TITLE\", \"description\": \"$DESCRIPTION\", \"priority\": \"$PRIORITY\"}")
            
            echo -e "${GREEN}✅ Added objective${NC}"
            echo "$RESPONSE" | python3 -m json.tool
            ;;
        complete)
            shift; shift
            OBJECTIVE_ID="$1"
            if [ -z "$PROJECT_ID" ] || [ -z "$OBJECTIVE_ID" ]; then
                echo "Usage: rag objectives complete <project_id> <objective_id>"
                exit 1
            fi
            
            curl -s -X POST "http://localhost:5555/projects/$PROJECT_ID/objectives/$OBJECTIVE_ID/complete"
            echo -e "${GREEN}✅ Completed objective${NC}"
            ;;
        list)
            shift
            if [ -z "$PROJECT_ID" ]; then
                PROJECTS=$(curl -s http://localhost:5555/projects)
                FOCUSED_ID=$(echo "$PROJECTS" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('focused_project', ''))")
                PROJECT_ID=$FOCUSED_ID
            fi
            
            if [ -n "$PROJECT_ID" ]; then
                CONTEXT=$(curl -s "http://localhost:5555/projects/$PROJECT_ID/context")
                echo -e "${CYAN}${OBJECTIVE_ICON} Objectives for project $PROJECT_ID:${NC}"
                echo "$CONTEXT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for obj in data.get('pending_objectives', []):
    print(f\"  - [{obj['priority'].upper()}] {obj['title']}\")
    if obj['description']:
        print(f\"    {obj['description']}\")
"
            else
                echo -e "${RED}No project specified or focused${NC}"
            fi
            ;;
        *)
            echo "Objective commands:"
            echo "  rag objectives add [project_id] [title] [description] [priority]"
            echo "  rag objectives complete <project_id> <objective_id>"
            echo "  rag objectives list [project_id]"
            ;;
    esac
}

# Context export
handle_context() {
    check_agent
    case "$1" in
        export|claude|"")
            shift
            PROJECT_ID="$1"
            if [ -z "$PROJECT_ID" ]; then
                PROJECTS=$(curl -s http://localhost:5555/projects)
                FOCUSED_ID=$(echo "$PROJECTS" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('focused_project', ''))")
                PROJECT_ID=$FOCUSED_ID
            fi
            
            if [ -n "$PROJECT_ID" ]; then
                CONTEXT=$(curl -s "http://localhost:5555/projects/$PROJECT_ID/context")
                echo -e "${CYAN}${CONTEXT_ICON} Project Context:${NC}"
                echo "$CONTEXT" | python3 -m json.tool
            else
                echo -e "${RED}No project specified or focused${NC}"
            fi
            ;;
        *)
            echo "Context commands:"
            echo "  rag context [export|claude] [project_id]"
            ;;
    esac
}

# Briefing command
handle_briefing() {
    check_agent
    echo -e "${CYAN}📊 Daily Briefing${NC}"
    echo -e "${CYAN}=================${NC}"
    
    # Get project summary
    PROJECTS=$(curl -s http://localhost:5555/projects)
    echo "$PROJECTS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Total Projects: {data['total_projects']}")
print(f\"Active: {data['active_projects']} | Paused: {data['paused_projects']} | Archived: {data['archived_projects']}")
print()
print('Active Projects:')
for proj in data['projects']:
    if proj['status'] == 'active':
        focused = '🎯 ' if proj['id'] == data.get('focused_project') else '   '
        print(f\"{focused}{proj['name']} ({proj['id']})\")
        print(f\"    Pending objectives: {proj['objectives_pending']}")
        print(f\"    Total decisions: {proj['total_decisions']}")
        print(f\"    Last active: {proj['last_active']}\")
"
}

# Main command handling
source ./sacred_cli_integration.sh # Add this near the top
case "$1" in
    sacred|s)
        shift
        handle_sacred "$@"
        ;;
    # Project management
    projects|proj|p)
        shift
        handle_projects "$@"
        ;;
    
    # Decision tracking
    decisions|decision|dec|d)
        shift
        handle_decisions "$@"
        ;;
    
    # Objective tracking
    objectives|objective|obj|o)
        shift
        handle_objectives "$@"
        ;;
    
    # Context export
    context|ctx|c)
        shift
        handle_context "$@"
        ;;
    
    # Daily briefing
    briefing|brief|b)
        handle_briefing
        ;;
    
    # Query (enhanced with project awareness)
    ask|query|q)
        check_agent
        shift
        if [ $# -eq 0 ]; then
            # Interactive mode
            cd "$RAG_DIR" && $PYTHON_CMD rag_agent.py query
        else
            # Quick query
            cd "$RAG_DIR" && $PYTHON_CMD rag_agent.py query --question "$*"
        fi
        ;;
    
    # Legacy commands
    add)
        shift
        handle_decisions add "$@"
        ;;
    
    morning)
        handle_briefing
        ;;
    
    # Agent control
    start)
        cd "$RAG_DIR" && $PYTHON_CMD rag_agent.py start
        ;;
    
    stop)
        echo -e "${BLUE}Stopping RAG Agent...${NC}"
        pkill -f "rag_agent.py start"
        sleep 2
        if curl -s http://localhost:5555/health > /dev/null 2>&1; then
            echo -e "${RED}❌ Failed to stop agent${NC}"
        else
            echo -e "${GREEN}✅ Agent stopped${NC}"
        fi
        ;;
    
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    
    status)
        if curl -s http://localhost:5555/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Agent is running${NC}"
            HEALTH=$(curl -s http://localhost:5555/health)
            echo "Health: $HEALTH"
        else
            echo -e "${RED}❌ Agent is not running${NC}"
        fi
        ;;
    
    logs)
        tail -f "$RAG_DIR/rag_agent.log"
        ;;
    
    help|*)
        echo "RAG Knowledge Agent v2.0 - Multi-Project Support"
        echo "==============================================="
        echo ""
        echo "Project Management:"
        echo "  rag projects list                      List all projects"
        echo "  rag projects create <name> <path>      Create new project"
        echo "  rag projects focus <id>                Set active project"
        echo "  rag projects pause <id>                Pause project tracking"
        echo "  rag projects resume <id>               Resume project tracking"
        echo "  rag projects archive <id>              Archive completed project"
        echo ""
        echo "Decision & Objective Tracking:"
        echo "  rag decisions add [decision] [reason]  Add architectural decision"
        echo "  rag objectives add [title] [desc]      Add project objective"
        echo "  rag objectives complete <proj> <id>    Mark objective complete"
        echo "  rag objectives list [project]          List pending objectives"
        echo ""
        echo "Context & Briefing:"
        echo "  rag context [project_id]               Export project context"
        echo "  rag briefing                           Get daily briefing"
        echo ""
        echo "Knowledge Base:"
        echo "  rag ask <question>                     Query knowledge base"
        echo "  rag query                              Interactive query mode"
        echo ""
        echo "Agent Control:"
        echo "  rag start                              Start the agent"
        echo "  rag stop                               Stop the agent"
        echo "  rag restart                            Restart the agent"
        echo "  rag status                             Check agent status"
        echo "  rag logs                               View agent logs"
        echo ""
        echo "Shortcuts:"
        echo "  rag p    = projects"
        echo "  rag d    = decisions"
        echo "  rag o    = objectives"
        echo "  rag c    = context"
        echo "  rag b    = briefing"
        echo "  rag q    = query"
        ;;
esac