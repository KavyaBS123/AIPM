"""Pydantic schemas for the AI Product Manager Environment."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """Available actions for the product manager agent."""
    PRIORITIZE_FEATURE = "prioritize_feature"
    REJECT_FEATURE = "reject_feature"
    DELAY_FEATURE = "delay_feature"
    REQUEST_MORE_INFO = "request_more_info"
    FINALIZE_ROADMAP = "finalize_roadmap"


class Action(BaseModel):
    """Action taken by the product manager agent."""
    action_type: ActionType = Field(..., description="Type of action to take")
    feature_id: Optional[str] = Field(None, description="Feature ID associated with action")
    reason: Optional[str] = Field(None, description="Reasoning for the action")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        use_enum_values = True


class UserFeedback(BaseModel):
    """User feedback on product."""
    complaint: str = Field(..., description="User complaint or feedback")
    severity: float = Field(..., ge=0.0, le=1.0, description="Severity from 0.0 to 1.0")
    frequency: int = Field(..., ge=1, description="How many users reported this")
    sentiment: str = Field(..., description="Sentiment: positive, neutral, negative")


class ProductMetrics(BaseModel):
    """Current product metrics."""
    churn_rate: float = Field(..., ge=0.0, le=1.0, description="User churn rate")
    retention_rate: float = Field(..., ge=0.0, le=1.0, description="User retention rate")
    revenue: float = Field(..., ge=0.0, description="Monthly recurring revenue")
    user_satisfaction: float = Field(..., ge=0.0, le=1.0, description="User satisfaction score")
    engagement_score: float = Field(..., ge=0.0, le=1.0, description="User engagement score")
    active_users: int = Field(..., ge=0, description="Number of active users")


class Feature(BaseModel):
    """Product feature to consider."""
    feature_id: str = Field(..., description="Unique feature identifier")
    name: str = Field(..., description="Feature name")
    description: str = Field(..., description="Feature description")
    impact_on_satisfaction: float = Field(..., ge=-1.0, le=1.0, description="Impact on user satisfaction (-1 to 1)")
    impact_on_revenue: float = Field(..., ge=-1.0, le=1.0, description="Impact on revenue (-1 to 1)")
    impact_on_churn: float = Field(..., ge=-1.0, le=1.0, description="Impact on churn reduction (-1 to 1)")
    effort: float = Field(..., ge=0.1, le=100.0, description="Implementation effort (1-100)")
    risk: float = Field(..., ge=0.0, le=1.0, description="Implementation risk")
    user_requests: int = Field(..., ge=0, description="Number of user requests for this feature")
    priority_score: Optional[float] = Field(None, description="Current priority score")


class Constraint(BaseModel):
    """Constraints for product roadmap."""
    sprint_duration: int = Field(..., description="Sprint duration in weeks")
    team_capacity: float = Field(..., description="Team capacity in story points per sprint")
    budget_available: float = Field(..., description="Available budget in dollars")
    deadline: Optional[str] = Field(None, description="Hard deadline date")
    max_parallel_features: int = Field(..., description="Max features that can be implemented in parallel")


class PMState(BaseModel):
    """Current state of the product manager environment."""
    step_count: int = Field(..., ge=0, description="Current step number")
    user_feedback: List[UserFeedback] = Field(..., description="List of user feedback")
    metrics: ProductMetrics = Field(..., description="Current product metrics")
    available_features: List[Feature] = Field(..., description="Features available for prioritization")
    constraints: Constraint = Field(..., description="Current constraints")
    prioritized_features: List[str] = Field(default_factory=list, description="IDs of prioritized features")
    rejected_features: List[str] = Field(default_factory=list, description="IDs of rejected features")
    delayed_features: List[str] = Field(default_factory=list, description="IDs of delayed features")
    actions_taken: List[Action] = Field(default_factory=list, description="History of actions taken")
    task_name: Optional[str] = Field(None, description="Current task name")


class Observation(BaseModel):
    """Observation returned to the agent."""
    step: int = Field(..., description="Current step number")
    summarized_feedback: str = Field(..., description="AI-generated summary of user feedback")
    metrics_summary: Dict[str, float] = Field(..., description="Current product metrics")
    features_summary: str = Field(..., description="Summary of available features")
    prioritized_count: int = Field(..., description="Number of features prioritized so far")
    rejected_count: int = Field(..., description="Number of features rejected so far")
    delayed_count: int = Field(..., description="Number of features delayed so far")
    constraint_info: str = Field(..., description="Summary of constraints")
    available_actions: List[str] = Field(..., description="List of available action types")
    time_remaining: float = Field(..., description="Remaining steps as fraction of total (0.0 to 1.0)")


class Reward(BaseModel):
    """Reward information returned after step."""
    total_reward: float = Field(..., description="Total reward for this step")
    decision_quality: float = Field(..., ge=0.0, le=1.0, description="Quality of the decision (0-1)")
    alignment_with_feedback: float = Field(..., ge=-1.0, le=1.0, description="Alignment with user feedback")
    revenue_impact: float = Field(..., ge=-1.0, le=1.0, description="Estimated revenue impact")
    satisfaction_impact: float = Field(..., ge=-1.0, le=1.0, description="Estimated satisfaction impact")
    churn_impact: float = Field(..., ge=-1.0, le=1.0, description="Estimated churn impact")
    reason: str = Field(..., description="Explanation of reward")
    breakdown: Dict[str, float] = Field(default_factory=dict, description="Detailed reward breakdown")
