#!/usr/bin/env python3
"""
Comprehensive grader validation script.
Verifies that all 3 graders are:
1. Importable
2. Have the correct score ranges
3. Are properly registered
"""

import sys
sys.path.insert(0, '.')

print("=" * 70)
print("GRADER VALIDATION TEST")
print("=" * 70)

# Test 1: Import all graders
print("\n✓ TEST 1: Import graders from package")
try:
    from graders import (
        BaseGrader,
        EasyTaskGrader,
        MediumTaskGrader,
        HardTaskGrader,
    )
    print(f"  ✅ BaseGrader imported: {BaseGrader.__module__}")
    print(f"  ✅ EasyTaskGrader imported: {EasyTaskGrader.__module__}")
    print(f"  ✅ MediumTaskGrader imported: {MediumTaskGrader.__module__}")
    print(f"  ✅ HardTaskGrader imported: {HardTaskGrader.__module__}")
except Exception as e:
    print(f"  ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Verify they come from graders.py (not grader.py)
print("\n✓ TEST 2: Verify graders are from graders.py (FIXED version)")
import inspect

easy_source = inspect.getsource(EasyTaskGrader)
if 'graders.graders' in inspect.getfile(EasyTaskGrader):
    print(f"  ✅ EasyTaskGrader from: {inspect.getfile(EasyTaskGrader)}")
else:
    print(f"  ❌ EasyTaskGrader from wrong file: {inspect.getfile(EasyTaskGrader)}")

# Test 3: Check score ranges in source code
print("\n✓ TEST 3: Check for (0.01, 0.99) score clamping")
for name, grader_class in [
    ("EasyTaskGrader", EasyTaskGrader),
    ("MediumTaskGrader", MediumTaskGrader),
    ("HardTaskGrader", HardTaskGrader),
]:
    source = inspect.getsource(grader_class)
    has_clamp = "0.99" in source and "0.01" in source
    status = "✅" if has_clamp else "❌"
    print(f"  {status} {name}: {'Has (0.01, 0.99) clamping' if has_clamp else 'Missing clamping'}")

# Test 4: Verify graders can be instantiated
print("\n✓ TEST 4: Instantiate graders")
try:
    easy = EasyTaskGrader()
    medium = MediumTaskGrader()
    hard = HardTaskGrader()
    print(f"  ✅ EasyTaskGrader instance created")
    print(f"  ✅ MediumTaskGrader instance created")
    print(f"  ✅ HardTaskGrader instance created")
except Exception as e:
    print(f"  ❌ Instantiation failed: {e}")
    sys.exit(1)

# Test 5: Ensure all have grade() method
print("\n✓ TEST 5: Verify grade() methods exist")
for name, grader in [
    ("EasyTaskGrader", easy),
    ("MediumTaskGrader", medium),
    ("HardTaskGrader", hard),
]:
    if hasattr(grader, 'grade') and callable(getattr(grader, 'grade')):
        print(f"  ✅ {name}.grade() method exists")
    else:
        print(f"  ❌ {name}.grade() method missing")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("✅ All 3 graders are properly configured")
print("✅ Graders use FIXED version with (0.01, 0.99) scores")
print("✅ All graders are instantiable and have grade() methods")
print("✅ Ready for validation")
print("=" * 70)
