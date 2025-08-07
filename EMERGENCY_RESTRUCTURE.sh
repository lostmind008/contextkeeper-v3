#!/bin/bash
# Emergency Restructure Script
# Run this to implement proper governance protocol

echo "🚨 EMERGENCY CONTEXTKEEPER RESTRUCTURE 🚨"
echo "Implementing governance protocol to fix architecture violations..."

# Create proper directory structure
echo "Creating proper directory structure..."
mkdir -p src/{core,api,sacred,analytics,dashboard,mcp,projects}
mkdir -p src/dashboard/{components,styles}
mkdir -p docs/{planning,archive,guides}

# Archive documentation sprawl
echo "Archiving documentation sprawl..."
mv *_REPORT.md docs/archive/ 2>/dev/null || true
mv *_SUMMARY.md docs/archive/ 2>/dev/null || true
mv *_ANALYSIS.md docs/archive/ 2>/dev/null || true
mv *_DEBUG*.md docs/archive/ 2>/dev/null || true
mv *_FIX*.md docs/archive/ 2>/dev/null || true
mv COMPREHENSIVE_*.md docs/archive/ 2>/dev/null || true

# Keep essential docs in root
echo "Organizing essential documentation..."
# Keep: README.md, CLAUDE.md, PROJECT_MAP.md, ARCHITECTURE.md, CHANGELOG.md

# Move components to proper structure
echo "Moving components to proper directories..."
mv analytics_integration.py src/ck_analytics/ 2>/dev/null || true
mv analytics_dashboard_live.html src/dashboard/ 2>/dev/null || true
mv sacred_layer_implementation.py src/sacred/ 2>/dev/null || true
mv enhanced_drift_sacred.py src/sacred/ 2>/dev/null || true
mv project_manager.py src/projects/ 2>/dev/null || true

echo "✅ Phase 1 complete. Project structure reorganised."
echo "Next: Create CLAUDE.md files for each directory"
echo "Next: Split monolithic files into skeletons"
