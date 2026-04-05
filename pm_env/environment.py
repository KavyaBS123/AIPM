"""Main environment class for the AI Product Manager Environment."""

import copy
import json
from typing import Dict, Optional, Tuple
import os

from pm_env.models import Action, Feature, Metrics, Observation, StepResult
from pm_env.reward import RewardCalculator


class ProductManagerEnv:
    """
    OpenEnv-compatible AI Product Manager Environment.
    
    An RL environment where an AI agent acts as a Product Manager,
    making decisions about feature prioritization, rejection, and scheduling.
    """
    
    def __init__(self, scenario_data: Dict = None):
        """
        Initialize the environment.
        
        Args:
            scenario_data: Dictionary containing scenario configuration
        """
        self.scenario_data = scenario_data or {}
        self.current_observation = None
        self.done = False
        self.step_count = 0
        self.max_steps = 10  # Default max steps
        self.reward_calculator = RewardCalculator()
        
        # Track prioritized, rejected, and delayed features
        self.prioritized_features = []
        self.rejected_features = []
        self.delayed_features = []
    
    def reset(self) -> Observation:
        """
        Reset the environment to initial state.
        
        Returns:
            Initial observation
        """
        self.step_count = 0
        self.done = False
        self.prioritized_features = []
        self.rejected_features = []
        self.delayed_features = []
        
        # Create initial observation from scenario
        metrics = Metrics(**self.scenario_data.get("metrics", {}))
        
        features = []
        for feature_data in self.scenario_data.get("features", []):
            features.append(Feature(**feature_data))
        
        self.current_observation = Observation(
            scenario_id=self.scenario_data.get("id", "unknown"),
            user_complaints=self.scenario_data.get("user_complaints", []),
            metrics=metrics,
            feature_backlog=features,
            constraints=self.scenario_data.get("constraints", {}),
            previous_actions=[],
            step_count=0
        )
        
        return self.current_observation
    
    def step(self, action: Action) -> StepResult:
        """
        Execute one step in the environment.
        
        Args:
            action: Action to execute
            
        Returns:
            StepResult containing observation, reward, done, info
        """
        if self.current_observation is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")
        
        info = {
            "step": self.step_count,
            "action_executed": action.dict()
        }
        
        # Validate and execute action
        is_valid, validation_info = self._validate_action(action)
        info.update(validation_info)
        
        if not is_valid:
            reward = -0.2  # Penalty for invalid action
            info["invalid_action"] = True
        else:
            # Calculate reward
            reward, reward_info = self.reward_calculator.calculate_reward(
                action,
                self.current_observation,
                self.scenario_data,
                is_first_action=(self.step_count == 0)
            )
            info.update(reward_info)
            
            # Execute action
            self._execute_action(action)
        
        # Update observation
        self.step_count += 1
        self.current_observation.step_count = self.step_count
        self.current_observation.previous_actions.append(
            self._action_to_string(action)
        )
        
        # Check if episode is done
        self.done = (
            action.action_type == "finalize" or
            self.step_count >= self.max_steps
        )
        
        info["done"] = self.done
        
        return StepResult(
            observation=copy.deepcopy(self.current_observation),
            reward=reward,
            done=self.done,
            info=info
        )
    
    def state(self) -> Dict:
        """
        Get the full state dict.
        
        Returns:
            Dictionary representation of current state
        """
        if self.current_observation is None:
            return {"status": "not_initialized"}
        
        return {
            "observation": self.current_observation.dict(),
            "step_count": self.step_count,
            "done": self.done,
            "prioritized_features": self.prioritized_features,
            "rejected_features": self.rejected_features,
            "delayed_features": self.delayed_features,
            "scenario_id": self.scenario_data.get("id", "unknown")
        }
    
    def _validate_action(self, action: Action) -> Tuple[bool, Dict]:
        """
        Validate if an action is legal.
        
        Args:
            action: Action to validate
            
        Returns:
            Tuple of (is_valid, validation_info)
        """
        valid_types = ["prioritize", "reject", "delay", "request_info", "finalize"]
        
        if action.action_type not in valid_types:
            return False, {"validation": f"Invalid action type: {action.action_type}"}
        
        # Finalize and request_info don't require feature_id
        if action.action_type in ["finalize", "request_info"]:
            return True, {"validation": "Valid"}
        
        # Other actions require feature_id
        if not action.feature_id:
            return False, {"validation": "feature_id required for this action"}
        
        # Check if feature exists in backlog
        feature_ids = [f.id for f in self.current_observation.feature_backlog]
        if action.feature_id not in feature_ids:
            return False, {"validation": f"Feature {action.feature_id} not in backlog"}
        
        # Check if feature already processed
        processed = (
            self.prioritized_features +
            self.rejected_features +
            self.delayed_features
        )
        if action.feature_id in processed:
            return False, {"validation": f"Feature {action.feature_id} already processed"}
        
        # Check budget constraints for prioritize
        if action.action_type == "prioritize":
            budget = self.current_observation.constraints.get("budget", float('inf'))
            sprint_capacity = self.current_observation.constraints.get("sprint_capacity", float('inf'))
            
            feature = next(
                (f for f in self.current_observation.feature_backlog if f.id == action.feature_id),
                None
            )
            if feature:
                # Simple check: effort shouldn't exceed remaining capacity
                prioritized_effort = sum(
                    next(
                        (f.effort for f in self.current_observation.feature_backlog if f.id == fid),
                        0
                    )
                    for fid in self.prioritized_features
                )
                if prioritized_effort + feature.effort > sprint_capacity:
                    return False, {"validation": "Exceeds sprint capacity"}
        
        return True, {"validation": "Valid"}
    
    def _execute_action(self, action: Action) -> None:
        """
        Execute the action and update environment state.
        
        Args:
            action: Action to execute
        """
        if action.action_type == "prioritize":
            self.prioritized_features.append(action.feature_id)
        elif action.action_type == "reject":
            self.rejected_features.append(action.feature_id)
        elif action.action_type == "delay":
            self.delayed_features.append(action.feature_id)
        # request_info and finalize don't modify feature state
    
    def _action_to_string(self, action: Action) -> str:
        """Convert action to string representation."""
        if action.feature_id:
            return f"{action.action_type}:{action.feature_id}"
        return action.action_type


def load_scenario(scenario_id: str) -> Dict:
    """
    Load a scenario from scenarios.json.
    
    Args:
        scenario_id: ID of scenario to load
        
    Returns:
        Scenario data dictionary
    """
    scenarios_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "scenarios",
        "scenarios.json"
    )
    
    try:
        with open(scenarios_path, "r") as f:
            scenarios = json.load(f)
        
        scenario = next(
            (s for s in scenarios.get("scenarios", []) if s.get("id") == scenario_id),
            None
        )
        
        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        return scenario
    except FileNotFoundError:
        raise FileNotFoundError(f"Scenarios file not found at {scenarios_path}")


def create_environment(scenario_id: str, max_steps: int = 10) -> ProductManagerEnv:
    """
    Factory function to create an environment with a specific scenario.
    
    Args:
        scenario_id: ID of the scenario to load
        max_steps: Maximum steps allowed per episode
        
    Returns:
        Initialized ProductManagerEnv
    """
    scenario_data = load_scenario(scenario_id)
    env = ProductManagerEnv(scenario_data)
    env.max_steps = max_steps
    return env
