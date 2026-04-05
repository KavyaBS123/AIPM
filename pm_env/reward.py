"""Reward function logic for the AI Product Manager Environment."""

from typing import Dict, List
from pm_env.models import Action, Feature, Observation


class RewardCalculator:
    """Calculates reward based on agent actions and environment feedback."""
    
    # Reward structure
    PRIORITIZE_HIGH_IMPACT_REWARD = 0.4
    VALID_JUSTIFICATION_REWARD = 0.2
    REJECT_CRITICAL_PENALTY = -0.3
    FINALIZE_GOOD_ROADMAP_REWARD = 0.1
    REQUEST_INFO_REWARD = 0.0
    
    def __init__(self):
        """Initialize reward calculator."""
        self.reward = 0.0
    
    def calculate_reward(
        self,
        action: Action,
        observation: Observation,
        scenario_data: Dict,
        is_first_action: bool = False
    ) -> tuple[float, Dict]:
        """
        Calculate reward for the given action.
        
        Args:
            action: The action taken by the agent
            observation: Current observation
            scenario_data: The full scenario data with correct_priority_order
            is_first_action: Whether this is the first action in the episode
            
        Returns:
            Tuple of (reward_value, info_dict)
        """
        self.reward = 0.0
        info = {
            "action_type": action.action_type,
            "reward_components": []
        }
        
        if action.action_type == "prioritize":
            self.reward, prioritize_info = self._reward_prioritize(
                action, observation, scenario_data
            )
            info["reward_components"].append(prioritize_info)
            
            # Bonus for valid justification
            if action.justification and len(action.justification.strip()) > 5:
                self.reward += self.VALID_JUSTIFICATION_REWARD
                info["reward_components"].append({
                    "component": "valid_justification",
                    "value": self.VALID_JUSTIFICATION_REWARD
                })
        
        elif action.action_type == "reject":
            self.reward, reject_info = self._reward_reject(
                action, observation, scenario_data
            )
            info["reward_components"].append(reject_info)
        
        elif action.action_type == "delay":
            info["reward_components"].append({
                "component": "delay_action",
                "value": 0.0,
                "reason": "Neutral action"
            })
        
        elif action.action_type == "request_info":
            info["reward_components"].append({
                "component": "request_info",
                "value": self.REQUEST_INFO_REWARD,
                "reason": "Neutral exploration action"
            })
        
        elif action.action_type == "finalize":
            self.reward, finalize_info = self._reward_finalize(
                action, observation, scenario_data
            )
            info["reward_components"].append(finalize_info)
        
        # Clip reward to valid range
        self.reward = max(-1.0, min(1.0, self.reward))
        info["total_reward"] = self.reward
        
        return self.reward, info
    
    def _reward_prioritize(
        self,
        action: Action,
        observation: Observation,
        scenario_data: Dict
    ) -> tuple[float, Dict]:
        """Reward for prioritizing a feature."""
        reward = 0.0
        reason = ""
        
        if not action.feature_id:
            return 0.0, {
                "component": "prioritize",
                "value": 0.0,
                "reason": "No feature_id provided"
            }
        
        # Find the feature
        feature = None
        for f in observation.feature_backlog:
            if f.id == action.feature_id:
                feature = f
                break
        
        if not feature:
            return 0.0, {
                "component": "prioritize",
                "value": 0.0,
                "reason": f"Feature {action.feature_id} not in backlog"
            }
        
        # Check if it's a high-impact feature
        correct_priority = scenario_data.get("correct_priority_order", [])
        if action.feature_id in correct_priority:
            position = correct_priority.index(action.feature_id)
            # Higher reward for prioritizing high-priority items first
            if position == 0:
                reward = self.PRIORITIZE_HIGH_IMPACT_REWARD
                reason = f"Feature {action.feature_id} is top priority"
            elif position == 1:
                reward = self.PRIORITIZE_HIGH_IMPACT_REWARD * 0.7
                reason = f"Feature {action.feature_id} is second priority"
            else:
                reward = self.PRIORITIZE_HIGH_IMPACT_REWARD * 0.4
                reason = f"Feature {action.feature_id} is in top priorities"
        else:
            # Penalize slightly for low-priority features
            reward = -0.1
            reason = f"Feature {action.feature_id} is not a top priority"
        
        return reward, {
            "component": "prioritize",
            "value": reward,
            "reason": reason,
            "feature_id": action.feature_id,
            "impact_area": feature.impact_area,
            "effort": feature.effort,
            "votes": feature.votes
        }
    
    def _reward_reject(
        self,
        action: Action,
        observation: Observation,
        scenario_data: Dict
    ) -> tuple[float, Dict]:
        """Reward for rejecting a feature."""
        reward = 0.0
        reason = ""
        
        if not action.feature_id:
            return 0.0, {
                "component": "reject",
                "value": 0.0,
                "reason": "No feature_id provided"
            }
        
        # Find the feature
        feature = None
        for f in observation.feature_backlog:
            if f.id == action.feature_id:
                feature = f
                break
        
        if not feature:
            return 0.0, {
                "component": "reject",
                "value": 0.0,
                "reason": f"Feature {action.feature_id} not in backlog"
            }
        
        # Check if it's a critical feature
        correct_priority = scenario_data.get("correct_priority_order", [])
        if action.feature_id in correct_priority[:2]:  # Top 2 features are critical
            reward = self.REJECT_CRITICAL_PENALTY
            reason = f"Rejected critical feature {action.feature_id}"
        else:
            reward = 0.05  # Small reward for rejecting low-priority features
            reason = f"Reasonably rejected low-priority feature {action.feature_id}"
        
        return reward, {
            "component": "reject",
            "value": reward,
            "reason": reason,
            "feature_id": action.feature_id
        }
    
    def _reward_finalize(
        self,
        action: Action,
        observation: Observation,
        scenario_data: Dict
    ) -> tuple[float, Dict]:
        """Reward for finalizing the roadmap."""
        # Evaluate the quality of prioritized features
        prioritized = [
            a.split(":")[1] for a in observation.previous_actions
            if a.startswith("prioritize:")
        ]
        
        correct_priority = scenario_data.get("correct_priority_order", [])
        
        # Calculate how many top features were correctly prioritized
        matches = sum(1 for p in prioritized if p in correct_priority)
        accuracy = matches / len(correct_priority) if correct_priority else 1.0
        
        reward = self.FINALIZE_GOOD_ROADMAP_REWARD * accuracy
        
        return reward, {
            "component": "finalize",
            "value": reward,
            "reason": f"Finalized roadmap with {accuracy:.0%} accuracy",
            "correct_features": len(correct_priority),
            "prioritized_features": len(prioritized),
            "matches": matches
        }
