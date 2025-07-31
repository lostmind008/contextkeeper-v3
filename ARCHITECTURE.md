# Technical Architecture: Sacred Metrics Analytics Endpoint

## Overview
Design for comprehensive sacred plan analytics endpoint to support the analytics dashboard with detailed metrics on plan adherence, drift detection, and governance insights.

## Database Schema Enhancement

The system utilises existing data structures from:
- `sacred_layer_implementation.py`: Plans registry and ChromaDB collections
- `enhanced_drift_sacred.py`: Drift analysis data
- `git_activity_tracker.py`: Git activity metrics

### Sacred Plans Registry Structure (Existing)
```python
# In SacredLayerManager.plans_registry
{
    "plan_id": {
        "plan": SacredPlan,
        "status": PlanStatus,  # DRAFT, APPROVED, LOCKED, SUPERSEDED
        "created_at": datetime,
        "approved_at": Optional[datetime],
        "locked_at": Optional[datetime],
        "superseded_by": Optional[str],
        "approver": Optional[str],
        "verification_code": str,
        "secondary_verification": str,
        "file_path": Optional[str]
    }
}
```

### Proposed Analytics Aggregation Structure
```python
# New metrics structure for /analytics/sacred endpoint
{
    "overall_metrics": {
        "total_projects": int,
        "projects_with_plans": int,
        "sacred_coverage_percentage": float,
        "total_plans": int,
        "approved_plans": int,
        "compliance_rate": float,
        "avg_adherence_score": float
    },
    "project_metrics": [
        {
            "project_id": str,
            "project_name": str,
            "plan_count": int,
            "approved_plans": int,
            "adherence_score": float,  # 0-100
            "drift_warnings": int,
            "last_drift_check": datetime,
            "status_breakdown": {
                "DRAFT": int,
                "APPROVED": int,
                "LOCKED": int,
                "SUPERSEDED": int
            }
        }
    ],
    "recent_activity": [
        {
            "type": str,  # "plan_created", "plan_approved", "drift_detected"
            "project_id": str,
            "plan_id": Optional[str],
            "timestamp": datetime,
            "details": str
        }
    ],
    "drift_analysis": {
        "total_drift_events": int,
        "projects_with_drift": int,
        "avg_drift_severity": float,
        "recent_drift_events": List[Dict]
    }
}
```

## API Endpoints Design

### Primary Endpoint: /analytics/sacred
**Method**: GET  
**Purpose**: Comprehensive sacred plan analytics for dashboard

**Query Parameters**:
- `timeframe`: Optional[str] = "7d" (1d, 7d, 30d, 90d)
- `project_filter`: Optional[str] = Project ID filter
- `include_history`: Optional[bool] = False (include historical trends)

**Response Structure**:
```json
{
    "timestamp": "2025-07-31T14:30:00Z",
    "timeframe": "7d",
    "overall_metrics": {
        "total_projects": 12,
        "projects_with_plans": 8,
        "sacred_coverage_percentage": 66.7,
        "total_plans": 23,
        "approved_plans": 18,
        "compliance_rate": 78.3,
        "avg_adherence_score": 85.4
    },
    "project_metrics": [
        {
            "project_id": "proj_123",
            "project_name": "API Authentication System",
            "plan_count": 3,
            "approved_plans": 2,
            "adherence_score": 92.5,
            "drift_warnings": 1,
            "last_drift_check": "2025-07-31T12:00:00Z",
            "status_breakdown": {
                "DRAFT": 1,
                "APPROVED": 2,
                "LOCKED": 0,
                "SUPERSEDED": 0
            }
        }
    ],
    "recent_activity": [
        {
            "type": "drift_detected",
            "project_id": "proj_123",
            "plan_id": "plan_abc",
            "timestamp": "2025-07-31T11:30:00Z",
            "details": "Code changes deviate from approved authentication method"
        }
    ],
    "drift_analysis": {
        "total_drift_events": 5,
        "projects_with_drift": 3,
        "avg_drift_severity": 2.3,
        "recent_drift_events": []
    }
}
```

### Enhanced Existing Endpoint: /sacred/plans
**Enhancement**: Add optional `include_metrics=true` parameter to existing endpoint

## Implementation Architecture

### Folder Structure
```
/Users/sumitm1/contextkeeper-pro-v3/contextkeeper/
├── rag_agent.py                     # Add new /analytics/sacred endpoint
├── sacred_layer_implementation.py   # Add metrics calculation methods
├── enhanced_drift_sacred.py         # Add aggregated drift metrics
├── analytics/                       # New directory
│   ├── __init__.py
│   ├── sacred_metrics.py           # Core metrics calculation logic
│   └── analytics_service.py        # Service layer for analytics
└── tests/
    └── analytics/
        ├── test_sacred_metrics.py
        └── test_analytics_endpoints.py
```

### Core Implementation Classes

#### 1. SacredMetricsCalculator (New)
```python
# analytics/sacred_metrics.py
class SacredMetricsCalculator:
    def __init__(self, sacred_manager: SacredLayerManager, 
                 drift_detector: SacredDriftDetector,
                 project_manager):
        self.sacred_manager = sacred_manager
        self.drift_detector = drift_detector
        self.project_manager = project_manager
    
    async def calculate_overall_metrics(self) -> Dict[str, Any]:
        """Calculate system-wide sacred plan metrics"""
        
    async def calculate_project_metrics(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Calculate per-project sacred plan metrics"""
        
    async def calculate_adherence_score(self, project_id: str) -> float:
        """Calculate adherence score based on drift analysis and plan compliance"""
        
    async def get_recent_activity(self, timeframe: str = "7d") -> List[Dict[str, Any]]:
        """Get recent sacred plan activity"""
```

#### 2. Analytics Service Layer
```python
# analytics/analytics_service.py
class AnalyticsService:
    def __init__(self, metrics_calculator: SacredMetricsCalculator):
        self.calculator = metrics_calculator
    
    async def get_sacred_analytics(self, timeframe: str = "7d", 
                                 project_filter: Optional[str] = None) -> Dict[str, Any]:
        """Main method for /analytics/sacred endpoint"""
```

### Integration Points

#### 1. Flask Endpoint Integration (rag_agent.py)
```python
# Add to _setup_routes method in RAGAgent class
@self.app.route('/analytics/sacred', methods=['GET'])
async def sacred_analytics():
    try:
        timeframe = request.args.get('timeframe', '7d')
        project_filter = request.args.get('project_filter')
        
        analytics_service = AnalyticsService(
            SacredMetricsCalculator(
                self.agent.sacred_manager,
                self.drift_detector,
                self.agent.project_manager
            )
        )
        
        result = await analytics_service.get_sacred_analytics(
            timeframe=timeframe,
            project_filter=project_filter
        )
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in sacred analytics endpoint: {str(e)}", exc_info=True)
        return jsonify({'error': f'Failed to calculate sacred analytics: {str(e)}'}), 500
```

#### 2. Sacred Layer Manager Enhancement
```python
# Add to SacredLayerManager class
def get_plans_statistics(self) -> Dict[str, Any]:
    """Get comprehensive plan statistics"""
    stats = {
        'total_plans': len(self.plans_registry),
        'by_status': {},
        'by_project': {}
    }
    
    for plan_data in self.plans_registry.values():
        status = plan_data['status'].value
        project_id = plan_data['plan'].project_id
        
        stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
        stats['by_project'][project_id] = stats['by_project'].get(project_id, 0) + 1
    
    return stats

def get_project_plan_summary(self, project_id: str) -> Dict[str, Any]:
    """Get plan summary for specific project"""
    project_plans = [
        plan_data for plan_data in self.plans_registry.values()
        if plan_data['plan'].project_id == project_id
    ]
    
    return {
        'total_plans': len(project_plans),
        'approved_plans': len([p for p in project_plans if p['status'] == PlanStatus.APPROVED]),
        'draft_plans': len([p for p in project_plans if p['status'] == PlanStatus.DRAFT]),
        'locked_plans': len([p for p in project_plans if p['status'] == PlanStatus.LOCKED]),
        'superseded_plans': len([p for p in project_plans if p['status'] == PlanStatus.SUPERSEDED])
    }
```

#### 3. Drift Detection Enhancement
```python
# Add to SacredDriftDetector class
async def get_drift_summary(self, project_id: Optional[str] = None, 
                          timeframe: str = "7d") -> Dict[str, Any]:
    """Get drift summary for analytics"""
    # Implementation to aggregate drift events
    
def calculate_adherence_score(self, project_id: str, 
                            drift_analysis: SacredDriftAnalysis) -> float:
    """Calculate adherence score (0-100) based on drift analysis"""
    # Scoring algorithm:
    # - Start with 100
    # - Deduct points for drift severity
    # - Consider frequency of drift events
    # - Weight by plan importance
```

## Security & Scaling Considerations

### Security
- **Authentication**: Endpoint should require same authentication as other sacred endpoints
- **Authorisation**: Read-only access, no sensitive plan content exposed
- **Rate Limiting**: Implement caching due to potentially expensive calculations
- **Data Sanitisation**: Ensure no sensitive verification codes in responses

### Performance & Scaling
- **Caching Strategy**: Cache metrics for 5-10 minutes to avoid expensive recalculations
- **Async Operations**: All database queries should be async
- **Pagination**: For large project lists, implement pagination
- **Background Processing**: Consider background calculation of metrics for large datasets

### Caching Implementation
```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedAnalyticsService:
    def __init__(self):
        self.cache_timeout = timedelta(minutes=5)
        self.last_calculated = {}
        self.cached_results = {}
    
    async def get_cached_sacred_analytics(self, cache_key: str) -> Optional[Dict]:
        """Get cached analytics if still valid"""
        if (cache_key in self.cached_results and 
            cache_key in self.last_calculated and
            datetime.now() - self.last_calculated[cache_key] < self.cache_timeout):
            return self.cached_results[cache_key]
        return None
```

## Testing Strategy

### Unit Tests
- Test metrics calculations with mock data
- Test adherence score algorithms
- Test caching behaviour
- Test error handling

### Integration Tests
- Test endpoint with real sacred plans
- Test cross-service integration (sacred + drift + git)
- Test performance with large datasets

### API Tests
```python
def test_sacred_analytics_endpoint():
    """Test /analytics/sacred endpoint"""
    response = client.get('/analytics/sacred?timeframe=7d')
    assert response.status_code == 200
    data = response.get_json()
    assert 'overall_metrics' in data
    assert 'project_metrics' in data
    assert 'drift_analysis' in data
```

## Implementation Timeline

### Phase 1: Core Metrics (2-3 hours)
1. Create analytics directory structure
2. Implement SacredMetricsCalculator
3. Add basic statistics methods to SacredLayerManager
4. Create unit tests

### Phase 2: API Integration (1-2 hours)
1. Add Flask endpoint to rag_agent.py
2. Implement AnalyticsService
3. Add error handling and logging
4. Test endpoint functionality

### Phase 3: Drift Integration (1-2 hours)
1. Enhance SacredDriftDetector with summary methods
2. Implement adherence scoring algorithm
3. Add drift metrics to analytics response
4. Integration testing

### Phase 4: Performance & Polish (1 hour)
1. Add caching layer
2. Performance testing
3. Documentation updates
4. Final integration tests

**Total Estimated Time**: 5-8 hours

## API Reference URLs
- Flask Documentation: https://flask.palletsprojects.com/en/2.3.x/
- ChromaDB Documentation: https://docs.trychroma.com/
- Python AsyncIO: https://docs.python.org/3/library/asyncio.html

This architecture provides a comprehensive sacred metrics system that integrates seamlessly with the existing ContextKeeper v3 sacred layer implementation while maintaining performance and Australian English spelling conventions.