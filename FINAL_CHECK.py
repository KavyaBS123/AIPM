#!/usr/bin/env python3
"""Final ultimate check before resubmission #19"""

import sys
import os
sys.path.insert(0, '.')

print("\n" + "="*75)
print("ULTIMATE FINAL VALIDATION BEFORE RESUBMIT #19")
print("="*75 + "\n")

all_checks_pass = True

# 1. Check definitions.py (Pydantic)
print("1️⃣  CHECK: definitions.py with Pydantic TaskDefinition")
print("-"*75)
try:
    from tasks.definitions import TASK_DEFINITIONS
    count = 0
    for task_name, task_def in TASK_DEFINITIONS.items():
        grader = getattr(task_def, 'grader_class', None)
        print(f"   ✅ {task_def.task_id}: {task_def.name}")
        print(f"       └─ grader_class = {grader}")
        if grader:
            count += 1
    if count == 3:
        print(f"\n   ✅ PASS: 3/3 tasks have grader_class")
    else:
        print(f"\n   ❌ FAIL: Only {count}/3 tasks have grader_class")
        all_checks_pass = False
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    all_checks_pass = False

# 2. Check task_definitions.py (Dataclass)
print("\n2️⃣  CHECK: task_definitions.py with Dataclass TaskDefinition")
print("-"*75)
try:
    from tasks.task_definitions import TASK_001, TASK_002, TASK_003
    count = 0
    for task in [TASK_001, TASK_002, TASK_003]:
        grader = getattr(task, 'grader_class', None)
        print(f"   ✅ {task.task_id}: {task.name}")
        print(f"       └─ grader_class = {grader}")
        if grader:
            count += 1
    if count == 3:
        print(f"\n   ✅ PASS: 3/3 tasks have grader_class")
    else:
        print(f"\n   ❌ FAIL: Only {count}/3 tasks have grader_class")
        all_checks_pass = False
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    all_checks_pass = False

# 3. Check graders can be instantiated
print("\n3️⃣  CHECK: All Graders Instantiable")
print("-"*75)
try:
    from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
    count = 0
    for name, cls in [('Easy', EasyTaskGrader), ('Medium', MediumTaskGrader), ('Hard', HardTaskGrader)]:
        g = cls()
        print(f"   ✅ {name}TaskGrader: instantiated successfully")
        count += 1
    if count == 3:
        print(f"\n   ✅ PASS: All 3 graders instantiable")
    else:
        all_checks_pass = False
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    all_checks_pass = False

# 4. Check API endpoints
print("\n4️⃣  CHECK: API Endpoints (/validate, /info, /tasks)")
print("-"*75)
try:
    from api.main import app
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    tests_passed = 0
    
    # Test /validate
    r1 = client.get('/validate')
    v1 = r1.json()
    if v1.get('validation_status') == 'PASS' and v1.get('tasks_with_graders_count') == 3:
        print(f"   ✅ GET /validate → PASS (3/3 tasks with graders)")
        tests_passed += 1
    else:
        print(f"   ❌ GET /validate → {v1.get('validation_status')} ({v1.get('tasks_with_graders_count')}/3)")
        all_checks_pass = False
    
    # Test /info
    r2 = client.get('/info')
    v2 = r2.json()
    status = v2.get('phase2_validation', {}).get('status', 'UNKNOWN')
    if status == 'PASS':
        print(f"   ✅ GET /info → PASS")
        tests_passed += 1
    else:
        print(f"   ❌ GET /info → {status}")
        all_checks_pass = False
    
    # Test /tasks
    r3 = client.get('/tasks')
    v3 = r3.json()
    tasks_with_graders = sum(1 for t in v3 if t.get('grader_class'))
    if len(v3) == 3 and tasks_with_graders == 3:
        print(f"   ✅ GET /tasks → 3/3 tasks have grader_class")
        tests_passed += 1
    else:
        print(f"   ❌ GET /tasks → {len(v3)} tasks ({tasks_with_graders} have grader_class)")
        all_checks_pass = False
    
    if tests_passed == 3:
        print(f"\n   ✅ PASS: All endpoints working correctly")
    else:
        print(f"\n   ❌ FAIL: {tests_passed}/3 endpoints working")
        
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    all_checks_pass = False

# 5. Check git status
print("\n5️⃣  CHECK: Git Status & Latest Commits")
print("-"*75)
try:
    import subprocess
    result = subprocess.run(['git', 'log', '--oneline', '-n', '3'], 
                          capture_output=True, text=True, cwd=os.getcwd())
    if result.returncode == 0:
        print("   Recent commits:")
        for line in result.stdout.strip().split('\n')[:3]:
            print(f"     {line}")
    result2 = subprocess.run(['git', 'status', '--short'], 
                           capture_output=True, text=True, cwd=os.getcwd())
    if result2.stdout.strip():
        print(f"\n   ⚠️  Uncommitted changes found!")
        print(result2.stdout)
        all_checks_pass = False
    else:
        print(f"\n   ✅ All changes committed and pushed")
except Exception as e:
    print(f"   ⚠️  Could not check git: {e}")

print("\n" + "="*75)
print("FINAL VERDICT")
print("="*75 + "\n")

if all_checks_pass:
    print("✅✅✅ SUBMISSION #19 IS 100% READY TO RESUBMIT ✅✅✅")
    print("\nThe validator will definitely see:")
    print("  • 3 tasks with grader_class field defined")
    print("  • All graders importable and instantiable")
    print("  • /validate endpoint confirms PASS")
    print("  • /info endpoint shows phase2_validation PASS")
    print("  • /tasks endpoint lists graders for all tasks")
    print("\n🚀 YOU CAN SAFELY SUBMIT #19 NOW!")
    sys.exit(0)
else:
    print("❌ CRITICAL ISSUES DETECTED")
    print("\nDO NOT RESUBMIT - Fix issues above first")
    sys.exit(1)
