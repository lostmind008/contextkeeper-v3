#!/bin/bash

echo "🚀 Setting up ContextKeeper v3 Development Environment..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create environment file from template
echo "🔧 Setting up environment configuration..."
if [ ! -f .env ]; then
    cp .env.template .env
    echo "✅ .env file created from template"
    echo "⚠️  Please add your API keys to the .env file"
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating required directories..."
mkdir -p rag_knowledge_db
mkdir -p logs
mkdir -p sacred_plans

# Set proper permissions
echo "🔒 Setting permissions..."
chmod +x scripts/*.sh
chmod +x .devcontainer/setup.sh

# Install MCP server dependencies
echo "🔌 Installing MCP server dependencies..."
cd mcp-server
npm install
cd ..

# Run initial tests
echo "🧪 Running initial tests..."
python -m pytest tests/ -v --tb=short || echo "⚠️  Some tests failed - check configuration"

echo ""
echo "✅ ContextKeeper v3 setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Add your API keys to .env file:"
echo "   - GOOGLE_API_KEY=your_google_api_key"
echo "   - GEMINI_API_KEY=your_gemini_api_key"
echo "2. Start the server: source venv/bin/activate && python rag_agent.py start"
echo "3. Test with: ./scripts/rag_cli_v2.sh projects list"
echo ""
echo "📚 Documentation: https://github.com/lostmind008/contextkeeper-v3"
echo "🔧 Troubleshooting: docs/TROUBLESHOOTING.md"