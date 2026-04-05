"""Task definitions for the AI Product Manager Environment."""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class TaskDefinition:
    """Definition of a task in the environment."""
    
    task_id: str
    name: str
    description: str
    difficulty: str
    max_steps: int
    objective: str
    success_criteria: str
    hints: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty,
            "max_steps": self.max_steps,
            "objective": self.objective,
            "success_criteria": self.success_criteria,
            "hints": self.hints,
        }


# Task 1: Easy - Critical Feature Identification
TASK_001 = TaskDefinition(
    task_id="task_001",
    name="Critical Feature Identification",
    description="Identify the single most critical feature to prioritize",
    difficulty="easy",
    max_steps=3,
    objective=(
        "Analyze user complaints, product metrics, and feature data to identify "
        "the SINGLE most critical feature that should be prioritized first. "
        "You must decide and finalize within 3 steps."
    ),
    success_criteria=(
        "Correctly identify the top feature from the correct_priority_order. "
        "Score: 1.0 if correct, 0.5 if second-best, 0.0 if wrong."
    ),
    hints=[
        "Look at the number of user votes for features",
        "Consider which impact area (retention/revenue/satisfaction) aligns with current metrics",
        "High user votes + relevant impact area = likely critical feature",
        "Pay attention to the severity of user complaints",
    ]
)

# Task 2: Medium - Roadmap Prioritization
TASK_002 = TaskDefinition(
    task_id="task_002",
    name="Roadmap Prioritization",
    description="Rank the top 3 features in correct priority order",
    difficulty="medium",
    max_steps=6,
    objective=(
        "Analyze the scenario and prioritize the top 3 features in the correct order. "
        "You must use request_info to gather insights, then make your prioritization decisions. "
        "Finalize your roadmap decision within 6 steps."
    ),
    success_criteria=(
        "The 3 features you prioritize must be in the correct order from correct_priority_order. "
        "Score: 1.0 for perfect order, 0.7 for 2 correct, 0.3 for 1 correct, 0.0 for no matches."
    ),
    hints=[
        "Use request_info action to explore different feature combinations",
        "Consider both user demand (votes) and business impact",
        "Think about dependencies: does fixing one issue enable solving another?",
        "Balance user satisfaction, retention, and revenue impact",
        "It's okay to reject low-priority features first",
    ]
)

# Task 3: Hard - Trade-off Decision Making
TASK_003 = TaskDefinition(
    task_id="task_003",
    name="Strategic Trade-off Decision",
    description="Make strategic feature trade-offs within budget constraints",
    difficulty="hard",
    max_steps=10,
    objective=(
        "You are a PM facing hard trade-offs. You have limited budget and sprint capacity. "
        "You must create a balanced roadmap that maximizes business value while respecting constraints. "
        "Consider revenue vs retention vs satisfaction. Justify your decisions. Finalize within 10 steps."
    ),
    success_criteria=(
        "The prioritized features should maximize overall business impact given constraints. "
        "Scoring considers: correctness of priority (weighting towards top features), "
        "budget adherence, and quality of justifications. "
        "Max score: 1.0 for optimal decisions; penalty for constraint violations."
    ),
    hints=[
        "Review the sprint_capacity and budget constraints first",
        "Small effort features can give quick wins; consider them for morale",
        "Revenue-focused features might be necessary for growth, but watch retention metrics",
        "If churn is high, prioritize retention features",
        "Justify each decision with data: votes, impact area, and metrics context",
        "Consider the ripple effects of delaying certain features",
        "It's strategic to reject low-demand features to focus team",
    ]
)


# Task registry
TASKS = {
    "task_001": TASK_001,
    "task_002": TASK_002,
    "task_003": TASK_003,
}


def get_task(task_id: str) -> TaskDefinition:
    """
    Get task definition by ID.
    
    Args:
        task_id: Task identifier
        
    Returns:
        TaskDefinition object
        
    Raises:
        ValueError if task not found
    """
    if task_id not in TASKS:
        raise ValueError(f"Task {task_id} not found. Available: {list(TASKS.keys())}")
    return TASKS[task_id]


def list_tasks() -> List[TaskDefinition]:
    """Get all available tasks."""
    return list(TASKS.values())


def get_tasks_by_difficulty(difficulty: str) -> List[TaskDefinition]:
    """Get tasks filtered by difficulty."""
    return [t for t in TASKS.values() if t.difficulty == difficulty]
