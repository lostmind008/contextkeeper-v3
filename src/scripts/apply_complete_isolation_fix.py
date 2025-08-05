#!/usr/bin/env python3
"""
Apply complete isolation fix for the vector search cross-contamination issue.
This fixes both the ingestion endpoint and directory ingestion method.
"""

import os
import shutil
from datetime import datetime

def apply_complete_fix():
    """Apply all necessary fixes to resolve cross-contamination"""
    
    rag_agent_path = "/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/rag_agent.py"
    backup_path = f"{rag_agent_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print("🔧 Applying Complete Vector Search Isolation Fix")
    print("=" * 60)
    
    # Create backup
    shutil.copy2(rag_agent_path, backup_path)
    print(f"✅ Created backup: {backup_path}")
    
    # Read the current file
    with open(rag_agent_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Secure the ingestion endpoint
    old_ingest_endpoint = '''            data = request.json
            path = data.get('path', '')
            
            if not path or not os.path.exists(path):
                return jsonify({'error': 'Valid path required'}), 400
            
            if os.path.isfile(path):
                # Check if single file should be ignored
                if self.agent.path_filter.should_ignore_path(path):
                    return jsonify({'error': 'File path is ignored by configuration', 'chunks_ingested': 0})
                chunks = self._run_async(self.agent.ingest_file(path))
            else:
                chunks = self._run_async(self.agent.ingest_directory(path))
            
            return jsonify({'chunks_ingested': chunks})'''
    
    new_ingest_endpoint = '''            data = request.json
            path = data.get('path', '')
            project_id = data.get('project_id')  # CRITICAL: Extract project_id from request
            
            if not path or not os.path.exists(path):
                return jsonify({'error': 'Valid path required'}), 400
            
            # CRITICAL: Enforce project isolation - require project_id for security
            if not project_id:
                return jsonify({'error': 'project_id required for secure ingestion'}), 400
            
            # Validate project exists
            if project_id not in self.agent.collections:
                # Try to initialize collections in case project was just created
                self.agent._init_project_collections()
                if project_id not in self.agent.collections:
                    return jsonify({'error': f'Project {project_id} not found or not accessible'}), 404
            
            if os.path.isfile(path):
                # Check if single file should be ignored
                if self.agent.path_filter.should_ignore_path(path):
                    return jsonify({'error': 'File path is ignored by configuration', 'chunks_ingested': 0})
                chunks = self._run_async(self.agent.ingest_file(path, project_id))
            else:
                chunks = self._run_async(self.agent.ingest_directory(path, project_id))
            
            # Security audit logging
            logger.info(f"Ingestion completed - Project: {project_id}, Path: {path}, Chunks: {chunks}")
            
            return jsonify({'chunks_ingested': chunks})'''
    
    # Fix 2: Update ingest_directory method
    old_ingest_directory = '''    async def ingest_directory(self, directory: str) -> int:
        """Recursively ingest all files in a directory"""
        total_chunks = 0
        
        for root, dirs, files in os.walk(directory):
            # Filter out directories that should be ignored
            dirs[:] = [d for d in dirs if not self.path_filter.should_ignore_directory(d)]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.config['default_file_extensions']):
                    file_path = os.path.join(root, file)
                    
                    # Check if the full path should be ignored (comprehensive check)
                    if self.path_filter.should_ignore_path(file_path):
                        continue
                    
                    chunks = await self.ingest_file(file_path)
                    total_chunks += chunks
        
        return total_chunks'''
    
    new_ingest_directory = '''    async def ingest_directory(self, directory: str, project_id: str = None) -> int:
        """Recursively ingest all files in a directory for a specific project"""
        total_chunks = 0
        
        for root, dirs, files in os.walk(directory):
            # Filter out directories that should be ignored
            dirs[:] = [d for d in dirs if not self.path_filter.should_ignore_directory(d)]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.config['default_file_extensions']):
                    file_path = os.path.join(root, file)
                    
                    # Check if the full path should be ignored (comprehensive check)
                    if self.path_filter.should_ignore_path(file_path):
                        continue
                    
                    chunks = await self.ingest_file(file_path, project_id)  # FIXED: Pass project_id
                    total_chunks += chunks
        
        return total_chunks'''
    
    fixes_applied = 0
    
    # Apply Fix 1: Ingestion endpoint
    if old_ingest_endpoint in content:
        content = content.replace(old_ingest_endpoint, new_ingest_endpoint)
        fixes_applied += 1
        print("✅ Fixed ingestion endpoint - now enforces project_id requirement")
    else:
        print("⚠️  Could not find ingestion endpoint code to fix")
    
    # Apply Fix 2: Directory ingestion method
    if old_ingest_directory in content:
        content = content.replace(old_ingest_directory, new_ingest_directory)
        fixes_applied += 1
        print("✅ Fixed ingest_directory method - now accepts and passes project_id")
    else:
        print("⚠️  Could not find ingest_directory method code to fix")
    
    # Write the fixed content back
    if fixes_applied > 0:
        with open(rag_agent_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n🎯 Applied {fixes_applied}/2 critical isolation fixes!")
        print("\nFixes Applied:")
        print("  1. ✅ Ingestion endpoint now requires project_id")
        print("  2. ✅ Directory ingestion passes project_id to file ingestion")
        print("  3. ✅ Added project validation and security logging")
        print("  4. ✅ Enforces strict project isolation")
        
        print(f"\n📄 Backup created at: {backup_path}")
        print("\n🧪 Next Steps:")
        print("  1. Restart the RAG agent service")
        print("  2. Run: python test_isolation_advanced.py")
        print("  3. Verify all tests pass with no cross-contamination")
        
        return True
    else:
        print("\n❌ No fixes could be applied - code may have already been modified")
        return False

if __name__ == "__main__":
    success = apply_complete_fix()
    exit(0 if success else 1)