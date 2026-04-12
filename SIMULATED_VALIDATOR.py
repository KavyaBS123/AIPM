#!/usr/bin/env python3
"""
Simulated Meta Hackathon Validator - Checking for graders
This script tests various ways the validator might check if graders are present
"""

import sys
import yaml
import os

def test_openenv_yaml_graders():
    """Check if openenv.yaml specifies graders"""
    try:
        print("\n[VALIDATOR CHECK 1] openenv.yaml graders specification")
        print("-" * 70)
        
        with open('openenv.yaml', 'r') as f:
            spec = yaml.safe_load(f)
        
        graders = spec.get('grading', {}).get('graders', [])
        print(f"Found {len(graders)} graders in openenv.yaml:")
        for grader in graders:
            print(f"  - Task {grader.get('task')}: {grader.get('type')}")
        
        if len(graders) >= 3:
            print("[OK] At least 3 graders specified in openenv.yaml")
            return True
        else:
            print("[FAIL] Less than 3 graders in openenv.yaml")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def test_graders_module_exists():
    """Check if graders module exists and is importable"""
    try:
        print("\n[VALIDATOR CHECK 2] Graders module importability")
        print("-" * 70)
        
        if not os.path.exists('graders/graders.py'):
            print("[FAIL] graders/graders.py does not exist")
            return False
        print("[OK] graders/graders.py exists")
        
        if not os .path.exists('graders/__init__.py'):
            print("[FAIL] graders/__init__.py does not exist")
            return False
        print("[OK] graders/__init__.py exists")
        
        # Try importing
        from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
        print("[OK] Successfully imported all 3 grader classes")
        return True
    except Exception as e:
        print(f"[FAIL] {e}")
        return False

def test_tasks_have_graders():
    """Check if task definitions reference graders"""
    try:
        print("\n[VALIDATOR CHECK 3] Tasks reference graders")
        print("-" * 70)
        
        from tasks import list_tasks
        
        tasks = list_tasks()
        tasks_with_graders = 0
        
        for task in tasks:
            has_grader = hasattr(task, 'grader_class') and task.grader_class
            status = "YES" if has_grader else "NO"
            print(f"  Task {task.task_id}: has grader_class = {status}")
            if has_grader:
                tasks_with_graders += 1
        
        print(f"\nResult: {tasks_with_graders}/3 tasks have grader_class")
        
        if tasks_with_graders >= 3:
            print("[OK] At least 3 tasks have grader_class")
            return True
        else:
            print(f"[FAIL] Only {tasks_with_graders}/3 tasks have grader_class")
            return False
    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        return False

def test_grader_manifest_count():
    """Check if grader_manifest reports 3 graders"""
    try:
        print("\n[VALIDATOR CHECK 4] Grader manifest count")
        print("-" * 70)
        
        from grader_manifest import get_grader_count
        
        count = get_grader_count()
        print(f"get_grader_count() returned: {count}")
        
        if count >= 3:
            print(f"[OK] Grader manifest reports {count} graders")
            return True
        else:
            print(f"[FAIL] Grader manifest reports only {count} graders")
            return False
    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*70)
    print("SIMULATED META HACKATHON VALIDATOR")
    print("Checking: 'Not enough tasks with graders'")
    print("="*70)
    
    os.chdir('c:\\Users\\Kavya\\OneDrive\\Desktop\\AIPM')
    
    results = []
    results.append(("openenv.yaml graders", test_openenv_yaml_graders()))
    results.append(("Graders module exists", test_graders_module_exists()))
    results.append(("Tasks have graders", test_tasks_have_graders()))
    results.append(("Grader manifest count", test_grader_manifest_count()))
    
    print("\n" + "="*70)
    print("VALIDATION RESULTS")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")
    
    print()
    if passed == total:
        print("[SUCCESS] All validator checks passed!")
        print("Validator should NOT return 'Not enough tasks with graders'")
        return 0
    else:
        print(f"[FAILURE] {total - passed} check(s) failed")
        print("Validator WOULD return 'Not enough tasks with graders'")
        return 1

if __name__ == '__main__':
    sys.exit(main())
