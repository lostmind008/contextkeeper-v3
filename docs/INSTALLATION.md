# ContextKeeper v3.0 Installation Guide

**Complete installation guide for ContextKeeper v3.0 with multi-project support, sacred architectural governance, and real-time analytics.**

## Prerequisites

- **Python 3.8+** (Python 3.9+ recommended)
- **4GB+ RAM** (8GB+ recommended for large projects)
- **2GB+ disk space** for ChromaDB storage
- **Google Cloud API key** for embeddings and AI features
- **Git** (for cloning repository)

## Quick Installation

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/lostmind008/contextkeeper-v3.git
cd contextkeeper

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create .env file
cp .env.template .env

# Edit with your values
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```env
# Google Cloud (for embeddings and LLM)
GOOGLE_API_KEY=your-google-api-key-here

# Sacred Layer (v3.0)
SACRED_APPROVAL_KEY=your-secure-secret-key

# Optional: Analytics and Performance
DEBUG=0
FLASK_ASYNC_MODE=True
LOG_LEVEL=INFO

# Database Settings (defaults are usually fine)
CHROMADB_PATH=./chromadb
EMBEDDING_MODEL=text-embedding-004
```

### 3. Verify Installation

```bash
# Start ContextKeeper (server-only mode recommended)
python rag_agent.py server

# Test basic functionality
python contextkeeper_cli.py health
# Should return: {"status":"healthy"}

# Test sacred layer
python contextkeeper_cli.py projects list

# Access the dashboard
open http://localhost:5556/dashboard
```

## Google Cloud Setup

### 1. Create Project and Enable APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable these APIs:
   - **Generative AI API** (for Gemini models)
   - **Vertex AI API** (for embeddings)

### 2. Get API Key

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > API Key**
3. Copy the key and add to your `.env` file
4. **Restrict the key** (recommended):
   - Click on the key to edit
   - Under **API restrictions**, select **Restrict key**
   - Choose **Generative AI API** and **Vertex AI API**

### 3. Test API Access

```bash
# Test with a simple curl request
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://generativeai.googleapis.com/v1beta/models"
```

## Detailed Setup Steps

### Virtual Environment Best Practices

```bash
# Use specific Python version (if multiple installed)
python3.9 -m venv venv

# Upgrade pip first
source venv/bin/activate
pip install --upgrade pip

# Install dependencies with specific versions
pip install -r requirements.txt --no-cache-dir

# Verify installation
pip list | grep -E "(flask|chromadb|google|anthropic)"
```

### ChromaDB Configuration

ChromaDB stores your project embeddings and is automatically configured:

```bash
# Default location (configurable in .env)
ls -la chromadb/

# Check storage usage
du -sh chromadb/

# Backup your data (recommended)
cp -r chromadb/ chromadb_backup_$(date +%Y%m%d)
```

### CLI Setup

```bash
# Make CLI executable
chmod +x contextkeeper

# Add to PATH (optional)
echo 'export PATH="$PATH:$(pwd)"' >> ~/.bashrc
source ~/.bashrc

# Test CLI
./contextkeeper health
python contextkeeper_cli.py health
```

## Security Configuration

### Sacred Layer Security

The Sacred Layer provides architectural governance through immutable plans:

```env
# Use a strong, unique key (32+ characters recommended)
SACRED_APPROVAL_KEY=your-very-secure-secret-key-minimum-32-chars

# Optional: Enable audit logging
SACRED_AUDIT_LOG=True
SACRED_LOG_PATH=./logs/sacred_audit.log
```

### API Security

```bash
# Restrict API key access (in Google Cloud Console)
# - Set application restrictions (if running on specific servers)
# - Set API restrictions (Generative AI + Vertex AI only)
# - Monitor usage regularly
```

### Network Security

```bash
# By default, server binds to localhost only
# To allow external access (use with caution):
python rag_agent.py server --host 0.0.0.0 --port 5556

# For production, use reverse proxy (nginx/apache)
# Never expose directly to internet without authentication
```

## Performance Optimization

### System Requirements by Project Size

| Project Size | RAM Recommended | Disk Space | Expected Performance |
|--------------|----------------|------------|---------------------|
| Small (<1k files) | 4GB | 500MB | <500ms queries |
| Medium (1k-10k files) | 8GB | 2GB | <1s queries |
| Large (10k+ files) | 16GB+ | 5GB+ | <2s queries |

### Optimization Settings

```env
# High-performance settings
CHROMADB_THREADS=8
EMBEDDING_BATCH_SIZE=100
QUERY_CACHE_SIZE=1000
MAX_CONCURRENT_QUERIES=10

# Memory optimization
CHROMADB_MEMORY_LIMIT=4GB
EMBEDDING_CACHE_SIZE=10000
```

### File Filtering

Exclude unnecessary files to improve performance:

```python
# Built-in exclusions (automatically applied)
EXCLUDED_PATTERNS = [
    'node_modules/', '.git/', '__pycache__/', '.venv/', 'venv/',
    '.pytest_cache/', '.mypy_cache/', 'dist/', 'build/',
    '*.pyc', '*.log', '*.tmp', '.DS_Store'
]
```

## Production Deployment

### Using Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5556

CMD ["python", "rag_agent.py", "server", "--host", "0.0.0.0"]
```

```bash
# Build and run
docker build -t contextkeeper:latest .
docker run -d -p 5556:5556 --env-file .env contextkeeper:latest
```

### Using systemd (Linux)

```ini
[Unit]
Description=ContextKeeper v3.0
After=network.target

[Service]
Type=simple
User=contextkeeper
WorkingDirectory=/opt/contextkeeper
Environment=PATH=/opt/contextkeeper/venv/bin
ExecStart=/opt/contextkeeper/venv/bin/python rag_agent.py server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable contextkeeper
sudo systemctl start contextkeeper
sudo systemctl status contextkeeper
```

### Reverse Proxy (nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5556;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support for dashboard
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Troubleshooting Installation

### Common Issues

**Python Version Conflicts**
```bash
# Check Python version
python3 --version

# Use specific Python version
/usr/bin/python3.9 -m venv venv
```

**Permission Errors**
```bash
# Fix permissions
chmod -R 755 contextkeeper/
chown -R $USER:$USER contextkeeper/

# On Windows, run as Administrator if needed
```

**Google API Errors**
```bash
# Test API key
export GOOGLE_API_KEY="your-key-here"
python -c "
import google.generativeai as genai
genai.configure(api_key='$GOOGLE_API_KEY')
print('API key works!')
"
```

**ChromaDB Issues**
```bash
# Reset ChromaDB
rm -rf chromadb/
python rag_agent.py server  # Will recreate database

# Check disk space
df -h .
```

**Port Conflicts**
```bash
# Check what's using port 5556
lsof -i :5556
netstat -tulpn | grep 5556

# Use different port
python rag_agent.py server --port 5557
```

### Installation Verification Checklist

```bash
# Run these commands to verify everything works

# 1. Check virtual environment
which python
python --version

# 2. Check dependencies
pip list | grep -E "(flask|chromadb|google)"

# 3. Check environment variables
python -c "import os; print('GOOGLE_API_KEY:', bool(os.getenv('GOOGLE_API_KEY')))"

# 4. Test server startup
python rag_agent.py server --test

# 5. Test CLI
python contextkeeper_cli.py health

# 6. Test API
curl http://localhost:5556/health

# 7. Test dashboard
curl -I http://localhost:5556/dashboard
```

## Getting Started After Installation

### 1. Create Your First Project
```bash
python contextkeeper_cli.py projects create "My First Project" /path/to/your/code
```

### 2. Start Exploring
```bash
python contextkeeper_cli.py ask "What does this project do?"
```

### 3. Try the Dashboard
Open `http://localhost:5556/dashboard` in your browser

### 4. Create Sacred Plan
```bash
python contextkeeper_cli.py sacred create <project_id> "Architecture Plan" architecture.md
```

## Next Steps

- [User Guide](USER_GUIDE.md) - Learn how to use ContextKeeper
- [API Reference](API_REFERENCE.md) - Complete API documentation  
- [Sacred Layer Guide](SACRED_LAYER.md) - Architectural governance
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions

## Support

If you encounter issues during installation:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search existing [GitHub Issues](https://github.com/lostmind008/contextkeeper-v3/issues)
3. Create a new issue with:
   - Operating system and Python version
   - Complete error messages
   - Output of `python contextkeeper_cli.py health --verbose`

---

**Installation Support**: August 2025 | **Tested On**: macOS, Ubuntu 20+, Windows 10+