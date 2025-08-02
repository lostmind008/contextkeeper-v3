# CRITICAL FIX REQUIRED: Vector Search Cross-Contamination

## Issue Identified
Projects can see each other's data due to ingestion endpoint bug.

## Root Cause
The `/ingest` endpoint doesn't require `project_id`, causing data to go to wrong projects.

## Fix Required in rag_agent.py

### 1. Line ~883: Add project_id extraction
```python
project_id = data.get('project_id')  # CRITICAL: Extract project_id from request
```

### 2. Lines ~885-890: Add project_id validation  
```python
# CRITICAL: Enforce project isolation - require project_id for security
if not project_id:
    return jsonify({'error': 'project_id required for secure ingestion'}), 400

# Validate project exists
if project_id not in self.agent.collections:
    # Try to initialize collections in case project was just created
    self.agent._init_project_collections()
    if project_id not in self.agent.collections:
        return jsonify({'error': f'Project {project_id} not found or not accessible'}), 404
```

### 3. Lines ~892, 894: Pass project_id to ingestion methods
```python
chunks = self._run_async(self.agent.ingest_file(path, project_id))
chunks = self._run_async(self.agent.ingest_directory(path, project_id))
```

### 4. Line ~625: Update ingest_directory signature
```python
async def ingest_directory(self, directory: str, project_id: str = None) -> int:
```

### 5. Line ~641: Pass project_id in ingest_directory
```python
chunks = await self.ingest_file(file_path, project_id)  # FIXED: Pass project_id
```

## Test After Fix
```bash
python test_isolation_advanced.py
```

Should pass all tests with no cross-contamination.