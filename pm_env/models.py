"""Pydantic models for the AI Product Manager Environment."""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class Feature(BaseModel):
    """Represents a feature in the backlog."""
    
    id: str = Field(..., description="Unique feature identifier")
    name: str = Field(..., description="Feature name")
    impact_area: str = Field(..., description="Impact area: retention, revenue, or satisfaction")
    effort: int = Field(..., ge=1, le=5, description="Effort level from 1 to 5")
    votes: int = Field(..., ge=0, description="User votes for this feature")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "F001",
                "name": "Dark Mode",
                "impact_area": "satisfaction",
                "effort": 2,
                "votes": 145
            }
        }


class Metrics(BaseModel):
    """Key product metrics."""
    
    churn_rate: float = Field(..., ge=0.0, le=1.0, description="Current churn rate (0-1)")
    retention_rate: float = Field(..., ge=0.0, le=1.0, description="Current retention rate (0-1)")
    revenue_growth: float = Field(..., description="Monthly revenue growth percentage")
    user_satisfaction: float = Field(..., ge=0.0, le=100.0, description="User satisfaction score 0-100")
    
    class Config:
        json_schema_extra = {
            "example": {
                "churn_rate": 0.08,
                "retention_rate": 0.92,
                "revenue_growth": 12.5,
                "user_satisfaction": 68.0
            }
        }


class Observation(BaseModel):
    """Complete observation state returned by environment."""
    
    scenario_id: str = Field(..., description="Current scenario identifier")
    user_complaints: List[str] = Field(..., description="List of main user complaints")
    metrics: Metrics = Field(..., description="Current product metrics")
    feature_backlog: List[Feature] = Field(..., description="Available features to prioritize")
    constraints: Dict[str, int] = Field(..., description="Constraints: budget, sprint_capacity, etc.")
    previous_actions: List[str] = Field(default_factory=list, description="History of actions taken")
    step_count: int = Field(default=0, ge=0, description="Current step number")
    
    class Config:
        json_schema_extra = {
            "example": {
                "scenario_id": "scenario_1",
                "user_complaints": ["App crashes on login", "Sync is too slow"],
                "metrics": {
                    "churn_rate": 0.08,
                    "retention_rate": 0.92,
                    "revenue_growth": 12.5,
                    "user_satisfaction": 68.0
                },
                "feature_backlog": [],
                "constraints": {"budget": 50000, "sprint_capacity": 40},
                "previous_actions": [],
                "step_count": 0
            }
        }


class Action(BaseModel):
    """Action taken by the agent."""
    
    action_type: str = Field(..., description="One of: prioritize, reject, delay, request_info, finalize")
    feature_id: Optional[str] = Field(None, description="Feature ID (required for prioritize/reject/delay)")
    justification: Optional[str] = Field(None, description="Explanation for the action")
    
    class Config:
        json_schema_extra = {
            "example": {
                "action_type": "prioritize",
                "feature_id": "F001",
                "justification": "Highest user votes and impacts satisfaction"
            }
        }


class StepResult(BaseModel):
    """Result of one environment step."""
    
    observation: Observation = Field(..., description="Updated observation")
    reward: float = Field(..., ge=-1.0, le=1.0, description="Reward for this step")
    done: bool = Field(..., description="Whether episode is complete")
    info: Dict = Field(default_factory=dict, description="Additional debugging info")
    
    class Config:
        json_schema_extra = {
            "example": {
                "observation": {
                    "scenario_id": "scenario_1",
                    "user_complaints": ["App crashes on login"],
                    "metrics": {
                        "churn_rate": 0.08,
                        "retention_rate": 0.92,
                        "revenue_growth": 12.5,
                        "user_satisfaction": 68.0
                    },
                    "feature_backlog": [],
                    "constraints": {"budget": 50000, "sprint_capacity": 40},
                    "previous_actions": ["prioritize:F001"],
                    "step_count": 1
                },
                "reward": 0.4,
                "done": False,
                "info": {"reason": "Valid prioritization"}
            }
        }
