#!/usr/bin/env python3
"""
Check if graders are actually callable and functional
Maybe validator tries to instantiate and call them?
"""

import sys

print("="*70)
print("TEST: Can validator actually USE the graders?")
print("="*70)

# Step 1: Import graders
print("\n[1] Importing graders...")
try:
    from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
    print("    SUCCESS: All graders imported")
except Exception as e:
    print(f"    FAIL: {e}")
    sys.exit(1)

# Step 2: Instantiate graders
print("\n[2] Instantiating graders...")
try:
    easy = EasyTaskGrader()
    medium = MediumTaskGrader()
    hard = HardTaskGrader()
    print("    SUCCESS: All graders instantiated")
except Exception as e:
    print(f"    FAIL: {e}")
    sys.exit(1)

# Step 3: Check if graders have .grade() method
print("\n[3] Checking for .grade() method...")
try:
    assert hasattr(easy, 'grade'), "EasyTaskGrader missing grade() method"
    assert hasattr(medium, 'grade'), "MediumTaskGrader missing grade() method"
    assert hasattr(hard, 'grade'), "HardTaskGrader missing grade() method"
    print("    SUCCESS: All graders have grade() method")
except Exception as e:
    print(f"    FAIL: {e}")
    sys.exit(1)

# Step 4: Try calling .grade() method
print("\n[4] Testing .grade() method calls...")
try:
    # Create mock data
    mock_actions = []
    mock_scenario = {"correct_priority_order": ["F001", "F002"]}
    from pm_env.models import Observation, Metrics
    mock_obs = Observation(
        scenario_id="test",
        user_complaints=[],
        metrics=Metrics(churn_rate=0.1, retention_rate=0.9, user_satisfaction=7.0),
        feature_backlog=[],
        constraints={},
        previous_actions=[],
        step_count=0
    )
    
    # Try calling grade on each
    easy_score, easy_details = easy.grade(mock_actions, mock_scenario, mock_obs)
    print(f"    Easy grader returned: score={easy_score}, type={type(easy_score)}")
    
    medium_score, medium_details = medium.grade(mock_actions, mock_scenario, mock_obs)
    print(f"    Medium grader returned: score={medium_score}, type={type(medium_score)}")
    
    hard_score, hard_details = hard.grade(mock_actions, mock_scenario, mock_obs)
    print(f"    Hard grader returned: score={hard_score}, type={type(hard_score)}")
    
    print("    SUCCESS: All graders callable")
except Exception as e:
    print(f"    FAIL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70)
print("RESULT: All grader functionality tests PASSED")
print("If validator still fails, issue is NOT with grader functionality")
print("="*70)
