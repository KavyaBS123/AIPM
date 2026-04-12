#!/usr/bin/env python3
"""
COMPREHENSIVE DIAGNOSTIC - Test every possible way validator might check for graders
Submission #23 Pre-Flight Check
"""

import sys
import traceback

def test_direct_task_imports():
    """Test 1: Can we import tasks directly?"""
    try:
        print("\n" + "="*70)
        print("TEST 1: Direct Task Imports")
        print("="*70)
        
        # Method A: Import from tasks module
        from tasks import list_tasks, get_task, TASK_001, TASK_002, TASK_003
        print("[OK] Can import from tasks module")
        
        # Method B: Import task definitions directly
        from tasks.task_definitions import TASK_001 as T1
        print("[OK] Can import from tasks.task_definitions")
        
        # Method C: Import Pydantic definitions
        from tasks.definitions import TASK_DEFINITIONS
        print("[OK] Can import from tasks.definitions")
        
        return True
    except Exception as e:
        print(f"[FAIL] FAILED: {e}")
        traceback.print_exc()
        return False

def test_task_grader_class_field():
    """Test 2: Do tasks have grader_class field and value?"""
    try:
        print("\n" + "="*70)
        print("TEST 2: Task grader_class Field")
        print("="*70)
        
        from tasks import list_tasks
        tasks = list_tasks()
        
        for task in tasks:
            print(f"\nTask {task.task_id}:")
            print(f"  - task type: {type(task)}")
            print(f"  - task.__dict__: {task.__dict__}")
            print(f"  - hasattr grader_class: {hasattr(task, 'grader_class')}")
            print(f"  - getattr grader_class: {getattr(task, 'grader_class', 'NOT_FOUND')}")
            
            if not hasattr(task, 'grader_class'):
                print(f"✗ Task {task.task_id} missing grader_class!")
                return False
            if not task.grader_class:
                print(f"✗ Task {task.task_id} grader_class is empty!")
                return False
        
        print("\n✓ All 3 tasks have grader_class field with values")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        traceback.print_exc()
        return False

def test_grader_imports():
    """Test 3: Can we import all graders?"""
    try:
        print("\n" + "="*70)
        print("TEST 3: Grader Imports")
        print("="*70)
        
        # Method A: Import from graders package
        from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
        print("✓ Can import graders from graders package")
        
        # Method B: Import from graders.graders module
        from graders.graders import EasyTaskGrader as E1, MediumTaskGrader as M1, HardTaskGrader as H1
        print("✓ Can import graders from graders.graders module")
        
        # Method C: Check module structure
        import graders
        print(f"✓ graders module: {graders}")
        print(f"  - dir(graders): {[x for x in dir(graders) if 'Grader' in x]}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        traceback.print_exc()
        return False

def test_grader_instantiation():
    """Test 4: Can we create grader instances?"""
    try:
        print("\n" + "="*70)
        print("TEST 4: Grader Instantiation")
        print("="*70)
        
        from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
        
        easy = EasyTaskGrader()
        print(f"✓ EasyTaskGrader instantiated: {easy}")
        
        medium = MediumTaskGrader()
        print(f"✓ MediumTaskGrader instantiated: {medium}")
        
        hard = HardTaskGrader()
        print(f"✓ HardTaskGrader instantiated: {hard}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        traceback.print_exc()
        return False

def test_grader_mapping():
    """Test 5: Can we map tasks to graders?"""
    try:
        print("\n" + "="*70)
        print("TEST 5: Task-to-Grader Mapping")
        print("="*70)
        
        from tasks import list_tasks
        from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
        
        grader_map = {
            'EasyTaskGrader': EasyTaskGrader,
            'MediumTaskGrader': MediumTaskGrader,
            'HardTaskGrader': HardTaskGrader
        }
        
        tasks = list_tasks()
        mapped_count = 0
        
        for task in tasks:
            if hasattr(task, 'grader_class'):
                grader_name = task.grader_class
                grader_class = grader_map.get(grader_name)
                print(f"\n{task.task_id}: {task.name}")
                print(f"  - grader_class name: {grader_name}")
                print(f"  - found in map: {grader_class is not None}")
                if grader_class:
                    grader_instance = grader_class()
                    print(f"  - instantiated: {grader_instance}")
                    mapped_count += 1
        
        print(f"\n✓ Successfully mapped {mapped_count}/3 tasks to graders")
        return mapped_count >= 3
    except Exception as e:
        print(f"✗ FAILED: {e}")
        traceback.print_exc()
        return False

def test_environment_graders():
    """Test 6: Are graders accessible via environment?"""
    try:
        print("\n" + "="*70)
        print("TEST 6: Environment Grader Access")
        print("="*70)
        
        from pm_env.environment import ProductManagerEnv
        from scenarios.data import SCENARIOS
        
        # Create environment
        scenario_data = SCENARIOS.get('scenario_1_ecommerce', {})
        env = ProductManagerEnv(scenario_data=scenario_data)
        print(f"✓ Environment created: {env}")
        
        # Check if environment has any grader-related attributes
        env_dir = [x for x in dir(env) if 'grad' in x.lower()]
        print(f"  - Grader-related attributes in env: {env_dir}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        traceback.print_exc()
        return False

def test_grader_manifest():
    """Test 7: Does grader_manifest.py work?"""
    try:
        print("\n" + "="*70)
        print("TEST 7: Grader Manifest")
        print("="*70)
        
        from grader_manifest import (
            get_tasks_with_graders,
            get_grader_count,
            validate_grader_setup,
            GRADER_REGISTRY
        )
        
        print(f"✓ GRADER_REGISTRY: {len(GRADER_REGISTRY)} entries")
        for task_id, entry in GRADER_REGISTRY.items():
            print(f"  - {task_id}: {entry.grader_class_name}")
        
        count = get_grader_count()
        print(f"✓ Grader count: {count}")
        
        tasks = get_tasks_with_graders()
        print(f"✓ Tasks with graders: {len(tasks)}")
        
        result = validate_grader_setup()
        print(f"✓ Validation result: {result['validation_status']}")
        
        return count >= 3 and result['validation_status'] == 'PASS'
    except Exception as e:
        print(f"✗ FAILED: {e}")
        traceback.print_exc()
        return False

def test_api_server_endpoints():
    """Test 8: Do API server endpoints exist?"""
    try:
        print("\n" + "="*70)
        print("TEST 8: API Server Endpoints")
        print("="*70)
        
        from api.server import create_app
        from fastapi.testclient import TestClient
        
        app = create_app()
        client = TestClient(app)
        
        # Test /validate
        resp = client.get('/validate')
        print(f"✓ GET /validate: {resp.status_code}")
        data = resp.json()
        print(f"  - validation_status: {data.get('validation_status')}")
        print(f"  - tasks_with_graders_count: {data.get('tasks_with_graders_count')}")
        
        # Test /tasks
        resp = client.get('/tasks')
        print(f"✓ GET /tasks: {resp.status_code}")
        data = resp.json()
        print(f"  - tasks returned: {len(data)}")
        for task in data:
            print(f"    - {task.get('task_id')}: has grader_class={bool(task.get('grader_class'))}")
        
        # Test /manifest
        resp = client.get('/manifest')
        print(f"✓ GET /manifest: {resp.status_code}")
        data = resp.json()
        print(f"  - validation_status: {data.get('validation_status')}")
        print(f"  - tasks_with_graders: {data.get('tasks_with_graders')}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic tests"""
    print("\n" + "="*70)
    print("COMPREHENSIVE DIAGNOSTIC - Submission #23 Pre-Flight")
    print("="*70)
    
    results = []
    results.append(("Direct Task Imports", test_direct_task_imports()))
    results.append(("Task grader_class Field", test_task_grader_class_field()))
    results.append(("Grader Imports", test_grader_imports()))
    results.append(("Grader Instantiation", test_grader_instantiation()))
    results.append(("Task-to-Grader Mapping", test_grader_mapping()))
    results.append(("Environment Graders", test_environment_graders()))
    results.append(("Grader Manifest", test_grader_manifest()))
    results.append(("API Server Endpoints", test_api_server_endpoints()))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓✓✓ ALL SYSTEMS GO - SAFE TO SUBMIT #23 ✓✓✓")
        return 0
    else:
        print(f"\n✗✗✗ {total - passed} TEST(S) FAILED - DO NOT SUBMIT ✗✗✗")
        return 1

if __name__ == '__main__':
    sys.exit(main())
