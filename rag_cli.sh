#!/bin/bash
# rag_cli.sh - Simple wrapper for RAG Knowledge Agent
# Make executable: chmod +x rag_cli.sh

# Configuration
RAG_DIR="$HOME/rag-agent"
PYTHON_CMD="$RAG_DIR/venv/bin/python3"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

# Main command handling
case "$1" in
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
        
    add|decision|d)
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
        
    morning|brief)
        check_agent
        echo -e "${BLUE}🌅 Good morning! Here's your project context:${NC}\n"
        
        # Get recent decisions
        cd "$RAG_DIR" && $PYTHON_CMD rag_agent.py query --question "What decisions were made recently?"
        
        echo -e "\n${BLUE}Current focus areas:${NC}"
        cd "$RAG_DIR" && $PYTHON_CMD rag_agent.py query --question "What are the current TODO items or pending tasks?"
        ;;
        
    status)
        if curl -s http://localhost:5555/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ RAG Agent is running${NC}"
            RESPONSE=$(curl -s http://localhost:5555/health)
            echo "Status: $RESPONSE"
        else
            echo -e "${RED}❌ RAG Agent is not running${NC}"
        fi
        ;;
        
    stop)
        echo -e "${BLUE}Stopping RAG Agent...${NC}"
        pkill -f "rag_agent.py start"
        echo -e "${GREEN}✅ Agent stopped${NC}"
        ;;
        
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
        
    start)
        check_agent
        echo -e "${GREEN}✅ Agent is running${NC}"
        ;;
        
    logs)
        tail -f "$RAG_DIR/rag_agent.log"
        ;;
        
    youtube|yt)
        # Special commands for YouTube Analyzer project
        check_agent
        shift
        case "$1" in
            gemini)
                cd "$RAG_DIR" && $PYTHON_CMD rag_agent.py query --question "Show all Gemini integration code and API usage"
                ;;
            agents)
                cd "$RAG_DIR" && $PYTHON_CMD rag_agent.py query --question "What agents have been created for the YouTube analyzer?"
                ;;
            api)
                cd "$RAG_DIR" && $PYTHON_CMD rag_agent.py query --question "What's the latest API configuration for Gemini and YouTube?"
                ;;
            errors)
                cd "$RAG_DIR" && $PYTHON_CMD rag_agent.py query --question "What errors or issues have been encountered and how were they solved?"
                ;;
            *)
                echo "YouTube Analyzer queries:"
                echo "  rag youtube gemini  - Show Gemini integration"
                echo "  rag youtube agents  - List all agents"
                echo "  rag youtube api     - Show API configs"
                echo "  rag youtube errors  - Show solved issues"
                ;;
        esac
        ;;
        
    help|*)
        echo "RAG Knowledge Agent CLI"
        echo ""
        echo "Usage: rag [command] [args]"
        echo ""
        echo "Commands:"
        echo "  ask, query, q [question]  - Query the knowledge base"
        echo "  add, decision, d [text]   - Add a project decision"
        echo "  morning, brief            - Get morning briefing"
        echo "  status                    - Check if agent is running"
        echo "  start                     - Start the agent"
        echo "  stop                      - Stop the agent"
        echo "  restart                   - Restart the agent"
        echo "  logs                      - View agent logs"
        echo "  youtube, yt [subcommand]  - YouTube Analyzer specific queries"
        echo ""
        echo "Examples:"
        echo "  rag ask What payment system are we using?"
        echo "  rag add Decided to use Stripe for payments"
        echo "  rag youtube gemini"
        echo "  rag morning"
        ;;
esac
