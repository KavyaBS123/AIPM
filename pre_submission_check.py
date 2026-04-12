#!/usr/bin/env python3
"""
Comprehensive pre-submission validation script.
Catches all potential errors BEFORE submission.
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def check_port_consistency():
    """Check that all port references are consistent."""
    print("\n=== PORT CONSISTENCY CHECK ===")
    
    errors = []
    ports_found = {}
    
    # Check main.py
    with open("main.py", encoding="utf-8") as f:
        content = f.read()
        port_matches = re.findall(r'port\s*=\s*(\d+)|"(\d+)"', content, re.IGNORECASE)
        if port_matches:
            for match in port_matches:
                port = match[0] or match[1]
                ports_found[f"main.py"] = port
                print(f"  ✓ main.py: port {port}")
    
    # Check Dockerfile
    with open("Dockerfile", encoding="utf-8") as f:
        content = f.read()
        # Check EXPOSE
        expose_matches = re.findall(r'EXPOSE\s+(\d+)', content)
        if expose_matches:
            for port in expose_matches:
                ports_found[f"Dockerfile EXPOSE"] = port
                print(f"  ✓ Dockerfile EXPOSE: {port}")
        
        # Check healthcheck port
        healthcheck_matches = re.findall(r'PORT="\$\{PORT:-(\d+)\}', content)
        if healthcheck_matches:
            for port in healthcheck_matches:
                ports_found[f"Dockerfile HEALTHCHECK"] = port
                print(f"  ✓ Dockerfile HEALTHCHECK: {port}")
    
    # Check inference.py
    with open("inference.py", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        api_port_matches = re.findall(r'API_BASE_URL.*:(\d+)', content)
        if api_port_matches:
            for port in api_port_matches:
                ports_found[f"inference.py API"] = port
                print(f"  ✓ inference.py API: {port}")
    
    # Verify consistency
    unique_ports = set(ports_found.values())
    if len(unique_ports) > 1:
        errors.append(f"CRITICAL: Port mismatch! Found ports: {ports_found}")
        print(f"  ✗ CRITICAL: Port mismatch detected!")
        for component, port in ports_found.items():
            print(f"    - {component}: {port}")
    else:
        port = unique_ports.pop() if unique_ports else "8000"
        print(f"  ✓ All ports consistent: {port}")
    
    return errors


def check_healthcheck_endpoints():
    """Check that healthcheck endpoint exists."""
    print("\n=== HEALTHCHECK ENDPOINT CHECK ===")
    
    errors = []
    
    # Check api/server.py for /health endpoint
    with open("api/server.py") as f:
        content = f.read()
        if '"/health"' in content or "'/health'" in content:
            print("  ✓ /health endpoint defined in api/server.py")
        else:
            errors.append("ERROR: /health endpoint not found in api/server.py")
            print("  ✗ /health endpoint not found!")
    
    return errors


def check_inference_py_syntax():
    """Check inference.py for syntax errors and import issues."""
    print("\n=== INFERENCE.PY VALIDATION ===")
    
    errors = []
    
    # Check syntax
    try:
        with open("inference.py", encoding="utf-8", errors="ignore") as f:
            code = f.read()
            compile(code, "inference.py", "exec")
        print("  ✓ inference.py syntax is valid")
    except SyntaxError as e:
        errors.append(f"SYNTAX ERROR in inference.py: {e}")
        print(f"  ✗ Syntax error: {e}")
    
    # Check imports
    try:
        import inference
        print("  ✓ inference.py imports successfully")
    except ImportError as e:
        errors.append(f"IMPORT ERROR in inference.py: {e}")
        print(f"  ✗ Import error: {e}")
    
    # Check required variables
    try:
        import inference
        required_vars = ['API_BASE_URL', 'MODEL_NAME', 'MAX_STEPS']
        for var in required_vars:
            if hasattr(inference, var):
                value = getattr(inference, var)
                print(f"  ✓ {var} = {value}")
            else:
                errors.append(f"MISSING: {var} not defined in inference.py")
                print(f"  ✗ Missing {var}")
    except Exception as e:
        errors.append(f"ERROR checking variables: {e}")
    
    return errors


def test_inference_execution():
    """Run a quick inference test."""
    print("\n=== INFERENCE EXECUTION TEST ===")
    
    errors = []
    
    try:
        result = subprocess.run(
            [sys.executable, "inference.py", "test_validation"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("  ✓ inference.py executed successfully")
            
            # Check output format
            output = result.stdout
            if "[START]" in output and "[STEP]" in output and "[END]" in output:
                print("  ✓ Output format is correct ([START]/[STEP]/[END])")
            else:
                errors.append("ERROR: Output format incorrect")
                print("  ✗ Output format incorrect")
        else:
            errors.append(f"EXECUTION ERROR: {result.stderr}")
            print(f"  ✗ Execution failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        errors.append("ERROR: inference.py timed out (>30s)")
        print("  ✗ Timeout (>30s)")
    except Exception as e:
        errors.append(f"ERROR: {e}")
        print(f"  ✗ Error: {e}")
    
    return errors


def check_dockerfile_validity():
    """Check Dockerfile for basic validity."""
    print("\n=== DOCKERFILE VALIDATION ===")
    
    errors = []
    
    try:
        with open("Dockerfile", encoding="utf-8") as f:
            content = f.read()
            
            # Check required directives
            checks = [
                ("FROM", "Base image"),
                ("WORKDIR", "Working directory"),
                ("COPY", "Copy files"),
                ("RUN", "Run commands"),
                ("EXPOSE", "Expose port"),
                ("CMD", "Startup command"),
                ("HEALTHCHECK", "Health check"),
            ]
            
            for directive, description in checks:
                if directive in content:
                    print(f"  ✓ {directive}: {description}")
                else:
                    errors.append(f"MISSING: {directive} ({description})")
                    print(f"  ✗ Missing {directive}")
    except Exception as e:
        errors.append(f"ERROR reading Dockerfile: {e}")
        print(f"  ✗ Error: {e}")
    
    return errors


def check_git_status():
    """Check git status for uncommitted changes."""
    print("\n=== GIT STATUS CHECK ===")
    
    errors = []
    
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            if result.stdout.strip():
                errors.append(f"WARNING: Uncommitted changes exist")
                print(f"  ⚠ Uncommitted changes found:")
                for line in result.stdout.strip().split("\n"):
                    print(f"    {line}")
            else:
                print("  ✓ All changes committed")
        else:
            errors.append("ERROR: Could not check git status")
            print("  ✗ Git error")
    except Exception as e:
        errors.append(f"ERROR: {e}")
    
    return errors


def main():
    """Run all checks."""
    print("=" * 60)
    print("PRE-SUBMISSION VALIDATION")
    print("=" * 60)
    
    all_errors = []
    
    # Run all checks
    all_errors.extend(check_port_consistency())
    all_errors.extend(check_healthcheck_endpoints())
    all_errors.extend(check_inference_py_syntax())
    all_errors.extend(check_dockerfile_validity())
    all_errors.extend(test_inference_execution())
    all_errors.extend(check_git_status())
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    if all_errors:
        print(f"\n❌ FOUND {len(all_errors)} ISSUES:\n")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")
        print("\n⚠️  DO NOT SUBMIT - Fix these errors first!")
        return 1
    else:
        print("\n✅ ALL CHECKS PASSED!")
        print("✅ Ready to submit!\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
