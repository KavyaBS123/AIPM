"""
GRADER MANIFEST - Complete Task-Grader Registry
This file explicitly lists all available graders for the validator to discover.
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class TaskGraderEntry:
    """Maps a task to its grader class"""
    task_id: str
    task_name: str
    grader_class_name: str
    difficulty: str


# Complete registry of all graders
GRADER_REGISTRY: Dict[str, TaskGraderEntry] = {
    "task_001": TaskGraderEntry(
        task_id="task_001",
        task_name="Identify Most Critical Feature",
        grader_class_name="EasyTaskGrader",
        difficulty="easy"
    ),
    "task_002": TaskGraderEntry(
        task_id="task_002",
        task_name="Optimized Feature Ranking",
        grader_class_name="MediumTaskGrader",
        difficulty="medium"
    ),
    "task_003": TaskGraderEntry(
        task_id="task_003",
        task_name="Strategic Trade-off Decision",
        grader_class_name="HardTaskGrader",
        difficulty="hard"
    ),
}


def get_tasks_with_graders() -> List[TaskGraderEntry]:
    """
    Get all tasks that have graders.
    
    This is explicitly what the validator checks.
    
    Returns:
        List of TaskGraderEntry objects
    """
    return list(GRADER_REGISTRY.values())


def get_grader_for_task(task_id: str) -> str:
    """Get the grader class name for a specific task"""
    if task_id in GRADER_REGISTRY:
        return GRADER_REGISTRY[task_id].grader_class_name
    return None


def get_grader_count() -> int:
    """Get count of tasks with graders"""
    return len(GRADER_REGISTRY)


def is_grader_enabled(task_id: str) -> bool:
    """Check if a task has a grader enabled"""
    return task_id in GRADER_REGISTRY


def validate_grader_setup() -> Dict[str, any]:
    """
    Validate that the grader setup is correct.
    
    Returns:
        Validation result dict
    """
    from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
    
    grader_classes = {
        'EasyTaskGrader': EasyTaskGrader,
        'MediumTaskGrader': MediumTaskGrader,
        'HardTaskGrader': HardTaskGrader,
    }
    
    tasks_with_graders = get_tasks_with_graders()
    all_valid = True
    
    for entry in tasks_with_graders:
        grader_class = grader_classes.get(entry.grader_class_name)
        if not grader_class:
            all_valid = False
            break
        try:
            grader = grader_class()
        except Exception:
            all_valid = False
            break
    
    return {
        'total_tasks': len(tasks_with_graders),
        'tasks_with_graders': len(tasks_with_graders),
        'minimum_required': 3,
        'all_graders_valid': all_valid,
        'validation_status': 'PASS' if len(tasks_with_graders) >= 3 and all_valid else 'FAIL',
        'tasks': [
            {
                'task_id': entry.task_id,
                'task_name': entry.task_name,
                'grader_class': entry.grader_class_name,
                'difficulty': entry.difficulty
            }
            for entry in tasks_with_graders
        ]
    }


# Quick validation - run on import
if __name__ == '__main__':
    print("GRADER MANIFEST VALIDATION:")
    print("="*60)
    result = validate_grader_setup()
    print(f"Status: {result['validation_status']}")
    print(f"Tasks with graders: {result['tasks_with_graders']}/{result['minimum_required']}")
    for task in result['tasks']:
        print(f"  ✓ {task['task_id']}: {task['grader_class']}")
