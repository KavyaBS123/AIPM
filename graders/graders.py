"""Grading system for tasks in AI Product Manager Environment."""

from typing import List, Dict, Tuple
from models import Feature, Action


class BaseGrader:
    """Base class for task graders."""
    
    def grade(self, *args, **kwargs) -> Tuple[float, str]:
        """
        Grade the agent's performance.
        
        Returns:
            Tuple of (score 0.0-1.0, explanation)
        """
        raise NotImplementedError


class EasyTaskGrader(BaseGrader):
    """Grader for Easy Task: Identify most critical feature."""
    
    def grade(
        self,
        actions: List[Action],
        features: List[Feature],
        user_feedback_count: Dict[str, int]
    ) -> Tuple[float, str]:
        """
        Grade if agent correctly identifies the most critical feature.
        
        Args:
            actions: List of actions taken by agent
            features: List of features with metadata
            user_feedback_count: Dict mapping feature_id to user request count
        
        Returns:
            Tuple of (score, explanation)
        """
        if not actions:
            return 0.01, "No actions taken"
        
        # Find first prioritize action
        prioritized_features = [
            a.feature_id for a in actions
            if a.action_type.value == "prioritize_feature" and a.feature_id
        ]
        
        if not prioritized_features:
            return 0.01, "No features were prioritized"
        
        first_prioritized_id = prioritized_features[0]
        
        # Calculate criticality based on user feedback and impact
        def calculate_criticality(feature: Feature) -> float:
            """Calculate criticality score (0.01 to 0.99)."""
            user_impact = (feature.user_requests / 1000.0) * 0.3  # 30% weight
            satisfaction_impact = max(0, feature.impact_on_satisfaction) * 0.4  # 40% weight
            churn_reduction = max(0, -feature.impact_on_churn) * 0.3  # 30% weight
            return max(0.01, min(0.99, user_impact + satisfaction_impact + churn_reduction))
        
        feature_criticality = {f.feature_id: calculate_criticality(f) for f in features}
        most_critical_id = max(feature_criticality, key=feature_criticality.get)
        
        # Scoring logic
        if first_prioritized_id == most_critical_id:
            score = 0.99
            explanation = f"Correctly identified {most_critical_id} as most critical feature"
        else:
            # Partial credit based on criticality ranking
            criticality_rank = sorted(
                feature_criticality.values(), reverse=True
            )
            selected_criticality = feature_criticality.get(first_prioritized_id, 0.0)
            rank_position = len([c for c in criticality_rank if c > selected_criticality])
            
            if rank_position == 1:  # Second most critical
                score = 0.6
                explanation = f"Selected {first_prioritized_id} (2nd most critical, should be {most_critical_id})"
            elif rank_position == 2:
                score = 0.3
                explanation = f"Selected {first_prioritized_id} (3rd most critical, should be {most_critical_id})"
            else:
                score = 0.1
                explanation = f"Selected {first_prioritized_id} (poor choice, should be {most_critical_id})"
        
        return score, explanation


class MediumTaskGrader(BaseGrader):
    """Grader for Medium Task: Rank/prioritize multiple features."""
    
    def grade(
        self,
        actions: List[Action],
        features: List[Feature],
        task_constraint: int = 3
    ) -> Tuple[float, str]:
        """
        Grade the ranking of top features.
        
        Args:
            actions: List of actions taken
            features: List of features
            task_constraint: How many features to rank (default 3)
        
        Returns:
            Tuple of (score, explanation)
        """
        # Get prioritized features in order
        prioritized_features = [
            a.feature_id for a in actions
            if a.action_type.value == "prioritize_feature" and a.feature_id
        ]
        
        if len(prioritized_features) < task_constraint:
            score = max(0.01, len(prioritized_features) * 0.15)  # Partial credit, clamped to (0, 1)
            explanation = f"Only prioritized {len(prioritized_features)}/{task_constraint} features"
            return score, explanation
        
        prioritized_features = prioritized_features[:task_constraint]
        
        # Calculate optimal ranking
        def calculate_criticality(feature: Feature) -> float:
            """Calculate criticality score."""
            user_impact = (min(feature.user_requests, 500) / 500.0) * 0.3
            satisfaction_impact = max(0, feature.impact_on_satisfaction) * 0.4
            revenue_impact = max(0, feature.impact_on_revenue) * 0.2
            churn_reduction = max(0, -feature.impact_on_churn) * 0.1
            return min(1.0, user_impact + satisfaction_impact + revenue_impact + churn_reduction)
        
        feature_map = {f.feature_id: f for f in features}
        criticality_scores = {
            fid: calculate_criticality(feature_map[fid])
            for fid in feature_map
        }
        
        optimal_ranking = sorted(
            criticality_scores.keys(),
            key=lambda x: criticality_scores[x],
            reverse=True
        )[:task_constraint]
        
        # Calculate ranking score
        score = 0.0
        matches = 0
        position_penalties = 0.0
        
        for i, prioritized_id in enumerate(prioritized_features):
            if prioritized_id in optimal_ranking:
                matches += 1
                optimal_pos = optimal_ranking.index(prioritized_id)
                position_difference = abs(i - optimal_pos)
                position_penalties += position_difference * 0.1
        
        # Scoring formula
        match_score = 0.65 * (matches / task_constraint)
        position_score = 0.25 * (1.0 - min(position_penalties / task_constraint, 1.0))
        coverage_score = 0.1 * (len(prioritized_features) / task_constraint)
        
        score = match_score + position_score + coverage_score
        
        explanation = f"Selected: {', '.join(prioritized_features[:3])}. "
        explanation += f"Optimal: {', '.join(optimal_ranking[:3])}. "
        explanation += f"Matches: {matches}/{task_constraint}"
        
        # Clamp score to (0, 1) exclusive
        score = max(0.01, min(0.99, score))
        return score, explanation


class HardTaskGrader(BaseGrader):
    """Grader for Hard Task: Make optimal trade-off decisions."""
    
    def grade(
        self,
        actions: List[Action],
        features: List[Feature],
        constraints: Dict,
        metrics_before: Dict,
        simulated_metrics_after: Dict
    ) -> Tuple[float, str]:
        """
        Grade trade-off decision quality (revenue vs satisfaction).
        
        Args:
            actions: List of actions taken
            features: List of features
            constraints: Current constraints
            metrics_before: Initial metrics
            simulated_metrics_after: Simulated metrics after decision
        
        Returns:
            Tuple of (score, explanation)
        """
        if not actions:
            return 0.01, "No actions taken"
        
        # Extract prioritized features
        prioritized_ids = [
            a.feature_id for a in actions
            if a.action_type.value == "prioritize_feature" and a.feature_id
        ]
        rejected_ids = [
            a.feature_id for a in actions
            if a.action_type.value == "reject_feature" and a.feature_id
        ]
        
        if not prioritized_ids and not rejected_ids:
            return 0.2, "Insufficient feature decisions made"
        
        feature_map = {f.feature_id: f for f in features}
        
        # Calculate net impact
        net_revenue_impact = sum(
            feature_map[fid].impact_on_revenue
            for fid in prioritized_ids
            if fid in feature_map
        )
        
        net_satisfaction_impact = sum(
            feature_map[fid].impact_on_satisfaction
            for fid in prioritized_ids
            if fid in feature_map
        )
        
        net_churn_reduction = sum(
            max(0, -feature_map[fid].impact_on_churn)
            for fid in prioritized_ids
            if fid in feature_map
        )
        
        # Effort and risk calculation
        total_effort = sum(
            feature_map[fid].effort
            for fid in prioritized_ids
            if fid in feature_map
        )
        
        avg_risk = (
            sum(feature_map[fid].risk for fid in prioritized_ids if fid in feature_map)
            / len(prioritized_ids)
            if prioritized_ids else 0
        )
        
        # Check if within constraints
        max_capacity = constraints.get("team_capacity", 200) * constraints.get("sprint_duration", 2)
        within_capacity = total_effort <= max_capacity
        
        # Trade-off evaluation
        # Good balance: satisfaction improvement + churn reduction, manageable revenue trade-offs
        satisfaction_churn_benefit = (net_satisfaction_impact + net_churn_reduction) / 2.0
        revenue_risk_penalty = max(0, -net_revenue_impact * 0.5) + (avg_risk * 0.2)
        
        decision_quality = max(
            0.0,
            satisfaction_churn_benefit - revenue_risk_penalty
        )
        
        # Normalize to (0, 1) exclusive
        decision_quality = max(0.01, min(0.99, decision_quality))
        
        # Bonus/penalty for constraint adherence
        if within_capacity:
            decision_quality = max(0.01, min(0.99, decision_quality + 0.15))
        else:
            decision_quality = max(0.01, min(0.99, decision_quality - 0.2))
        
        # Bonus for good risk management
        if avg_risk < 0.3:
            decision_quality = max(0.01, min(0.99, decision_quality + 0.1))
        elif avg_risk > 0.4:
            decision_quality = max(0.01, min(0.99, decision_quality - 0.1))
        
        explanation = f"Revenue impact: {net_revenue_impact:.2f}, "
        explanation += f"Satisfaction: {net_satisfaction_impact:.2f}, "
        explanation += f"Churn reduction: {net_churn_reduction:.2f}. "
        explanation += f"Total effort: {total_effort}/{max_capacity:.0f}. "
        explanation += f"Risk: {avg_risk:.2f}"
        
        # Clamp final score to (0, 1) exclusive
        return max(0.01, min(0.99, decision_quality)), explanation
