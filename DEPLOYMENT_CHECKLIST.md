# ContextKeeper v3.0 Production Deployment Checklist

## 📋 Overview

This comprehensive checklist covers all aspects of deploying ContextKeeper v3.0 to production, including infrastructure setup, security hardening, monitoring configuration, and rollback procedures.

**System Components**:
- Python Flask API (Port 5556)
- ChromaDB Vector Storage
- Google Gemini API Integration
- Sacred Layer for Architectural Plans
- MCP Server for Claude Code Integration
- Git Activity Tracking

## ✅ Pre-Deployment Checklist

### 1. Environment Requirements

- [ ] **Python Version**: 3.8+ installed
- [ ] **Virtual Environment**: Created and activated
- [ ] **System Resources**:
  - [ ] Minimum 4GB RAM
  - [ ] 10GB+ free disk space for ChromaDB storage
  - [ ] 2+ CPU cores recommended
- [ ] **Network Requirements**:
  - [ ] Port 5556 available for Flask API
  - [ ] Outbound HTTPS access to Google AI APIs
  - [ ] Firewall rules configured

### 2. API Keys and Credentials

- [ ] **Google AI API Key** obtained from https://aistudio.google.com/app/apikey
- [ ] **Sacred Approval Key** generated (32+ characters)
  ```bash
  # Generate secure key
  openssl rand -hex 32
  ```
- [ ] **Environment File** created from template:
  ```bash
  cp .env.template .env
  # Remove 'export' statements
  # Fill in actual values
  ```

### 3. Code Repository

- [ ] **Clone Repository** to production server
- [ ] **Checkout Stable Branch/Tag**
  ```bash
  git checkout v3.0-stable  # or specific release tag
  ```
- [ ] **Verify File Integrity**
  ```bash
  # Check critical files exist
  ls -la rag_agent.py project_manager.py sacred_layer_implementation.py
  ls -la mcp-server/enhanced_mcp_server.js
  ```

## 🚀 Deployment Steps

### Phase 1: Infrastructure Setup

#### 1.1 System Dependencies

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install Python dependencies
sudo apt-get install -y python3-pip python3-venv python3-dev

# Install Git (if not present)
sudo apt-get install -y git

# Install Node.js for MCP server (if using)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 1.2 Application Setup

```bash
# Navigate to deployment directory
cd /opt/contextkeeper  # or your chosen directory

# Clone repository (if not done)
git clone https://github.com/your-repo/contextkeeper.git
cd contextkeeper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Setup MCP server dependencies (if using)
cd mcp-server
npm install
cd ..
```

#### 1.3 Directory Structure

```bash
# Create required directories
mkdir -p ~/.rag_projects
mkdir -p rag_knowledge_db/sacred_plans
mkdir -p rag_knowledge_db/sacred_chromadb
mkdir -p logs
mkdir -p backups

# Set permissions
chmod 755 ~/.rag_projects
chmod 755 rag_knowledge_db
chmod 755 logs
```

### Phase 2: Configuration

#### 2.1 Environment Configuration

```bash
# Edit .env file
nano .env

# Required values:
GOOGLE_API_KEY=your-google-ai-api-key
GEMINI_API_KEY=your-google-ai-api-key
SACRED_APPROVAL_KEY=your-32-char-minimum-key

# Optional production settings:
FLASK_DEBUG=false
LOG_LEVEL=INFO
CONTEXTKEEPER_HOST=0.0.0.0  # For external access
CONTEXTKEEPER_PORT=5556
```

#### 2.2 Application Configuration

```python
# Create production config file: config/production.py
import os

class ProductionConfig:
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # Security
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', os.urandom(32))
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/contextkeeper.log'
    
    # ChromaDB
    CHROMADB_PERSIST_DIR = './rag_knowledge_db'
    
    # API Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "100 per hour"
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:*', 'https://yourdomain.com']
```

#### 2.3 Nginx Reverse Proxy (Recommended)

```nginx
# /etc/nginx/sites-available/contextkeeper
server {
    listen 80;
    server_name contextkeeper.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name contextkeeper.yourdomain.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/contextkeeper.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/contextkeeper.yourdomain.com/privkey.pem;
    
    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    # Proxy settings
    location / {
        proxy_pass http://127.0.0.1:5556;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for real-time features
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # API rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://127.0.0.1:5556;
    }
}
```

### Phase 3: Security Hardening

#### 3.1 API Security

- [ ] **Enable API Key Authentication**
  ```python
  # Add to rag_agent.py
  from functools import wraps
  
  def require_api_key(f):
      @wraps(f)
      def decorated_function(*args, **kwargs):
          api_key = request.headers.get('X-API-Key')
          if not api_key or api_key != os.environ.get('API_KEY'):
              return jsonify({'error': 'Invalid API key'}), 401
          return f(*args, **kwargs)
      return decorated_function
  ```

- [ ] **Implement Rate Limiting**
  ```bash
  pip install flask-limiter
  ```

- [ ] **Enable HTTPS Only** (via Nginx)

- [ ] **Configure CORS Properly**
  ```python
  CORS(app, origins=['https://yourdomain.com'])
  ```

#### 3.2 File System Security

```bash
# Restrict file permissions
chmod 600 .env
chmod 700 rag_knowledge_db
chmod 700 ~/.rag_projects

# Create dedicated user
sudo useradd -r -s /bin/false contextkeeper
sudo chown -R contextkeeper:contextkeeper /opt/contextkeeper
```

#### 3.3 Database Security

- [ ] **ChromaDB Access Control**
  ```python
  # Configure ChromaDB with authentication
  chroma_client = chromadb.Client(Settings(
      chroma_db_impl="duckdb+parquet",
      persist_directory="./rag_knowledge_db",
      anonymized_telemetry=False
  ))
  ```

- [ ] **Backup Encryption**
  ```bash
  # Encrypt backups
  tar -czf - rag_knowledge_db | openssl enc -aes-256-cbc -salt -out backup.tar.gz.enc
  ```

### Phase 4: Service Configuration

#### 4.1 Systemd Service

```ini
# /etc/systemd/system/contextkeeper.service
[Unit]
Description=ContextKeeper RAG Service
After=network.target

[Service]
Type=simple
User=contextkeeper
Group=contextkeeper
WorkingDirectory=/opt/contextkeeper
Environment="PATH=/opt/contextkeeper/venv/bin"
ExecStart=/opt/contextkeeper/venv/bin/python /opt/contextkeeper/rag_agent.py start
Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/contextkeeper/rag_knowledge_db /opt/contextkeeper/logs

# Resource limits
LimitNOFILE=65536
MemoryLimit=4G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
```

#### 4.2 Enable and Start Service

```bash
# Enable service
sudo systemctl daemon-reload
sudo systemctl enable contextkeeper.service

# Start service
sudo systemctl start contextkeeper.service

# Check status
sudo systemctl status contextkeeper.service
```

### Phase 5: Monitoring Setup

#### 5.1 Application Monitoring

```python
# Add health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check ChromaDB connection
        collections = chroma_client.list_collections()
        
        # Check disk space
        import shutil
        disk_usage = shutil.disk_usage('/')
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'chromadb_collections': len(collections),
            'disk_free_gb': disk_usage.free // (2**30)
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
```

#### 5.2 Log Rotation

```bash
# /etc/logrotate.d/contextkeeper
/opt/contextkeeper/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 contextkeeper contextkeeper
    sharedscripts
    postrotate
        systemctl reload contextkeeper.service > /dev/null 2>&1 || true
    endscript
}
```

#### 5.3 Prometheus Metrics (Optional)

```python
# Install prometheus client
pip install prometheus-client

# Add metrics endpoint
from prometheus_client import Counter, Histogram, generate_latest

query_counter = Counter('contextkeeper_queries_total', 'Total queries processed')
query_duration = Histogram('contextkeeper_query_duration_seconds', 'Query duration')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

#### 5.4 Alerting Setup

```yaml
# alertmanager.yml
alerts:
  - name: ContextKeeperDown
    expr: up{job="contextkeeper"} == 0
    for: 5m
    annotations:
      summary: "ContextKeeper is down"
      
  - name: HighMemoryUsage
    expr: process_resident_memory_bytes{job="contextkeeper"} > 3e+9
    for: 10m
    annotations:
      summary: "High memory usage detected"
      
  - name: APIErrors
    expr: rate(contextkeeper_errors_total[5m]) > 0.1
    annotations:
      summary: "High error rate detected"
```

## 🔄 Rollback Procedures

### Quick Rollback (< 5 minutes)

```bash
# 1. Stop current service
sudo systemctl stop contextkeeper

# 2. Restore previous version
cd /opt/contextkeeper
git checkout previous-tag  # or commit hash

# 3. Restore database if needed
cp -r backups/[timestamp]/rag_knowledge_db ./

# 4. Restart service
sudo systemctl start contextkeeper

# 5. Verify health
curl http://localhost:5556/health
```

### Full Rollback (Including Data)

```bash
# 1. Create rollback script
cat > rollback.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/contextkeeper/backups/$(date +%Y%m%d_%H%M%S)"

# Stop service
systemctl stop contextkeeper

# Backup current state
mkdir -p $BACKUP_DIR
cp -r rag_knowledge_db $BACKUP_DIR/
cp .env $BACKUP_DIR/
git rev-parse HEAD > $BACKUP_DIR/git_commit.txt

# Restore from backup
RESTORE_FROM="$1"
if [ -z "$RESTORE_FROM" ]; then
    echo "Usage: ./rollback.sh backup_timestamp"
    exit 1
fi

cp -r backups/$RESTORE_FROM/rag_knowledge_db ./
cp backups/$RESTORE_FROM/.env ./

# Restore code
git checkout $(cat backups/$RESTORE_FROM/git_commit.txt)

# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt

# Start service
systemctl start contextkeeper

echo "Rollback complete. Verify at http://localhost:5556/health"
EOF

chmod +x rollback.sh
```

## 📊 Post-Deployment Verification

### 1. Health Checks

```bash
# API health
curl http://localhost:5556/health

# Project listing
curl http://localhost:5556/projects

# Test query
curl -X POST http://localhost:5556/query \
  -H "Content-Type: application/json" \
  -d '{"question": "test query", "k": 5, "project_id": "test-project"}'
```

### 2. Performance Baseline

```bash
# Run performance test
python tests/performance/benchmark.py

# Expected metrics:
# - Query response time: < 2 seconds
# - Indexing speed: > 10 files/second
# - Memory usage: < 2GB idle, < 4GB under load
```

### 3. Security Scan

```bash
# Run security checks
pip install safety bandit

# Check dependencies
safety check

# Scan code
bandit -r . -f json -o security_scan.json
```

## 🚨 Emergency Procedures

### Service Unresponsive

```bash
# 1. Check process
ps aux | grep rag_agent

# 2. Check logs
tail -f /opt/contextkeeper/logs/contextkeeper.log

# 3. Restart service
sudo systemctl restart contextkeeper

# 4. If still failing, check resources
df -h  # Disk space
free -m  # Memory
```

### Database Corruption

```bash
# 1. Stop service
sudo systemctl stop contextkeeper

# 2. Backup corrupted DB
mv rag_knowledge_db rag_knowledge_db.corrupted

# 3. Restore from backup
cp -r backups/last_known_good/rag_knowledge_db ./

# 4. Reindex if needed
python rag_agent.py reindex --all-projects
```

### API Key Compromise

```bash
# 1. Immediately revoke compromised key in Google AI Console

# 2. Generate new key

# 3. Update .env file
nano .env  # Update GOOGLE_API_KEY and GEMINI_API_KEY

# 4. Restart service
sudo systemctl restart contextkeeper

# 5. Update any client applications
```

## 📝 Maintenance Tasks

### Daily
- [ ] Check service health endpoint
- [ ] Review error logs for anomalies
- [ ] Monitor disk space usage

### Weekly
- [ ] Backup ChromaDB database
- [ ] Review API usage metrics
- [ ] Update security patches

### Monthly
- [ ] Full system backup
- [ ] Performance analysis
- [ ] Review and rotate logs
- [ ] Update dependencies (test first)

## 🔧 Troubleshooting Guide

### Common Issues

1. **ChromaDB Connection Errors**
   ```bash
   # Check if ChromaDB directory exists and has correct permissions
   ls -la rag_knowledge_db/
   # Ensure the user running the service has write access
   ```

2. **High Memory Usage**
   ```bash
   # Adjust collection size limits
   # Implement periodic garbage collection
   # Consider moving to cloud vector DB
   ```

3. **Slow Query Performance**
   ```bash
   # Check index size
   du -sh rag_knowledge_db/
   # Consider pruning old data
   # Optimize embedding batch size
   ```

## 📚 Additional Resources

- [ContextKeeper Documentation](./docs/)
- [API Reference](./docs/api/API_REFERENCE.md)
- [Architecture Guide](./docs/ARCHITECTURE.md)
- [Troubleshooting Guide](./docs/TROUBLESHOOTING.md)
- [Security Guidelines](./docs/SECURITY_GUIDELINES.md)

## ✅ Sign-Off Checklist

Before considering deployment complete:

- [ ] All health checks passing
- [ ] Monitoring alerts configured
- [ ] Backups automated and tested
- [ ] Documentation updated
- [ ] Team trained on procedures
- [ ] Emergency contacts documented
- [ ] First week of logs reviewed
- [ ] Performance baselines established

---

**Last Updated**: 2025-07-30  
**Version**: 3.0  
**Maintained By**: DevOps Team