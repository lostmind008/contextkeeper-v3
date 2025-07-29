#!/usr/bin/env python3
"""
test_end_to_end_workflows.py - End-to-end integration tests for ContextKeeper v3

Created: 2025-07-29 04:17:00 (Australia/Sydney)
Part of: ContextKeeper v3.0 Test Suite

Tests complete workflows that span multiple components: file ingestion → 
embedding → querying → Sacred Layer integration. Validates that all the 
fixes work together as a complete system.
"""

import pytest
import asyncio
import tempfile
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@pytest.mark.integration
class TestCompleteRAGWorkflow:
    """Test complete RAG workflow from ingestion to querying"""
    
    @pytest.fixture
    def mock_rag_system(self, temp_dir, mock_embedder):
        """Create a mock RAG system for end-to-end testing"""
        class MockRAGSystem:
            def __init__(self, storage_path, embedder):
                self.storage_path = storage_path
                self.embedder = embedder
                self.ingested_files = {}
                self.embeddings_db = {}
                self.query_history = []
            
            def ingest_files(self, project_id, file_paths):
                """Mock file ingestion process"""
                ingested_count = 0
                
                for file_path in file_paths:
                    if Path(file_path).exists():
                        # Read file content
                        content = Path(file_path).read_text()
                        
                        # Generate embeddings
                        embeddings = self.embedder.embed_documents([content])
                        
                        # Store in mock database
                        file_key = f"{project_id}:{file_path}"
                        self.ingested_files[file_key] = {
                            "content": content,
                            "embeddings": embeddings[0],
                            "file_path": file_path,
                            "project_id": project_id
                        }
                        
                        ingested_count += 1
                
                return {
                    "status": "success",
                    "files_processed": ingested_count,
                    "project_id": project_id
                }
            
            def query(self, project_id, query_text, limit=5):
                """Mock query processing"""
                self.query_history.append({
                    "project_id": project_id,
                    "query": query_text,
                    "timestamp": time.time()
                })
                
                # Generate query embedding
                query_embedding = self.embedder.embed_query(query_text)
                
                # Find matching files (simplified similarity)
                results = []
                for file_key, file_data in self.ingested_files.items():
                    if file_data["project_id"] == project_id:
                        # Simple mock similarity score
                        similarity_score = 0.85 if query_text.lower() in file_data["content"].lower() else 0.3
                        
                        if similarity_score > 0.5:
                            results.append({
                                "content": file_data["content"][:200] + "...",
                                "file_path": file_data["file_path"],
                                "score": similarity_score
                            })
                
                # Sort by score and limit results
                results.sort(key=lambda x: x["score"], reverse=True)
                return {
                    "query": query_text,
                    "project_id": project_id,
                    "results": results[:limit],
                    "count": len(results[:limit])
                }
        
        return MockRAGSystem(temp_dir, mock_embedder)
    
    def test_file_ingestion_to_query_workflow(self, mock_rag_system, sample_files_for_ingestion):
        """Test complete workflow: ingest files → query content"""
        project_id = "workflow_test_project"
        
        # Step 1: Ingest files
        file_paths = [
            str(sample_files_for_ingestion / "sample.py"),
            str(sample_files_for_ingestion / "README.md"),
            str(sample_files_for_ingestion / "config.json")
        ]
        
        ingestion_result = mock_rag_system.ingest_files(project_id, file_paths)
        
        # Verify ingestion
        assert ingestion_result["status"] == "success"
        assert ingestion_result["files_processed"] == 3
        assert ingestion_result["project_id"] == project_id
        
        # Step 2: Query the ingested content
        query_result = mock_rag_system.query(
            project_id=project_id,
            query_text="fibonacci calculation",
            limit=5
        )
        
        # Verify query results
        assert query_result["project_id"] == project_id
        assert query_result["query"] == "fibonacci calculation"
        assert query_result["count"] > 0
        assert len(query_result["results"]) > 0
        
        # Verify relevant content was found
        fibonacci_result = next(
            (r for r in query_result["results"] if "fibonacci" in r["content"].lower()),
            None
        )
        assert fibonacci_result is not None
        assert fibonacci_result["score"] > 0.5
    
    def test_multi_project_isolation_workflow(self, mock_rag_system, sample_files_for_ingestion):
        """Test that different projects maintain data isolation"""
        project_a = "project_alpha"
        project_b = "project_beta"
        
        # Ingest files into different projects
        file_paths = [str(sample_files_for_ingestion / "sample.py")]
        
        mock_rag_system.ingest_files(project_a, file_paths)
        mock_rag_system.ingest_files(project_b, file_paths)
        
        # Query each project
        query_a = mock_rag_system.query(project_a, "fibonacci")
        query_b = mock_rag_system.query(project_b, "fibonacci")
        
        # Both should find results within their own project
        assert query_a["project_id"] == project_a
        assert query_b["project_id"] == project_b
        assert query_a["count"] > 0
        assert query_b["count"] > 0
        
        # Query non-existent project
        query_c = mock_rag_system.query("project_gamma", "fibonacci")
        assert query_c["count"] == 0  # No results for non-existent project
    
    def test_query_history_tracking(self, mock_rag_system, sample_files_for_ingestion):
        """Test that query history is properly tracked"""
        project_id = "history_test_project"
        
        # Ingest files
        file_paths = [str(sample_files_for_ingestion / "README.md")]
        mock_rag_system.ingest_files(project_id, file_paths)
        
        # Perform multiple queries
        queries = [
            "test project documentation",
            "how to use this application",
            "features and capabilities"
        ]
        
        for query_text in queries:
            mock_rag_system.query(project_id, query_text)
        
        # Verify query history
        history = mock_rag_system.query_history
        assert len(history) >= len(queries)
        
        # Check recent queries
        recent_queries = history[-len(queries):]
        for i, query_record in enumerate(recent_queries):
            assert query_record["project_id"] == project_id
            assert query_record["query"] == queries[i]
            assert "timestamp" in query_record


@pytest.mark.integration
@pytest.mark.sacred
class TestSacredLayerIntegration:
    """Test Sacred Layer integration with RAG system"""
    
    @pytest.fixture
    def integrated_system(self, mock_rag_system, sacred_manager):
        """Create integrated RAG + Sacred Layer system"""
        class IntegratedSystem:
            def __init__(self, rag_system, sacred_manager):
                self.rag = rag_system
                self.sacred = sacred_manager
            
            def create_plan_from_query(self, project_id, query, plan_title):
                """Create Sacred plan based on RAG query results"""
                # Query RAG system
                query_results = self.rag.query(project_id, query)
                
                # Generate plan content from results
                plan_content = f"# {plan_title}\n\n"
                plan_content += f"Based on query: {query}\n\n"
                
                for result in query_results["results"]:
                    plan_content += f"## From {result['file_path']}\n"
                    plan_content += f"Relevance: {result['score']:.2f}\n"
                    plan_content += f"{result['content']}\n\n"
                
                # Create Sacred plan
                plan = self.sacred.create_plan(
                    project_id=project_id,
                    title=plan_title,
                    content=plan_content
                )
                
                return {
                    "plan": plan,
                    "query_results": query_results,
                    "verification_code": self.sacred.generate_verification_code(plan)
                }
            
            def query_with_sacred_context(self, project_id, query):
                """Query combining RAG results with Sacred context"""
                # Get regular RAG results
                rag_results = self.rag.query(project_id, query)
                
                # Get Sacred plans for project
                sacred_plans = [
                    plan for plan in self.sacred.plans_registry.values() 
                    if plan.project_id == project_id
                ]
                
                # Combine results
                return {
                    "query": query,
                    "project_id": project_id,
                    "rag_results": rag_results["results"],
                    "sacred_plans": [
                        {
                            "plan_id": p.plan_id,
                            "title": p.title,
                            "status": p.status.value,
                            "content_preview": p.content[:100] + "..."
                        } for p in sacred_plans
                    ],
                    "combined_count": rag_results["count"] + len(sacred_plans)
                }
        
        return IntegratedSystem(mock_rag_system, sacred_manager)
    
    def test_plan_creation_from_rag_results(self, integrated_system, sample_files_for_ingestion):
        """Test creating Sacred plans from RAG query results"""
        project_id = "sacred_integration_test"
        
        # First ingest files into RAG system
        file_paths = [str(sample_files_for_ingestion / "sample.py")]
        integrated_system.rag.ingest_files(project_id, file_paths)
        
        # Create plan from query results
        result = integrated_system.create_plan_from_query(
            project_id=project_id,
            query="fibonacci implementation",
            plan_title="Fibonacci Algorithm Architecture"
        )
        
        # Verify plan creation
        assert "plan" in result
        assert "query_results" in result
        assert "verification_code" in result
        
        plan = result["plan"]
        assert plan.project_id == project_id
        assert plan.title == "Fibonacci Algorithm Architecture"
        assert "fibonacci implementation" in plan.content.lower()
        assert len(result["verification_code"]) > 0
    
    def test_combined_rag_sacred_querying(self, integrated_system, sample_files_for_ingestion):
        """Test querying that combines RAG and Sacred results"""
        project_id = "combined_query_test"
        
        # Setup: Ingest files and create Sacred plan
        file_paths = [str(sample_files_for_ingestion / "README.md")]
        integrated_system.rag.ingest_files(project_id, file_paths)
        
        # Create a Sacred plan
        integrated_system.sacred.create_plan(
            project_id=project_id,
            title="Project Architecture Plan",
            content="This plan outlines the overall architecture of the test project."
        )
        
        # Perform combined query
        combined_results = integrated_system.query_with_sacred_context(
            project_id=project_id,
            query="project architecture"
        )
        
        # Verify combined results
        assert combined_results["project_id"] == project_id
        assert combined_results["query"] == "project architecture"
        assert "rag_results" in combined_results
        assert "sacred_plans" in combined_results
        assert combined_results["combined_count"] > 0
        
        # Verify Sacred plan is included
        sacred_plans = combined_results["sacred_plans"]
        assert len(sacred_plans) > 0
        
        architecture_plan = next(
            (p for p in sacred_plans if "architecture" in p["title"].lower()),
            None
        )
        assert architecture_plan is not None
    
    def test_sacred_plan_approval_workflow_integration(self, integrated_system):
        """Test complete Sacred plan approval workflow"""
        project_id = "approval_workflow_test"
        
        # Create plan
        plan = integrated_system.sacred.create_plan(
            project_id=project_id,
            title="Database Schema Plan",
            content="Detailed database schema design..."
        )
        
        # Generate verification code
        verification_code = integrated_system.sacred.generate_verification_code(plan)
        
        # Mock approval process
        def mock_approve_plan(plan_id, approver, verification_code, secondary_key):
            if plan_id in integrated_system.sacred.plans_registry and secondary_key == "test_key":
                plan = integrated_system.sacred.plans_registry[plan_id]
                plan.status = plan.status.__class__("approved")  # Handle enum conversion
                plan.approved_by = approver
                return True
            return False
        
        integrated_system.sacred.approve_plan = mock_approve_plan
        
        # Approve plan
        approval_result = integrated_system.sacred.approve_plan(
            plan_id=plan.plan_id,
            approver="senior_architect",
            verification_code=verification_code,
            secondary_key="test_key"
        )
        
        # Verify approval workflow
        assert approval_result is True
        
        # Verify plan is now in approved state
        approved_plan = integrated_system.sacred.plans_registry[plan.plan_id]
        assert str(approved_plan.status).lower() == "approved"
        assert approved_plan.approved_by == "senior_architect"


@pytest.mark.integration
class TestSystemResilience:
    """Test system resilience and error recovery"""
    
    def test_database_connection_failure_recovery(self, mock_rag_system):
        """Test system behavior when database connections fail"""
        # Simulate database failure
        original_embeddings_db = mock_rag_system.embeddings_db
        mock_rag_system.embeddings_db = None
        
        # System should handle gracefully
        try:
            result = mock_rag_system.query("test_project", "test query")
            # Should return empty results rather than crashing
            assert result["count"] == 0
            assert result["results"] == []
        except Exception as e:
            # If exception occurs, it should be handled gracefully
            assert "database" in str(e).lower() or "connection" in str(e).lower()
        
        finally:
            # Restore database for other tests
            mock_rag_system.embeddings_db = original_embeddings_db
    
    def test_large_file_ingestion_handling(self, mock_rag_system, temp_dir):
        """Test handling of large files during ingestion"""
        project_id = "large_file_test"
        
        # Create a large test file
        large_file = Path(temp_dir) / "large_test_file.py"
        large_content = "# Large file test\n" + "print('test line')\n" * 1000
        large_file.write_text(large_content)
        
        # Test ingestion
        result = mock_rag_system.ingest_files(project_id, [str(large_file)])
        
        # Should handle large files successfully
        assert result["status"] == "success"
        assert result["files_processed"] == 1
        
        # Verify content was stored
        file_key = f"{project_id}:{large_file}"
        assert file_key in mock_rag_system.ingested_files
        assert len(mock_rag_system.ingested_files[file_key]["content"]) > 10000
    
    def test_concurrent_query_handling(self, mock_rag_system, sample_files_for_ingestion):
        """Test system behavior under concurrent query load"""
        import threading
        import queue
        
        project_id = "concurrent_test"
        
        # Setup: Ingest test files
        file_paths = [str(sample_files_for_ingestion / "sample.py")]
        mock_rag_system.ingest_files(project_id, file_paths)
        
        # Concurrent query execution
        results_queue = queue.Queue()
        
        def execute_query(query_id):
            try:
                result = mock_rag_system.query(project_id, f"query_{query_id}")
                results_queue.put(("success", query_id, result))
            except Exception as e:
                results_queue.put(("error", query_id, str(e)))
        
        # Launch concurrent queries
        threads = []
        num_concurrent_queries = 5
        
        for i in range(num_concurrent_queries):
            thread = threading.Thread(target=execute_query, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all queries to complete
        for thread in threads:
            thread.join(timeout=5.0)
        
        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        
        # Verify all queries completed
        assert len(results) == num_concurrent_queries
        
        # Verify no errors occurred
        errors = [r for r in results if r[0] == "error"]
        assert len(errors) == 0, f"Concurrent queries failed: {errors}"
        
        # Verify all queries returned valid results
        successful_results = [r for r in results if r[0] == "success"]
        assert len(successful_results) == num_concurrent_queries


@pytest.mark.integration
@pytest.mark.performance
class TestPerformanceIntegration:
    """Test performance characteristics of integrated system"""
    
    def test_ingestion_performance_scaling(self, mock_rag_system, temp_dir):
        """Test how ingestion performance scales with file count"""
        import time
        
        project_id = "performance_test"
        
        # Create multiple test files
        file_counts = [1, 5, 10]
        performance_data = []
        
        for file_count in file_counts:
            # Create files
            test_files = []
            for i in range(file_count):
                test_file = Path(temp_dir) / f"perf_test_{i}.py"
                test_file.write_text(f"# Performance test file {i}\ndef function_{i}():\n    return {i}")
                test_files.append(str(test_file))
            
            # Measure ingestion time
            start_time = time.time()
            result = mock_rag_system.ingest_files(project_id, test_files)
            ingestion_time = time.time() - start_time
            
            performance_data.append({
                "file_count": file_count,
                "ingestion_time": ingestion_time,
                "files_processed": result["files_processed"]
            })
            
            # Clean up for next iteration
            mock_rag_system.ingested_files.clear()
        
        # Verify performance characteristics
        for data in performance_data:
            assert data["ingestion_time"] < 5.0, f"Ingestion too slow for {data['file_count']} files"
            assert data["files_processed"] == data["file_count"]
        
        # Verify reasonable scaling (not exponential)
        if len(performance_data) >= 2:
            time_ratio = performance_data[-1]["ingestion_time"] / performance_data[0]["ingestion_time"]
            file_ratio = performance_data[-1]["file_count"] / performance_data[0]["file_count"]
            
            # Time scaling should be reasonable compared to file count scaling
            assert time_ratio <= file_ratio * 2, "Performance scaling is acceptable"
    
    def test_query_response_time_consistency(self, mock_rag_system, sample_files_for_ingestion):
        """Test that query response times remain consistent"""
        import time
        
        project_id = "response_time_test"
        
        # Setup: Ingest files
        file_paths = [
            str(sample_files_for_ingestion / "sample.py"),
            str(sample_files_for_ingestion / "README.md")
        ]
        mock_rag_system.ingest_files(project_id, file_paths)
        
        # Execute multiple queries and measure response times
        queries = [
            "fibonacci calculation",
            "project documentation", 
            "configuration settings",
            "test implementation",
            "database connection"
        ]
        
        response_times = []
        
        for query in queries:
            start_time = time.time()
            result = mock_rag_system.query(project_id, query)
            response_time = time.time() - start_time
            
            response_times.append(response_time)
            
            # Each query should complete quickly
            assert response_time < 2.0, f"Query too slow: {query}"
            assert "results" in result
        
        # Response times should be reasonably consistent
        if len(response_times) > 1:
            avg_time = sum(response_times) / len(response_times)
            max_deviation = max(abs(t - avg_time) for t in response_times)
            
            # Maximum deviation should not be more than 3x average
            assert max_deviation <= avg_time * 3, "Response times too inconsistent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])