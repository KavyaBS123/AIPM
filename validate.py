#!/usr/bin/env python
"""Validation script to check environment setup."""

import sys
import json
from pathlib import Path

# Add project root
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def check_imports() -> bool:
    """Check if all required modules can be imported."""
    print("✓ Checking imports...")
    
    required_modules = [
        ("fastapi", "fastapi"),
        ("pydantic", "pydantic"),
        ("requests", "requests"),
        ("openai", "openai"),
    ]
    
    all_ok = True
    for module_name, import_name in required_modules:
        try:
            __import__(import_name)
            print(f"  ✓ {module_name}")
        except ImportError as e:
            print(f"  ✗ {module_name}: {e}")
            all_ok = False
    
    return all_ok


def check_project_structure() -> bool:
    """Check if all required directories and files exist."""
    print("\n✓ Checking project structure...")
    
    required_paths = [
        "env/__init__.py",
        "env/environment.py",
        "models/__init__.py",
        "models/schemas.py",
        "scenarios/__init__.py",
        "scenarios/data.py",
        "tasks/__init__.py",
        "tasks/definitions.py",
        "graders/__init__.py",
        "graders/graders.py",
        "api/__init__.py",
        "api/server.py",
        "inference.py",
        "main.py",
        "config.py",
        "requirements.txt",
        "Dockerfile",
        "README.md",
    ]
    
    all_ok = True
    for path in required_paths:
        full_path = project_root / path
        if full_path.exists():
            print(f"  ✓ {path}")
        else:
            print(f"  ✗ {path} - NOT FOUND")
            all_ok = False
    
    return all_ok


def check_module_exports() -> bool:
    """Check if modules export expected items."""
    print("\n✓ Checking module exports...")
    
    all_ok = True
    
    # Check models
    try:
        from models import Action, ActionType, Observation, Reward, Feature
        print("  ✓ models (Action, ActionType, Observation, Reward, Feature)")
    except ImportError as e:
        print(f"  ✗ models: {e}")
        all_ok = False
    
    # Check environment
    try:
        from env import create_environment, ProductManagerEnvironment
        print("  ✓ env (create_environment, ProductManagerEnvironment)")
    except ImportError as e:
        print(f"  ✗ env: {e}")
        all_ok = False
    
    # Check scenarios
    try:
        from scenarios import get_scenario, list_scenarios
        print("  ✓ scenarios (get_scenario, list_scenarios)")
    except ImportError as e:
        print(f"  ✗ scenarios: {e}")
        all_ok = False
    
    # Check tasks
    try:
        from tasks import get_task_definition, list_tasks
        print("  ✓ tasks (get_task_definition, list_tasks)")
    except ImportError as e:
        print(f"  ✗ tasks: {e}")
        all_ok = False
    
    # Check graders
    try:
        from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
        print("  ✓ graders (EasyTaskGrader, MediumTaskGrader, HardTaskGrader)")
    except ImportError as e:
        print(f"  ✗ graders: {e}")
        all_ok = False
    
    # Check API
    try:
        from api import create_app
        print("  ✓ api (create_app)")
    except ImportError as e:
        print(f"  ✗ api: {e}")
        all_ok = False
    
    return all_ok


def check_environment_creation() -> bool:
    """Test creating an environment."""
    print("\n✓ Testing environment creation...")
    
    try:
        from env import create_environment
        from scenarios import list_scenarios
        from tasks import list_tasks
        
        # List available scenarios
        scenarios = list_scenarios()
        print(f"  ✓ Available scenarios: {len(scenarios)}")
        for s in scenarios:
            print(f"    - {s}")
        
        # List available tasks
        tasks = list_tasks()
        print(f"  ✓ Available tasks: {len(tasks)}")
        for t in tasks:
            print(f"    - {t}")
        
        # Create environment
        env = create_environment(
            scenario_key="scenario_1_ecommerce",
            task_id="task_001",
            seed=42
        )
        print(f"  ✓ Environment created")
        
        # Reset
        obs = env.reset()
        print(f"  ✓ Environment reset successful")
        
        # Check observation
        assert hasattr(obs, "step"), "Missing 'step' in observation"
        assert hasattr(obs, "metrics_summary"), "Missing 'metrics_summary' in observation"
        print(f"  ✓ Observation structure valid")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_api_server() -> bool:
    """Test API server creation."""
    print("\n✓ Testing API server creation...")
    
    try:
        from api import create_app
        
        app = create_app()
        print(f"  ✓ FastAPI app created")
        
        # Check endpoints
        routes = [r.path for r in app.routes]
        required_routes = ["/reset", "/step", "/state", "/health", "/info"]
        
        for route in required_routes:
            if route in routes:
                print(f"    ✓ {route}")
            else:
                print(f"    ✗ {route} - missing")
        
        return all(r in routes for r in required_routes)
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_inference_agent() -> bool:
    """Test inference agent creation."""
    print("\n✓ Testing inference agent...")
    
    try:
        from inference import PMInferenceAgent
        
        # Note: We don't actually call it without API key,
        # but we can check it instantiates
        agent = PMInferenceAgent(
            api_key="test-key",
            model="gpt-4o-mini"
        )
        print(f"  ✓ PMInferenceAgent created")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_checks() -> int:
    """Run all validation checks."""
    print("=" * 80)
    print("🔍 Environment Validation")
    print("=" * 80)
    
    checks = [
        ("Imports", check_imports),
        ("Project Structure", check_project_structure),
        ("Module Exports", check_module_exports),
        ("Environment Creation", check_environment_creation),
        ("API Server", check_api_server),
        ("Inference Agent", check_inference_agent),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 Summary")
    print("=" * 80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All checks passed! Environment is ready.")
        return 0
    else:
        print("\n⚠️  Some checks failed. See above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_checks())
