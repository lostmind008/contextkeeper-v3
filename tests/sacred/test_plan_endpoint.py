#!/usr/bin/env python3
"""Tests for sacred plan retrieval endpoint"""

from unittest.mock import Mock, patch
from rag_agent import RAGServer
from src.sacred.sacred_layer_implementation import SacredPlan, PlanStatus


def test_get_sacred_plan_endpoint():
    plan = SacredPlan(
        plan_id="plan123",
        project_id="proj1",
        title="Test Plan",
        content="Plan content",
        status=PlanStatus.DRAFT,
        created_at="2025-01-01T00:00:00",
        approved_at=None,
        approved_by=None,
        verification_code=None
    )

    sacred_manager = Mock(plans_registry={"plan123": plan})
    agent = Mock(
        project_manager=Mock(),
        sacred_integration=Mock(sacred_manager=sacred_manager)
    )

    with patch('rag_agent.add_sacred_drift_endpoint'):
        server = RAGServer(agent)
        client = server.app.test_client()
        resp = client.get('/sacred/plans/plan123')

    assert resp.status_code == 200
    data = resp.get_json()
    assert data['plan_id'] == 'plan123'
    assert data['content'] == 'Plan content'
