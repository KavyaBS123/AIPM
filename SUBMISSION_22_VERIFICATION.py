"""
COMPREHENSIVE PRE-SUBMISSION VERIFICATION FOR SUBMISSION #22

This script tests EVERYTHING the validator might check.
Exit code 0 = SAFE TO SUBMIT
Exit code 1 = SOMETHING IS WRONG
"""

import sys
import traceback

def test_import_tasks():
    """Test 1: Can we import tasks?"""
    try:
        from tasks import list_tasks, get_task
        print('✓ Test 1: Import tasks module - PASS')
        return True
    except Exception as e:
        print(f'✗ Test 1: Import tasks module - FAIL: {e}')
        traceback.print_exc()
        return False

def test_tasks_have_grader_class():
    """Test 2: Do all tasks have grader_class field?"""
    try:
        from tasks import list_tasks
        tasks = list_tasks()
        
        if len(tasks) != 3:
            print(f'✗ Test 2: Expected 3 tasks, got {len(tasks)} - FAIL')
            return False
        
        for task in tasks:
            if not hasattr(task, 'grader_class'):
                print(f'✗ Test 2: Task {task.task_id} missing grader_class - FAIL')
                return False
            if not task.grader_class or not isinstance(task.grader_class, str):
                print(f'✗ Test 2: Task {task.task_id} has invalid grader_class - FAIL')
                return False
        
        print('✓ Test 2: All 3 tasks have grader_class - PASS')
        return True
    except Exception as e:
        print(f'✗ Test 2: Check grader_class field - FAIL: {e}')
        traceback.print_exc()
        return False

def test_import_graders():
    """Test 3: Can we import all grader classes?"""
    try:
        from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
        print('✓ Test 3: Import all grader classes - PASS')
        return True
    except Exception as e:
        print(f'✗ Test 3: Import grader classes - FAIL: {e}')
        traceback.print_exc()
        return False

def test_can_instantiate_graders():
    """Test 4: Can we instantiate all graders?"""
    try:
        from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
        
        easy = EasyTaskGrader()
        medium = MediumTaskGrader()
        hard = HardTaskGrader()
        
        print('✓ Test 4: Instantiate all grader classes - PASS')
        return True
    except Exception as e:
        print(f'✗ Test 4: Instantiate graders - FAIL: {e}')
        traceback.print_exc()
        return False

def test_validation_logic():
    """Test 5: Does the validation logic count 3 tasks with graders?"""
    try:
        from tasks import list_tasks
        from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
        
        tasks = list_tasks()
        grader_map = {
            'EasyTaskGrader': EasyTaskGrader,
            'MediumTaskGrader': MediumTaskGrader,
            'HardTaskGrader': HardTaskGrader
        }
        
        tasks_with_graders_count = 0
        for task in tasks:
            if hasattr(task, 'grader_class') and task.grader_class:
                grader_class = grader_map.get(task.grader_class)
                if grader_class:
                    try:
                        grader = grader_class()
                        tasks_with_graders_count += 1
                    except:
                        pass
        
        if tasks_with_graders_count >= 3:
            print(f'✓ Test 5: Found {tasks_with_graders_count}/3 tasks with graders - PASS')
            return True
        else:
            print(f'✗ Test 5: Only found {tasks_with_graders_count}/3 tasks with graders - FAIL')
            return False
    except Exception as e:
        print(f'✗ Test 5: Validation logic - FAIL: {e}')
        traceback.print_exc()
        return False

def test_api_endpoint():
    """Test 6: Does the /validate API endpoint return PASS?"""
    try:
        from api.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get('/validate')
        
        if response.status_code != 200:
            print(f'✗ Test 6: API returned status {response.status_code} - FAIL')
            return False
        
        data = response.json()
        if data.get('validation_status') != 'PASS':
            print(f'✗ Test 6: Validation status is {data.get("validation_status")} - FAIL')
            return False
        
        if data.get('tasks_with_graders_count', 0) < 3:
            print(f'✗ Test 6: Only {data.get("tasks_with_graders_count")}/3 tasks with graders - FAIL')
            return False
        
        print('✓ Test 6: /validate API endpoint returns PASS - PASS')
        return True
    except Exception as e:
        print(f'✗ Test 6: API endpoint test - FAIL: {e}')
        traceback.print_exc()
        return False

def main():
    print('=' * 70)
    print('COMPREHENSIVE PRE-SUBMISSION VERIFICATION (Submission #22)')
    print('=' * 70)
    print()
    
    results = [
        test_import_tasks(),
        test_tasks_have_grader_class(),
        test_import_graders(),
        test_can_instantiate_graders(),
        test_validation_logic(),
        test_api_endpoint(),
    ]
    
    print()
    print('=' * 70)
    if all(results):
        print('✓✓✓ ALL TESTS PASSED - SAFE TO SUBMIT #22 ✓✓✓')
        print('=' * 70)
        return 0
    else:
        failed_count = sum(1 for r in results if not r)
        print(f'✗✗✗ {failed_count}/{len(results)} TESTS FAILED - DO NOT SUBMIT ✗✗✗')
        print('=' * 70)
        return 1

if __name__ == '__main__':
    sys.exit(main())
