#!/usr/bin/env python3
"""
Analytics Integration for ContextKeeper RAG Agent
Adds sacred metrics endpoints to the Flask application
"""

import logging
from flask import request, jsonify
from analytics import SacredMetricsCalculator, AnalyticsService
from enhanced_drift_sacred import SacredDriftDetector

logger = logging.getLogger(__name__)

def add_analytics_endpoints(app, agent):
    """
    Add analytics endpoints to the Flask application
    
    Args:
        app: Flask application instance
        agent: RAG agent instance with sacred integration
    """
    
    @app.route('/analytics/sacred', methods=['GET'])
    def sacred_analytics():
        """Get comprehensive sacred plan analytics"""
        try:
            timeframe = request.args.get('timeframe', '7d')
            project_filter = request.args.get('project_filter')
            include_history = request.args.get('include_history', 'false').lower() == 'true'
            
            # Initialize analytics service
            drift_detector = SacredDriftDetector(
                agent,
                agent.sacred_integration.sacred_manager
            )
            
            metrics_calculator = SacredMetricsCalculator(
                agent.sacred_integration.sacred_manager,
                drift_detector,
                agent.project_manager
            )
            
            analytics_service = AnalyticsService(metrics_calculator)
            
            # Run async analytics calculation
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    analytics_service.get_sacred_analytics(
                        timeframe=timeframe,
                        project_filter=project_filter,
                        include_history=include_history
                    )
                )
            finally:
                loop.close()
            
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error in sacred analytics endpoint: {str(e)}", exc_info=True)
            return jsonify({'error': f'Failed to calculate sacred analytics: {str(e)}'}), 500

    @app.route('/analytics/sacred/health', methods=['GET'])
    def sacred_analytics_health():
        """Health check for sacred analytics system"""
        try:
            drift_detector = SacredDriftDetector(
                agent,
                agent.sacred_integration.sacred_manager
            )
            
            metrics_calculator = SacredMetricsCalculator(
                agent.sacred_integration.sacred_manager,
                drift_detector,
                agent.project_manager
            )
            
            analytics_service = AnalyticsService(metrics_calculator)
            
            # Run async health check
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    analytics_service.get_sacred_health_check()
                )
            finally:
                loop.close()
                
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error in sacred analytics health check: {str(e)}", exc_info=True)
            return jsonify({'error': f'Failed to check analytics health: {str(e)}'}), 500

    @app.route('/analytics/sacred/project/<project_id>', methods=['GET'])
    def project_sacred_analytics(project_id):
        """Get detailed sacred analytics for a specific project"""
        try:
            timeframe = request.args.get('timeframe', '7d')
            
            drift_detector = SacredDriftDetector(
                agent,
                agent.sacred_integration.sacred_manager
            )
            
            metrics_calculator = SacredMetricsCalculator(
                agent.sacred_integration.sacred_manager,
                drift_detector,
                agent.project_manager
            )
            
            analytics_service = AnalyticsService(metrics_calculator)
            
            # Run async project analytics
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    analytics_service.get_project_detailed_analytics(
                        project_id=project_id,
                        timeframe=timeframe
                    )
                )
            finally:
                loop.close()
            
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error in project sacred analytics: {str(e)}", exc_info=True)
            return jsonify({'error': f'Failed to get project analytics: {str(e)}'}), 500

    @app.route('/analytics/sacred/clear-cache', methods=['POST'])
    def clear_analytics_cache():
        """Clear analytics cache - useful for development and testing"""
        try:
            drift_detector = SacredDriftDetector(
                agent,
                agent.sacred_integration.sacred_manager
            )
            
            metrics_calculator = SacredMetricsCalculator(
                agent.sacred_integration.sacred_manager,
                drift_detector,
                agent.project_manager
            )
            
            analytics_service = AnalyticsService(metrics_calculator)
            analytics_service.clear_cache()
            
            return jsonify({
                'status': 'success',
                'message': 'Analytics cache cleared successfully'
            })
        except Exception as e:
            logger.error(f"Error clearing analytics cache: {str(e)}", exc_info=True)
            return jsonify({'error': f'Failed to clear cache: {str(e)}'}), 500

    logger.info("Sacred analytics endpoints added successfully")
    
def integrate_analytics_with_rag_agent():
    """
    Helper function to automatically integrate analytics with rag_agent.py
    This can be called from rag_agent.py to add the endpoints
    """
    def decorator(rag_agent_class):
        original_setup_routes = rag_agent_class._setup_routes
        
        def enhanced_setup_routes(self):
            # Call original setup_routes
            original_setup_routes(self)
            
            # Add analytics endpoints
            add_analytics_endpoints(self.app, self.agent)
            
            logger.info("Analytics endpoints integrated with RAG agent")
        
        rag_agent_class._setup_routes = enhanced_setup_routes
        return rag_agent_class
    
    return decorator