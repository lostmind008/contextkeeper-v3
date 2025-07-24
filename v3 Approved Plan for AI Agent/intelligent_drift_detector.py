#!/usr/bin/env python3
"""
Intelligent Drift Detection for ContextKeeper
Uses NLP and pattern analysis to detect when development drifts from objectives
"""

import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import logging
from dataclasses import dataclass
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

@dataclass
class DriftAnalysis:
    """Results of drift detection analysis"""
    alignment_score: float  # 0-1 score
    status: str  # aligned, minor_drift, major_drift
    aligned_activities: List[Dict[str, Any]]
    misaligned_activities: List[Dict[str, Any]]
    recommendations: List[str]
    objective_progress: Dict[str, float]  # objective -> progress estimate
    time_distribution: Dict[str, float]  # objective -> time spent percentage

class IntelligentDriftDetector:
    """Advanced drift detection using NLP and pattern analysis"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Keywords that indicate different types of work
        self.work_patterns = {
            'implementation': ['implement', 'create', 'build', 'develop', 'add', 'feature'],
            'bugfix': ['fix', 'bug', 'error', 'issue', 'problem', 'resolve'],
            'refactor': ['refactor', 'clean', 'optimize', 'improve', 'restructure'],
            'documentation': ['document', 'readme', 'docs', 'comment', 'explain'],
            'testing': ['test', 'unit', 'integration', 'coverage', 'spec'],
            'configuration': ['config', 'setup', 'environment', 'deploy', 'settings']
        }
    
    def analyze_drift(self, objectives: List[Dict[str, Any]], 
                     activities: List[Dict[str, Any]],
                     decisions: List[Dict[str, Any]] = None) -> DriftAnalysis:
        """Analyze alignment between objectives and recent activities"""
        
        if not objectives or not activities:
            return DriftAnalysis(
                alignment_score=0.0,
                status="no_data",
                aligned_activities=[],
                misaligned_activities=activities,
                recommendations=["No objectives or activities to analyze"],
                objective_progress={},
                time_distribution={}
            )
        
        # Prepare text data
        objective_texts = [
            f"{obj.get('title', '')} {obj.get('description', '')}"
            for obj in objectives
        ]
        
        activity_texts = []
        for activity in activities:
            # Handle different activity types
            if 'message' in activity:  # Git commit
                text = activity['message']
            elif 'content' in activity:  # File content
                text = activity['content'][:200]  # Use snippet
            elif 'decision' in activity:  # Decision
                text = f"{activity['decision']} {activity.get('reasoning', '')}"
            else:
                text = str(activity)
            activity_texts.append(text)
        
        # Calculate similarity matrix
        all_texts = objective_texts + activity_texts
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            
            # Split back into objectives and activities
            obj_vectors = tfidf_matrix[:len(objectives)]
            act_vectors = tfidf_matrix[len(objectives):]
            
            # Calculate similarities
            similarities = cosine_similarity(act_vectors, obj_vectors)
            
        except Exception as e:
            logger.warning(f"Failed to vectorize texts: {e}")
            # Fallback to simple keyword matching
            similarities = self._keyword_similarity(activity_texts, objective_texts)
        
        # Analyze results
        aligned_activities = []
        misaligned_activities = []
        objective_activities = defaultdict(list)
        
        for i, activity in enumerate(activities):
            max_similarity = np.max(similarities[i])
            best_objective_idx = np.argmax(similarities[i])
            
            if max_similarity > 0.3:  # Threshold for alignment
                activity['alignment_score'] = float(max_similarity)
                activity['aligned_objective'] = objectives[best_objective_idx].get('title', 'Unknown')
                aligned_activities.append(activity)
                objective_activities[best_objective_idx].append(activity)
            else:
                activity['alignment_score'] = float(max_similarity)
                misaligned_activities.append(activity)
        
        # Calculate overall alignment
        alignment_score = len(aligned_activities) / len(activities) if activities else 0
        
        # Determine status
        if alignment_score >= 0.7:
            status = "aligned"
        elif alignment_score >= 0.4:
            status = "minor_drift"
        else:
            status = "major_drift"
        
        # Calculate objective progress
        objective_progress = {}
        time_distribution = {}
        total_activities = len(activities)
        
        for i, obj in enumerate(objectives):
            obj_title = obj.get('title', f'Objective {i}')
            obj_activities = objective_activities[i]
            
            # Estimate progress based on activity
            progress = self._estimate_progress(obj, obj_activities)
            objective_progress[obj_title] = progress
            
            # Calculate time distribution
            time_percentage = len(obj_activities) / total_activities if total_activities > 0 else 0
            time_distribution[obj_title] = time_percentage
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            alignment_score, status, misaligned_activities, 
            objective_progress, decisions
        )
        
        return DriftAnalysis(
            alignment_score=alignment_score,
            status=status,
            aligned_activities=aligned_activities,
            misaligned_activities=misaligned_activities,
            recommendations=recommendations,
            objective_progress=objective_progress,
            time_distribution=time_distribution
        )
    
    def _keyword_similarity(self, activity_texts: List[str], 
                          objective_texts: List[str]) -> np.ndarray:
        """Fallback keyword-based similarity calculation"""
        similarities = []
        
        for act_text in activity_texts:
            act_words = set(act_text.lower().split())
            row = []
            
            for obj_text in objective_texts:
                obj_words = set(obj_text.lower().split())
                
                # Calculate Jaccard similarity
                intersection = len(act_words & obj_words)
                union = len(act_words | obj_words)
                similarity = intersection / union if union > 0 else 0
                row.append(similarity)
            
            similarities.append(row)
        
        return np.array(similarities)
    
    def _estimate_progress(self, objective: Dict[str, Any], 
                          activities: List[Dict[str, Any]]) -> float:
        """Estimate progress on an objective based on activities"""
        if not activities:
            return 0.0
        
        # Look for progress indicators in activities
        progress_indicators = {
            'started': 0.1,
            'wip': 0.3,
            'in progress': 0.3,
            'partial': 0.5,
            'mostly': 0.7,
            'complete': 0.9,
            'done': 1.0,
            'finished': 1.0
        }
        
        max_progress = 0.0
        
        for activity in activities:
            text = str(activity).lower()
            
            # Check for explicit progress indicators
            for indicator, progress in progress_indicators.items():
                if indicator in text:
                    max_progress = max(max_progress, progress)
            
            # Check for implementation keywords
            if any(word in text for word in self.work_patterns['implementation']):
                max_progress = max(max_progress, 0.5)
            
            # Check for testing keywords (indicates near completion)
            if any(word in text for word in self.work_patterns['testing']):
                max_progress = max(max_progress, 0.8)
        
        # Also consider number of activities
        activity_factor = min(len(activities) / 10, 1.0)  # Assume 10 activities = good progress
        
        return min(max(max_progress, activity_factor * 0.5), 1.0)
    
    def _generate_recommendations(self, alignment_score: float, status: str,
                                misaligned_activities: List[Dict[str, Any]],
                                objective_progress: Dict[str, float],
                                decisions: List[Dict[str, Any]] = None) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Status-based recommendations
        if status == "major_drift":
            recommendations.append(
                "⚠️ Major drift detected. Consider reviewing and updating objectives "
                "or refocusing development efforts."
            )
        elif status == "minor_drift":
            recommendations.append(
                "📊 Minor drift detected. Some activities don't align with objectives."
            )
        
        # Analyze misaligned activities
        if misaligned_activities:
            activity_types = defaultdict(int)
            for activity in misaligned_activities:
                activity_type = self._classify_activity(activity)
                activity_types[activity_type] += 1
            
            # Most common misaligned activity type
            if activity_types:
                most_common = max(activity_types.items(), key=lambda x: x[1])
                recommendations.append(
                    f"💡 Most misaligned activities are '{most_common[0]}' "
                    f"({most_common[1]} activities). Consider if this should be a new objective."
                )
        
        # Progress-based recommendations
        low_progress_objectives = [
            obj for obj, progress in objective_progress.items() 
            if progress < 0.3
        ]
        
        if low_progress_objectives:
            recommendations.append(
                f"🎯 Low progress on objectives: {', '.join(low_progress_objectives[:3])}. "
                "Consider prioritizing these."
            )
        
        # Time distribution recommendations
        neglected_objectives = [
            obj for obj, time_pct in objective_progress.items()
            if time_pct < 0.1
        ]
        
        if neglected_objectives:
            recommendations.append(
                f"⏰ No recent activity on: {', '.join(neglected_objectives[:3])}. "
                "These objectives may need attention."
            )
        
        # Decision consistency check
        if decisions and alignment_score < 0.5:
            recent_decisions = sorted(decisions, 
                                    key=lambda d: d.get('timestamp', ''), 
                                    reverse=True)[:3]
            
            recommendations.append(
                "📝 Review recent decisions to ensure they still align with objectives. "
                "Consider updating objectives based on architectural changes."
            )
        
        # Positive reinforcement
        if status == "aligned":
            recommendations.append(
                "✅ Great job! Your development activities align well with objectives."
            )
        
        return recommendations
    
    def _classify_activity(self, activity: Dict[str, Any]) -> str:
        """Classify an activity into a work pattern category"""
        text = str(activity).lower()
        
        # Count matches for each pattern
        pattern_scores = {}
        for pattern_name, keywords in self.work_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                pattern_scores[pattern_name] = score
        
        if pattern_scores:
            return max(pattern_scores.items(), key=lambda x: x[1])[0]
        return "other"
    
    def generate_drift_report(self, project_name: str, 
                            analysis: DriftAnalysis,
                            time_period: str = "24 hours") -> str:
        """Generate a human-readable drift report"""
        report = f"""
Drift Analysis Report - {project_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Time Period: Last {time_period}
{'=' * 60}

Overall Alignment: {analysis.alignment_score:.1%}
Status: {analysis.status.replace('_', ' ').title()}

Objective Progress:
"""
        
        for obj, progress in analysis.objective_progress.items():
            bar_length = int(progress * 20)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            report += f"  {obj[:40]:<40} {bar} {progress:.0%}\n"
        
        report += "\nTime Distribution:\n"
        for obj, time_pct in analysis.time_distribution.items():
            report += f"  {obj[:40]:<40} {time_pct:.1%} of activities\n"
        
        if analysis.misaligned_activities:
            report += f"\nMisaligned Activities ({len(analysis.misaligned_activities)}):\n"
            for activity in analysis.misaligned_activities[:5]:
                activity_desc = activity.get('message', activity.get('decision', str(activity)))[:60]
                report += f"  - {activity_desc}... (alignment: {activity.get('alignment_score', 0):.1%})\n"
        
        report += "\nRecommendations:\n"
        for rec in analysis.recommendations:
            report += f"  {rec}\n"
        
        return report

# Integration with the main RAG agent
def add_drift_detection_endpoint(app, agent, project_manager):
    """Add drift detection endpoint to Flask app"""
    detector = IntelligentDriftDetector()
    
    @app.route('/projects/<project_id>/drift', methods=['GET'])
    async def analyze_drift(project_id):
        hours = int(request.args.get('hours', 24))
        
        project = project_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Get objectives
        objectives = [
            {
                'title': obj.title,
                'description': obj.description,
                'priority': obj.priority
            }
            for obj in project.objectives
            if obj.status != 'completed'
        ]
        
        # Get recent activities (queries, file ingestions, etc.)
        # This would need to be implemented in the main agent
        activities = []
        
        # Query recent knowledge base entries
        recent_results = await agent.query(
            "recent changes OR recent commits OR recent activity",
            k=50,
            project_id=project_id
        )
        
        for result in recent_results.get('results', []):
            if result['metadata'].get('type') in ['git_activity', 'decision', 'code']:
                activities.append({
                    'content': result['content'],
                    'type': result['metadata'].get('type'),
                    'timestamp': result['metadata'].get('ingested_at')
                })
        
        # Get decisions
        decisions = [
            {
                'decision': dec.decision,
                'reasoning': dec.reasoning,
                'timestamp': dec.timestamp
            }
            for dec in project.decisions[-10:]  # Last 10 decisions
        ]
        
        # Analyze drift
        analysis = detector.analyze_drift(objectives, activities, decisions)
        
        # Generate report
        report = detector.generate_drift_report(project.name, analysis, f"{hours} hours")
        
        return jsonify({
            'project_id': project_id,
            'project_name': project.name,
            'analysis': {
                'alignment_score': analysis.alignment_score,
                'status': analysis.status,
                'objective_progress': analysis.objective_progress,
                'time_distribution': analysis.time_distribution,
                'recommendations': analysis.recommendations,
                'aligned_count': len(analysis.aligned_activities),
                'misaligned_count': len(analysis.misaligned_activities)
            },
            'report': report
        })