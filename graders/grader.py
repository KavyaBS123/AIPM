"""Grader system for evaluating task performance."""

from typing import Dict, List, Tuple
from abc import ABC, abstractmethod

from pm_env.models import Observation


class BaseGrader(ABC):
    """Abstract base class for task graders."""
    
    @abstractmethod
    def grade(
        self,
        actions_taken: List[str],
        scenario: Dict,
        observation: Observation
    ) -> Tuple[float, Dict]:
        """
        Grade the agent's performance.
        
        Args:
            actions_taken: List of actions in "action_type:feature_id" format
            scenario: Scenario data including correct_priority_order
            observation: Final observation state
            
        Returns:
            Tuple of (score: 0.0-1.0, explanation_dict)
        """
        pass


class EasyTaskGrader(BaseGrader):
    """Grader for Easy task: Critical Feature Identification."""
    
    def grade(
        self,
        actions_taken: List[str],
        scenario: Dict,
        observation: Observation
    ) -> Tuple[float, Dict]:
        """
        Grade Task 1: Did the agent identify the correct top feature?
        
        Scoring:
        - 1.0: Correctly prioritized the #1 feature
        - 0.5: Prioritized the #2 feature from correct_priority_order
        - 0.0: Wrong feature or no prioritization
        """
        correct_priority = scenario.get("correct_priority_order", [])
        
        if not correct_priority:
            return 0.0, {"error": "No correct_priority_order in scenario"}
        
        # Extract prioritized features
        prioritized = [
            a.split(":")[1] for a in actions_taken
            if a.startswith("prioritize:")
        ]
        
        if not prioritized:
            return 0.0, {
                "reason": "No features prioritized",
                "correct_feature": correct_priority[0] if correct_priority else None,
                "prioritized_features": []
            }
        
        score = 0.0
        first_prioritized = prioritized[0]
        
        if first_prioritized == correct_priority[0]:
            score = 1.0
            reason = f"Correctly identified critical feature {first_prioritized}"
        elif len(correct_priority) > 1 and first_prioritized == correct_priority[1]:
            score = 0.5
            reason = f"Identified second-best feature {first_prioritized}"
        else:
            score = 0.0
            reason = f"Incorrect feature {first_prioritized}"
        
        return score, {
            "reason": reason,
            "score": score,
            "correct_feature": correct_priority[0],
            "prioritized_features": prioritized,
            "correct_priority_order": correct_priority
        }


class MediumTaskGrader(BaseGrader):
    """Grader for Medium task: Roadmap Prioritization."""
    
    def grade(
        self,
        actions_taken: List[str],
        scenario: Dict,
        observation: Observation
    ) -> Tuple[float, Dict]:
        """
        Grade Task 2: Are the top 3 features ranked correctly?
        
        Scoring:
        - 1.0: All 3 features in correct order
        - 0.7: 2 out of 3 correct
        - 0.3: 1 out of 3 correct
        - 0.0: No correct matches
        """
        correct_priority = scenario.get("correct_priority_order", [])
        
        if len(correct_priority) < 3:
            return 0.0, {"error": "Scenario has fewer than 3 priority features"}
        
        target_features = correct_priority[:3]
        
        # Extract prioritized features in order
        prioritized = [
            a.split(":")[1] for a in actions_taken
            if a.startswith("prioritize:")
        ]
        
        if len(prioritized) < 3:
            # Partial credit for fewer than 3 prioritizations
            matches = sum(1 for p in prioritized if p in target_features)
            score = 0.3 * (matches / 3) if matches > 0 else 0.0
        else:
            prioritized = prioritized[:3]
            
            # Count matches
            matches = sum(1 for i, p in enumerate(prioritized) if i < len(target_features) and p == target_features[i])
            
            if matches == 3:
                score = 1.0
                reason = "Perfect ranking of top 3 features"
            elif matches == 2:
                score = 0.7
                reason = "2 out of 3 features correctly ranked"
            elif matches == 1:
                score = 0.3
                reason = "1 out of 3 features correctly ranked"
            else:
                score = 0.0
                reason = "No features in correct order"
            
            return score, {
                "reason": reason,
                "score": score,
                "correct_top_3": target_features,
                "prioritized": prioritized,
                "matches": matches
            }
        
        return score, {
            "reason": f"Prioritized only {len(prioritized)} feature(s), {matches} correct",
            "score": score,
            "correct_top_3": target_features,
            "prioritized": prioritized,
            "matches": matches
        }


class HardTaskGrader(BaseGrader):
    """Grader for Hard task: Strategic Trade-off Decision."""
    
    def grade(
        self,
        actions_taken: List[str],
        scenario: Dict,
        observation: Observation
    ) -> Tuple[float, Dict]:
        """
        Grade Task 3: Quality of trade-off decisions.
        
        Scoring factors:
        - Correctness: How many top features were prioritized (weight: 0.6)
        - Constraint adherence: Did they respect budget/capacity? (weight: 0.3)
        - Decision justification: Did they provide reasoning? (weight: 0.1)
        """
        correct_priority = scenario.get("correct_priority_order", [])
        constraints = observation.constraints
        
        # Extract actions
        prioritized = [a.split(":")[1] for a in actions_taken if a.startswith("prioritize:")]
        rejected = [a.split(":")[1] for a in actions_taken if a.startswith("reject:")]
        actions_with_justification = [
            a for a in actions_taken
            if ":" in a and len(a.split(":")) > 1
        ]
        
        # 1. Feature correctness score (0.6 weight)
        correct_matches = sum(
            1 for p in prioritized if p in correct_priority[:3]
        )
        feature_score = correct_matches / 3
        
        # 2. Constraint adherence score (0.3 weight)
        constraint_score = 1.0
        
        # Check sprint capacity
        sprint_capacity = constraints.get("sprint_capacity", float('inf'))
        total_effort = sum(
            next(
                (f.effort for f in observation.feature_backlog if f.id == p),
                0
            )
            for p in prioritized
        )
        
        if total_effort > sprint_capacity:
            constraint_penalty = min(0.3, (total_effort - sprint_capacity) / sprint_capacity * 0.3)
            constraint_score -= constraint_penalty
        
        # 3. Justification score (0.1 weight)
        justification_score = min(1.0, len(actions_with_justification) / 4)
        
        # Combine scores
        score = (
            feature_score * 0.6 +
            constraint_score * 0.3 +
            justification_score * 0.1
        )
        
        score = max(0.0, min(1.0, score))
        
        return score, {
            "score": score,
            "feature_score": feature_score,
            "constraint_score": constraint_score,
            "justification_score": justification_score,
            "correct_priority_order": correct_priority,
            "prioritized_features": prioritized,
            "rejected_features": rejected,
            "total_effort": total_effort,
            "sprint_capacity": sprint_capacity,
            "constraint_violated": total_effort > sprint_capacity,
            "num_justified_actions": len(actions_with_justification)
        }


def grade_task(
    task_id: str,
    actions_taken: List[str],
    scenario: Dict,
    observation: Observation
) -> Tuple[float, Dict]:
    """
    Grade a task based on its difficulty.
    
    Args:
        task_id: Task identifier
        actions_taken: List of actions in "action_type:feature_id" format
        scenario: Scenario data
        observation: Final observation state
        
    Returns:
        Tuple of (score, explanation_dict)
    """
    if task_id == "task_001":
        grader = EasyTaskGrader()
    elif task_id == "task_002":
        grader = MediumTaskGrader()
    elif task_id == "task_003":
        grader = HardTaskGrader()
    else:
        raise ValueError(f"Unknown task: {task_id}")
    
    return grader.grade(actions_taken, scenario, observation)
