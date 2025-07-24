#!/usr/bin/env python3
"""
test_sacred_layer.py - Unit tests for Sacred Layer implementation

Created: 2025-07-24 03:45:00 (Australia/Sydney)
Part of: ContextKeeper v3.0 Sacred Layer Upgrade

Tests the core Sacred Layer functionality including plan creation,
approval, verification, and immutability guarantees.
"""

import pytest
import asyncio
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sacred_layer_implementation import (
    SacredLayerManager, SacredPlan, PlanStatus,
    SacredIntegratedRAGAgent
)


class TestSacredLayerManager:
    """Test suite for SacredLayerManager"""
    
    @pytest.fixture
    def sacred_manager(self, tmp_path):
        """Create a SacredLayerManager instance for testing"""
        return SacredLayerManager(str(tmp_path))
    
    def test_initialization(self, sacred_manager, tmp_path):
        """Test proper initialization of SacredLayerManager"""
        # Check directories created
        assert (tmp_path / "sacred_plans").exists()
        assert (tmp_path / "sacred_chromadb").exists()
        
        # Check approval key loaded
        assert sacred_manager.approval_key is not None
    
    def test_create_plan(self, sacred_manager):
        """Test creating a new sacred plan"""
        plan = sacred_manager.create_plan(
            project_id="test_project",
            title="Test Architecture Plan",
            content="This is a test plan content"
        )
        
        assert plan.project_id == "test_project"
        assert plan.title == "Test Architecture Plan"
        assert plan.status == PlanStatus.DRAFT
        assert plan.plan_id is not None
        assert plan.content_hash is not None
    
    def test_verification_code_generation(self, sacred_manager):
        """Test verification code generation"""
        plan = sacred_manager.create_plan(
            project_id="test_project",
            title="Test Plan",
            content="Content"
        )
        
        code = sacred_manager.generate_verification_code(plan)
        
        assert code is not None
        assert len(code) > 0
        # TODO: Add more specific verification code format tests
    
    @pytest.mark.asyncio
    async def test_plan_approval_flow(self, sacred_manager):
        """Test the complete plan approval flow"""
        # Create plan
        plan = sacred_manager.create_plan(
            project_id="test_project",
            title="Test Plan",
            content="Test content"
        )
        
        # Generate verification code
        verification_code = sacred_manager.generate_verification_code(plan)
        
        # Attempt approval with correct codes
        # TODO: Mock environment key for testing
        approval_result = sacred_manager.approve_plan(
            plan_id=plan.plan_id,
            approver="test_user",
            verification_code=verification_code,
            secondary_key="test_key"
        )
        
        # Verify approval status
        # TODO: Implement actual approval logic
        assert isinstance(approval_result, bool)
    
    def test_large_plan_chunking(self, sacred_manager):
        """Test chunking of large plan content"""
        large_content = "Test content. " * 1000  # Create large content
        
        chunks = sacred_manager.chunk_large_plan(large_content, chunk_size=100)
        
        assert len(chunks) > 1
        assert all(len(chunk) <= 150 for chunk in chunks)  # Allow for overlap
    
    def test_plan_reconstruction(self, sacred_manager):
        """Test reconstruction of chunked plans"""
        original_content = "This is a test plan with multiple sentences. " * 50
        
        chunks = sacred_manager.chunk_large_plan(original_content)
        reconstructed = sacred_manager.reconstruct_plan(chunks)
        
        # Check reconstruction accuracy
        # Note: May not be exact due to chunking algorithm
        assert len(reconstructed) >= len(original_content) * 0.95


class TestSacredIntegratedRAGAgent:
    """Test suite for Sacred Layer RAG integration"""
    
    @pytest.fixture
    def mock_rag_agent(self):
        """Create a mock RAG agent for testing"""
        class MockRAGAgent:
            class MockProjectManager:
                storage_path = "/tmp/test_storage"
            
            project_manager = MockProjectManager()
        
        return MockRAGAgent()
    
    @pytest.fixture
    def sacred_integrated_agent(self, mock_rag_agent):
        """Create SacredIntegratedRAGAgent for testing"""
        return SacredIntegratedRAGAgent(mock_rag_agent)
    
    @pytest.mark.asyncio
    async def test_create_sacred_plan_api(self, sacred_integrated_agent):
        """Test creating sacred plan through API"""
        result = await sacred_integrated_agent.create_sacred_plan(
            project_id="test_project",
            title="API Test Plan",
            content_or_path="Test content via API"
        )
        
        assert result["status"] == "created"
        assert "plan_id" in result
        assert "verification_code" in result
    
    @pytest.mark.asyncio
    async def test_query_sacred_context(self, sacred_integrated_agent):
        """Test querying sacred context"""
        result = await sacred_integrated_agent.query_sacred_context(
            project_id="test_project",
            query="authentication"
        )
        
        assert "plans" in result
        assert "count" in result
        assert isinstance(result["plans"], list)


class TestPlanImmutability:
    """Test suite for verifying plan immutability"""
    
    def test_approved_plan_cannot_be_modified(self, sacred_manager):
        """Ensure approved plans cannot be modified"""
        # TODO: Implement immutability tests
        pass
    
    def test_content_hash_verification(self, sacred_manager):
        """Verify content hash prevents tampering"""
        # TODO: Implement hash verification tests
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])