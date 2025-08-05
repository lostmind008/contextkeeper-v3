#!/usr/bin/env python3
"""
Critical fix for vector search cross-contamination issue.
This script fixes the ingestion endpoint to require project_id.
"""

def main():
    print("Applying isolation fix...")
    
    # Read the file
    with open('rag_agent.py', 'r') as f:
        content = f.read()
    
    # Find and replace the problematic code
    old_code = """            data = request.json
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
            
            return jsonify({'chunks_ingested': chunks})"""
    
    new_code = """            data = request.json
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
            
            return jsonify({'chunks_ingested': chunks})"""
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open('rag_agent.py', 'w') as f:
            f.write(content)
        print("✅ Fixed ingestion endpoint isolation issue")
    else:
        print("❌ Could not find target code to fix")

if __name__ == "__main__":
    main()