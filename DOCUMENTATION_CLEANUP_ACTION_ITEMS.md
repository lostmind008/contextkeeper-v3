# ContextKeeper v3.0 Documentation Cleanup Action Items

**Generated**: 2025-07-24  
**Review Scope**: Complete documentation audit for ContextKeeper v3.0 Sacred Layer  
**Current Status**: Phase 3 Complete (MCP Integration) → Phase 4 (Final Testing)

## 🚨 CRITICAL ISSUES FOUND

### 0. **INCORRECT COMMAND SYNTAX** (CRITICAL PRIORITY)
My initial review contained the same type of misinformation I was supposed to find and fix.

**Incorrect Information I Added:**
- README.md Line 206: `python rag_agent.py server --port 5556` - This command doesn't exist
- The rag_agent.py script doesn't accept `--port` argument
- Available commands: start, query, ingest, watch, server (but no port option)

**Action Required:**
- Fix all incorrect command examples in documentation
- Verify all technical details against actual script capabilities
- Remove any non-existent command arguments

### 1. **VERSION MISALIGNMENT** (HIGH PRIORITY)
Multiple documentation files incorrectly show project as v2.0 when it's actually v3.0 Phase 3 Complete.

**Files Affected:**
- `README.md` - Shows v2.0.0 badge, no Sacred Layer mention
- `SETUP.md` - Missing v3.0 Sacred Layer setup steps  
- `API_REFERENCE.md` - Port confusion (5555 vs 5556)
- `QUICK_REFERENCE.md` - No Sacred Layer commands

### 2. **PORT INCONSISTENCIES** (HIGH PRIORITY)
Documentation shows conflicting port numbers for different services.

**Current Reality** (from Phase 3 completion):
- Sacred Layer: Port 5556 ✅
- Legacy v2.0: Port 5555 ✅
- MCP Server: STDIO protocol ✅

**Incorrect References:**
- `API_REFERENCE.md` lines 75-106: Shows port 5556 for LLM queries but port 5555 as base URL
- `README.md` line 118: Shows port 5555 only
- `SETUP.md` line 126: Shows port 5555 only

### 3. **YOUTUBE ANALYZER CONTAMINATION** (HIGH PRIORITY)
Multiple files contain references to unrelated YouTube Analyzer project.

**Out-of-Place File:**
- `youtube_analyzer_integration.py` - ENTIRE FILE should be removed (177 lines of wrong project code)

**Contaminated Files:**
- `README.md` lines 107-111, 119: YouTube-specific commands
- `QUICK_REFERENCE.md` lines 39-53, 87: YouTube Analyzer sections
- File references at line 87: Lists youtube_analyzer_integration.py as project file

### 4. **DUPLICATE INSTRUCTIONS** (MEDIUM PRIORITY)
Some files contain redundant or confusing setup instructions.

**Files Affected:**
- `README.md` lines 63-71 and 79-88: Duplicate "Start the Agent" sections
- `README.md` lines 28-47 and setup instructions: Overlapping dependency setup

### 5. **OUTDATED CLI REFERENCES** (MEDIUM PRIORITY)
Documentation references old CLI commands that may not work with Sacred Layer.

**Files Affected:**
- `QUICK_REFERENCE.md`: No Sacred Layer CLI commands shown
- `README.md`: Missing sacred-specific usage examples

## 🧹 FILES REQUIRING CLEANUP

### **File Removal Required:**
1. `youtube_analyzer_integration.py` - Complete removal (unrelated project)

### **Major Updates Required:**
1. `README.md` - Version update, remove YouTube refs, fix port info, add Sacred Layer
2. `QUICK_REFERENCE.md` - Remove YouTube sections, add Sacred Layer commands
3. `API_REFERENCE.md` - Fix port inconsistencies, clarify service separation
4. `SETUP.md` - Add Sacred Layer setup steps, clarify port configuration

### **Minor Updates Required:**
1. Documentation files referencing youtube_analyzer_integration.py
2. Any remaining v2.0 version references

## 📋 CORRECTIVE ACTIONS REQUIRED

### **Phase 1: Version Alignment**
- [ ] Update README.md version badge from v2.0.0 to v3.0.0
- [ ] Add Sacred Layer features to "What's New" section
- [ ] Remove duplicate setup instructions
- [ ] Add MCP integration highlights

### **Phase 2: Port Standardisation**
- [ ] Document clear service separation:
  - Legacy RAG Agent: localhost:5555
  - Sacred Layer: localhost:5556  
  - MCP Server: STDIO (no HTTP port)
- [ ] Update all API examples with correct ports
- [ ] Add service startup sequence documentation

### **Phase 3: Content Cleanup**
- [ ] Remove youtube_analyzer_integration.py completely
- [ ] Remove all YouTube Analyzer references from documentation
- [ ] Update file listings to reflect actual project structure
- [ ] Remove YouTube-specific CLI commands

### **Phase 4: Sacred Layer Integration**
- [ ] Add Sacred Layer CLI commands to QUICK_REFERENCE.md
- [ ] Include sacred plan workflow examples
- [ ] Document 2-layer verification process
- [ ] Add MCP tool usage examples

### **Phase 5: Accuracy Verification**
- [ ] Cross-reference all technical details against Phase 3 completion status
- [ ] Verify all file paths and references are current
- [ ] Ensure setup instructions reflect v3.0 requirements
- [ ] Test all documented API endpoints and CLI commands

## ⚠️ WHAT NOT TO CHANGE

**Files to Leave Unchanged** (Application Logic):
- `rag_agent.py`
- `sacred_layer_implementation.py`
- `git_activity_tracker.py`
- `enhanced_drift_sacred.py`
- All Python application files
- `rag_cli.sh` and `rag_cli_v2.sh` (CLI delegation pattern is correct)

**Valid File Patterns:**
- `rag_cli.sh` → `rag_cli_v2.sh` delegation is intentional design
- `tests/` directory structure is appropriate
- `v3 Approved Plan for AI Agent/` reference directory should remain

## 🎯 SUCCESS CRITERIA

**Documentation Accuracy:**
- All version references show v3.0
- All port references are service-specific and correct
- No YouTube Analyzer contamination remains
- Sacred Layer features are properly documented

**Technical Accuracy:**
- Setup instructions work for v3.0 Sacred Layer
- API examples use correct endpoints and ports
- CLI commands reflect current capabilities
- MCP integration is properly documented

**Consistency:**
- All documentation files reflect same project status (Phase 3 Complete)
- Port usage is consistent across all documentation
- File references match actual project structure

## 📊 PRIORITY MATRIX

**CRITICAL (Fix First):**
1. Remove youtube_analyzer_integration.py 
2. Fix README.md version and YouTube contamination
3. Resolve port inconsistencies in API_REFERENCE.md

**HIGH:**
1. Update QUICK_REFERENCE.md with Sacred Layer commands
2. Add Sacred Layer setup to SETUP.md
3. Remove YouTube references from all files

**MEDIUM:**
1. Clean up duplicate instructions
2. Improve API documentation clarity
3. Add comprehensive Sacred Layer examples

**LOW:**
1. Minor formatting improvements
2. Update badges and metadata
3. Cross-reference validation

---

**Next Action**: Begin with CRITICAL priority items, focusing on file removal and major version alignment issues first.