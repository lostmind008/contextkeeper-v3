# 🚀 LostMind AI - ContextKeeper User Guide

## 🎯 **What is ContextKeeper?**

**LostMind AI - ContextKeeper** is a revolutionary AI-powered development context management system that helps developers maintain clarity, consistency, and control over their projects. It's designed to transform your development workflow with intelligent context tracking, architectural decision management, and AI-driven insights.

### ✨ **Key Features**
- **🤖 AI-Powered Context Tracking** - Automatically tracks and understands your codebase
- **📊 Real-time Analytics** - Monitor project health and performance
- **🎯 Sacred Layer Protection** - Protect architectural decisions from drift
- **🔍 Intelligent Search** - Find relevant code and decisions instantly
- **📈 Project Insights** - Get AI-driven recommendations and patterns

## 🚀 **Getting Started**

### **1. Access the Dashboard**
- **URL**: `http://localhost:5556/analytics_dashboard_live.html`
- **Status**: The dashboard shows real-time project statistics and health

### **2. Current Status**
- ✅ **Server**: Running on port 5556
- ✅ **Health**: All systems operational
- ✅ **Projects**: Currently 0 projects (fresh start)
- ✅ **Analytics**: Live dashboard accessible

## 📋 **How to Use ContextKeeper**

### **Creating Your First Project**

1. **Via Dashboard**:
   - Click "Create New Project" button
   - Enter project name
   - Project will be automatically configured

2. **Via CLI**:
   ```bash
   ./scripts/rag_cli_v2.sh projects create "My Project" "/path/to/project"
   ```

3. **Via API**:
   ```bash
   curl -X POST http://localhost:5556/projects \
     -H "Content-Type: application/json" \
     -d '{
       "name": "My Project",
       "root_path": "/path/to/project",
       "description": "My awesome project"
     }'
   ```

### **Managing Projects**

#### **List All Projects**
```bash
./scripts/rag_cli_v2.sh projects list
```

#### **Focus on a Project**
```bash
./scripts/rag_cli_v2.sh projects focus <project_id>
```

#### **Get Project Status**
```bash
./scripts/rag_cli_v2.sh projects status <project_id>
```

### **Querying Your Codebase**

#### **Ask Questions About Your Code**
```bash
curl -X POST http://localhost:5556/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How is authentication implemented?",
    "project_id": "your_project_id"
  }'
```

#### **Get Code Context**
```bash
curl -X POST http://localhost:5556/code-context \
  -H "Content-Type: application/json" \
  -d '{
    "feature_description": "user authentication",
    "project_id": "your_project_id"
  }'
```

### **Managing Sacred Plans**

#### **Create a Sacred Plan**
```bash
curl -X POST http://localhost:5556/sacred/plans \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "your_project_id",
    "plan_content": "We will use JWT for authentication",
    "approval_key": "your-approval-key"
  }'
```

#### **List Sacred Plans**
```bash
curl -X GET http://localhost:5556/sacred/plans
```

## 🎨 **Dashboard Features**

### **Real-time Statistics**
- **Active Projects**: Number of currently active projects
- **Focused Project**: Currently selected project
- **Total Decisions**: Architectural decisions tracked
- **System Health**: Overall system status

### **Project Management**
- **Project Cards**: Click to focus on a project
- **Status Indicators**: Active, Paused, Archived
- **Quick Actions**: Create, focus, and manage projects

### **Analytics & Insights**
- **Performance Metrics**: Real-time project health
- **Trend Analysis**: Historical data and patterns
- **AI Recommendations**: Intelligent suggestions

## 🔧 **Advanced Features**

### **File Ingestion**
ContextKeeper automatically tracks changes in your project files:

```bash
# Ingest a specific file
curl -X POST http://localhost:5556/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/file.py",
    "project_id": "your_project_id"
  }'
```

### **Git Integration**
- Automatic git activity tracking
- Commit analysis and context preservation
- Branch-specific context management

### **API Integration**
All features are available via RESTful API:
- **Base URL**: `http://localhost:5556`
- **Authentication**: API key based
- **Documentation**: Available at `/docs`

## 🛠️ **Configuration**

### **Environment Variables**
```bash
export GOOGLE_API_KEY="your-google-api-key"
export SACRED_APPROVAL_KEY="your-approval-key"
export ANALYTICS_CACHE_DURATION=300
export FLASK_ASYNC_MODE=True
export DEBUG=0
```

### **Project Configuration**
Projects are stored in `~/.rag_projects/` with JSON configuration files.

## 📊 **Analytics & Monitoring**

### **Dashboard Metrics**
- **Project Health**: Real-time status monitoring
- **Query Activity**: Usage patterns and trends
- **Drift Detection**: Architectural compliance monitoring
- **Performance**: Response times and system metrics

### **Export Options**
- **PDF Reports**: Complete project analytics
- **JSON Data**: Raw analytics data
- **PNG Screenshots**: Dashboard visualizations

## 🚀 **Best Practices**

### **Project Organization**
1. **Clear Naming**: Use descriptive project names
2. **Regular Updates**: Keep project context current
3. **Sacred Plans**: Document important architectural decisions
4. **Monitoring**: Regularly check project health

### **Query Optimization**
1. **Specific Questions**: Ask targeted questions
2. **Context Awareness**: Include relevant project context
3. **Iterative Refinement**: Build on previous queries
4. **Pattern Recognition**: Look for recurring patterns

### **Team Collaboration**
1. **Shared Context**: Use common project configurations
2. **Decision Tracking**: Document team decisions
3. **Knowledge Sharing**: Leverage AI insights across team
4. **Continuous Learning**: Adapt based on AI recommendations

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Dashboard Not Loading**
- Check if server is running: `curl http://localhost:5556/health`
- Verify port 5556 is not blocked
- Check browser console for errors

#### **API Connection Issues**
- Verify environment variables are set
- Check API key validity
- Ensure proper JSON formatting

#### **Project Not Found**
- Verify project ID is correct
- Check project configuration files
- Ensure project is active

### **Performance Optimization**
- **Large Codebases**: Use selective file ingestion
- **Frequent Queries**: Implement caching strategies
- **Memory Usage**: Monitor system resources
- **Response Times**: Optimize query complexity

## 🎯 **Getting Involved**

### **Contribute to ContextKeeper**
- **GitHub**: [https://github.com/lostmind008/contextkeeper-v3](https://github.com/lostmind008/contextkeeper-v3)
- **Issues**: Report bugs and feature requests
- **Pull Requests**: Contribute code improvements
- **Documentation**: Help improve guides and docs

### **Community**
- **Discussions**: Join GitHub discussions
- **Feedback**: Share your experience
- **Ideas**: Suggest new features
- **Showcase**: Share your use cases

## 📞 **Support**

### **Getting Help**
1. **Documentation**: Check this guide and GitHub README
2. **Issues**: Create GitHub issues for bugs
3. **Discussions**: Use GitHub discussions for questions
4. **Community**: Engage with other users

### **Resources**
- **API Reference**: Available in GitHub repository
- **Examples**: Check `/examples` directory
- **Tutorials**: Follow step-by-step guides
- **Videos**: Watch demonstration videos

---

## 🎉 **Ready to Transform Your Development Workflow?**

ContextKeeper is designed to make your development process more intelligent, efficient, and maintainable. Start with a simple project, explore the features, and discover how AI-powered context management can revolutionize your workflow.

**Happy coding with LostMind AI - ContextKeeper! 🚀** 