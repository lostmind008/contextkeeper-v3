#!/usr/bin/env python3
"""
Test script for sacred analytics implementation
"""

import asyncio
import logging
from analytics.sacred_metrics import SacredMetricsCalculator
from analytics.analytics_service import AnalyticsService
from sacred_layer_implementation import SacredLayerManager
from enhanced_drift_sacred import SacredDriftDetector

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockProjectManager:
    """Mock project manager for testing"""
    def __init__(self):
        self.projects = {
            'test_project_1': {'id': 'test_project_1', 'name': 'Test Project 1'},
            'test_project_2': {'id': 'test_project_2', 'name': 'Test Project 2'}
        }
    
    async def list_projects(self):
        return list(self.projects.values())

class MockAgent:
    """Mock agent for testing"""
    def __init__(self):
        self.config = {'db_path': '/tmp/test_db'}
    
    async def embed_text(self, text):
        # Simple mock embedding - just return a list of zeros
        return [0.0] * 384

async def test_analytics():
    """Test the analytics implementation"""
    try:
        print("🧪 Testing Sacred Analytics Implementation")
        print("=" * 50)
        
        # Create mock components
        mock_agent = MockAgent()
        mock_project_manager = MockProjectManager()
        
        # Initialize sacred manager with mock embedder
        sacred_manager = SacredLayerManager('/tmp/test_sacred_db', mock_agent)
        print("✓ Sacred manager initialized")
        
        # Initialize drift detector
        drift_detector = SacredDriftDetector(mock_agent, sacred_manager)
        print("✓ Drift detector initialized")
        
        # Initialize metrics calculator
        metrics_calculator = SacredMetricsCalculator(
            sacred_manager,
            drift_detector,
            mock_project_manager
        )
        print("✓ Metrics calculator initialized")
        
        # Test overall metrics calculation
        print("\n📊 Testing Overall Metrics Calculation...")
        overall_metrics = await metrics_calculator.calculate_overall_metrics()
        print(f"✓ Overall metrics: {overall_metrics}")
        
        # Test project metrics calculation
        print("\n📈 Testing Project Metrics Calculation...")
        project_metrics = await metrics_calculator.calculate_project_metrics()
        print(f"✓ Project metrics: {len(project_metrics)} projects analyzed")
        
        # Test analytics service
        print("\n🔬 Testing Analytics Service...")
        analytics_service = AnalyticsService(metrics_calculator)
        
        result = await analytics_service.get_sacred_analytics()
        print("✓ Sacred analytics calculated successfully")
        
        # Print summary
        print(f"  - Total projects: {result['overall_metrics']['total_projects']}")
        print(f"  - Projects with plans: {result['overall_metrics']['projects_with_plans']}")
        print(f"  - Sacred coverage: {result['overall_metrics']['sacred_coverage_percentage']}%")
        
        # Test health check
        print("\n🏥 Testing Health Check...")
        health = await analytics_service.get_sacred_health_check()
        print(f"✓ Health check status: {health['status']}")
        
        print("\n🎉 All tests passed! Analytics implementation is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        logger.error("Test failed", exc_info=True)
        return False

if __name__ == "__main__":
    success = asyncio.run(test_analytics())
    exit(0 if success else 1)