"""Task definitions for AI Product Manager Environment."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class TaskDefinition(BaseModel):
    """Definition of a task for the environment."""
    task_id: str = Field(..., description="Unique task identifier")
    name: str = Field(..., description="Task name")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, hard")
    description: str = Field(..., description="Task description")
    objective: str = Field(..., description="Clear objective for the agent")
    steps_allowed: int = Field(..., description="Number of steps agent has to complete task")
    success_criteria: str = Field(..., description="What constitutes success")
    hints: Optional[str] = Field(None, description="Hints for solving the task")
    maximum_reward: float = Field(..., description="Maximum possible reward")
    grader_class: str = Field(..., description="Grader class name (e.g., 'EasyTaskGrader')")


TASK_DEFINITIONS = {
    "task_easy_identify_critical": TaskDefinition(
        task_id="task_001",
        name="Identify Most Critical Feature",
        difficulty="easy",
        description="Analyze user feedback and product metrics to identify the single most critical feature to prioritize.",
        objective="Prioritize the one feature that best addresses the most critical user pain point and product metric.",
        steps_allowed=5,
        success_criteria="The prioritized feature should be the one with highest criticality (combination of user requests, satisfaction impact, and churn reduction).",
        hints="Look at user complaint frequency, severity, and feature impact on satisfaction and churn.",
        maximum_reward=1.0,
        grader_class="EasyTaskGrader"
    ),
    "task_medium_rank_features": TaskDefinition(
        task_id="task_002",
        name="Optimized Feature Ranking",
        difficulty="medium",
        description="Rank and prioritize the top 3 features considering user feedback, metrics, effort, and constraints.",
        objective="Create an optimal prioritization ranking of top 3 features that balances impact, effort, and risk.",
        steps_allowed=15,
        success_criteria="Top 3 prioritized features should match the optimal ranking considering criticality and constraints.",
        hints="Consider both user impact (satisfaction, churn reduction) and implementation constraints (effort, risk, team capacity).",
        maximum_reward=1.0,
        grader_class="MediumTaskGrader"
    ),
    "task_hard_tradeoff": TaskDefinition(
        task_id="task_003",
        name="Strategic Trade-off Decision",
        difficulty="hard",
        description="Make strategic trade-off decisions between revenue goals and user satisfaction. Build a complete roadmap.",
        objective="Create a feature roadmap that optimally balances revenue impact, user satisfaction gains, and implementation constraints.",
        steps_allowed=25,
        success_criteria="Roadmap should demonstrate good trade-off judgment, staying within constraints while maximizing stakeholder value.",
        hints="Some features boost revenue but hurt satisfaction. Balance stakeholder interests. Consider multi-sprint planning.",
        maximum_reward=1.0,
        grader_class="HardTaskGrader"
    )
}


def get_task_definition(task_id: str) -> TaskDefinition:
    """Get a task definition by ID."""
    if task_id not in TASK_DEFINITIONS:
        raise ValueError(f"Unknown task: {task_id}. Available: {list(TASK_DEFINITIONS.keys())}")
    return TASK_DEFINITIONS[task_id]


def list_tasks() -> list[str]:
    """List all available task IDs."""
    return list(TASK_DEFINITIONS.keys())


def get_all_tasks() -> Dict[str, TaskDefinition]:
    """Get all task definitions."""
    return TASK_DEFINITIONS
