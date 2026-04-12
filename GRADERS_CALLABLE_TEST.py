#!/usr/bin/env python3
"""
CRITICAL TEST: Verify graders ARE callable and have proper interface
Used for debugging validator rejection
"""

import sys
import inspect

print("=" * 70)
print("GRADERS CALLABLE TEST")
print("=" * 70)

try:
    from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
    print("\n✅ [1] All graders imported successfully")
    
    # Create instances
    easy = EasyTaskGrader()
    medium = MediumTaskGrader()
    hard = HardTaskGrader()
    print("✅ [2] All graders instantiated successfully")
    
    # Verify they have grade() method
    for name, grader in [("Easy", easy), ("Medium", medium), ("Hard", hard)]:
        if not hasattr(grader, 'grade'):
            raise ValueError(f"{name} grader missing grade() method")
        if not callable(grader.grade):
            raise ValueError(f"{name} grader.grade is not callable")
        
        # Get signature
        sig = inspect.signature(grader.grade)
        params = list(sig.parameters.keys())
        print(f"   ✅ {name}: grade{sig}")
    
    print("\n✅ [3] All graders have callable grade() method with proper signature")
    
    # Check if they're Pydantic BaseModel or plain classes
    print("\n✅ [4] Grader types:")
    for name, grader in [("Easy", easy), ("Medium", medium), ("Hard", hard)]:
        print(f"   - {name}: {type(grader).__name__} (base: {type(grader).__bases__})")
    
    print("\n" + "=" * 70)
    print("RESULT: ✅ ALL TESTS PASSED - Graders are callable and properly configured")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
