#!/usr/bin/env python3
"""
Task-Grader Validation Script

Validates that the submission includes at least 3 tasks with working graders.
This script can be run directly to check Phase 2 requirements.

Usage:
    python validate_graders.py
    
Exit Codes:
    0 - All checks passed (3+ tasks with graders)
    1 - Validation failed (fewer than 3 tasks with graders)
    2 - Error during validation
"""

import sys
import json


def validate_tasks_with_graders():
    """
    Validate that we have at least 3 tasks with working graders.
    
    Returns:
        dict with validation results
    """
    try:
        # Import task definitions
        from tasks.task_definitions import TASK_001, TASK_002, TASK_003
        
        # Import graders
        from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
        
        # Map grader names to classes
        grader_map = {
            'EasyTaskGrader': EasyTaskGrader,
            'MediumTaskGrader': MediumTaskGrader,
            'HardTaskGrader': HardTaskGrader
        }
        
        # Check all tasks
        tasks = [TASK_001, TASK_002, TASK_003]
        tasks_with_graders = []
        
        for task in tasks:
            # Check if task has grader_class
            if not hasattr(task, 'grader_class'):
                continue
            
            grader_class_name = task.grader_class
            if not grader_class_name:
                continue
            
            # Check if grader class exists
            grader_class = grader_map.get(grader_class_name)
            if not grader_class:
                continue
            
            # Try to instantiate grader
            try:
                grader = grader_class()
                tasks_with_graders.append({
                    'task_id': task.task_id,
                    'name': task.name,
                    'difficulty': task.difficulty,
                    'grader_class': grader_class_name,
                    'status': 'OK'
                })
                print(f"✅ {task.task_id} ({grader_class_name}): OK")
            except Exception as e:
                print(f"⚠️ {task.task_id} ({grader_class_name}): Failed to instantiate - {e}")
        
        # Check minimum requirement
        has_3_tasks = len(tasks_with_graders) >= 3
        
        result = {
            'validation_status': 'PASS' if has_3_tasks else 'FAIL',
            'tasks_with_graders_count': len(tasks_with_graders),
            'required_count': 3,
            'tasks': tasks_with_graders,
            'message': f"Found {len(tasks_with_graders)}/3 tasks with graders"
        }
        
        if has_3_tasks:
            print(f"\n✅ VALIDATION PASSED: {len(tasks_with_graders)}/3 tasks have working graders")
            return 0, result
        else:
            print(f"\n❌ VALIDATION FAILED: Only {len(tasks_with_graders)}/3 tasks have working graders")
            return 1, result
            
    except ImportError as e:
        print(f"❌ ERROR: Import failed - {e}")
        return 2, {'error': f"Import error: {e}"}
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 2, {'error': str(e)}


if __name__ == "__main__":
    sys.path.insert(0, '.')
    exit_code, result = validate_tasks_with_graders()
    print(f"\n{json.dumps(result, indent=2)}")
    sys.exit(exit_code)
