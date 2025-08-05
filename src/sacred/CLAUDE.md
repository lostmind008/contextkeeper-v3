# CLAUDE.md - Sacred Layer Implementation

This file provides context for Claude Code when working with the Sacred Layer components.

## Directory Purpose
Implements the immutable architectural governance layer that ensures implementation aligns with approved plans. Provides 2-layer verification and drift detection capabilities.

## Key Files
- **`sacred_layer_implementation.py`** (527 lines) ✅ MOVED HERE
  - Immutable plan storage with hash-based IDs
  - 2-layer approval workflow (draft → pending → approved)
  - Isolated ChromaDB collection for sacred documents
  - ✅ Governance header added
  
- **`enhanced_drift_sacred.py`** ✅ MOVED HERE
  - Semantic similarity between plans and implementation
  - Automated drift reporting
  - Plan compliance verification

## Sacred Principles
1. **Immutability**: Approved plans cannot be modified
2. **Verification**: 2-layer approval with SACRED_APPROVAL_KEY
3. **Isolation**: Separate ChromaDB collection from project data
4. **Traceability**: Full audit trail for all plan changes
5. **Drift Detection**: Continuous alignment verification

## Planning Decisions
- 2025-07-20: Decided on 2-layer verification (hash + env key)
- 2025-07-21: Implemented immutable plan storage in ChromaDB
- 2025-07-22: Added drift detection with code alignment checking
- 2025-08-05: Applied governance restructuring

## Workflow
```
Draft Plan → Submit for Approval → Pending → Approve with Key → Locked
                                              ↓
                                        Drift Detection
```

## Dependencies
- **External**: chromadb, langchain_text_splitters
- **Internal**: Core rag_agent for embeddings
- **Environment**: SACRED_APPROVAL_KEY required

## Navigation
- Parent: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/src/
- Core Integration: ../core/rag_agent.py
- CLI Access: ../../scripts/rag_cli_v2.sh sacred
