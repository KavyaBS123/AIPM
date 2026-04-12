#!/usr/bin/env python3
"""
FINAL VERIFICATION: Test that validator can find graders at all levels
Used to verify Submission #24 fix
"""

import yaml
import sys

print("=" * 80)
print("FINAL GRADER DISCOVERY VERIFICATION - SUBMISSION #24")
print("=" * 80)

try:
    # Load openenv.yaml
    with open("openenv.yaml", "r") as f:
        spec = yaml.safe_load(f)
    
    print("\n✅ [1] openenv.yaml loaded successfully")
    
    # Check top-level grading section
    if "grading" not in spec:
        raise ValueError("❌ Top-level 'grading' section not found")
    
    grading = spec["grading"]
    graders_at_top = grading.get("graders", [])
    print(f"✅ [2] Top-level grading section found with {len(graders_at_top)} graders")
    
    if len(graders_at_top) != 3:
        raise ValueError(f"❌ Expected 3 graders at top-level, got {len(graders_at_top)}")
    
    for g in graders_at_top:
        print(f"   - {g['task']}: {g['grader_class']}")
    
    # Check task-level grader specifications
    if "info" not in spec or "tasks" not in spec["info"]:
        raise ValueError("❌ info.tasks section not found")
    
    tasks = spec["info"]["tasks"]
    print(f"\n✅ [3] Task definitions found in info.tasks: {len(tasks)} tasks")
    
    tasks_with_graders = 0
    for task in tasks:
        task_id = task.get("id")
        grader_class = task.get("grader_class")
        
        if grader_class:
            tasks_with_graders += 1
            print(f"   ✅ {task_id}: {grader_class}")
        else:
            print(f"   ❌ {task_id}: NO grader_class specified")
    
    if tasks_with_graders != 3:
        raise ValueError(f"❌ Only {tasks_with_graders}/3 tasks have grader_class specified")
    
    print(f"\n✅ [4] All 3 tasks have grader_class specified")
    
    # Verify grader classes are actually defined
    from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
    print(f"✅ [5] All grader classes are importable and functional")
    
    # Final verification: map YAML specs to actual classes
    expected_mappings = {
        "task_001": "EasyTaskGrader",
        "task_002": "MediumTaskGrader",
        "task_003": "HardTaskGrader"
    }
    
    print(f"\n✅ [6] Validating task-to-grader mappings:")
    for task in tasks:
        task_id = task.get("id")
        yaml_grader = task.get("grader_class")
        expected = expected_mappings.get(task_id)
        
        if yaml_grader != expected:
            raise ValueError(f"❌ {task_id}: YAML shows {yaml_grader}, expected {expected}")
        
        print(f"   ✅ {task_id} → {yaml_grader}")
    
    print("\n" + "=" * 80)
    print("🎉 SUCCESS: YAML is correctly configured for validator!")
    print("=" * 80)
    print("\nConfiguration verified:")
    print("✅ Top-level grading section: 3 graders mapped")
    print("✅ Task definitions: All 3 have grader_class field")
    print("✅ Grader classes: All importable")
    print("✅ Task-to-grader mapping: All 3 correct")
    print("\nReady for Submission #24 ✅")
    
except Exception as e:
    print(f"\n❌ VERIFICATION FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
