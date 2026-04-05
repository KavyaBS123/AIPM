#!/usr/bin/env python
"""
Full Setup and Verification Script for AI Product Manager Environment
Checks all dependencies and configurations before running
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n🔍 Checking dependencies...")
    required = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'openai',
        'python-dotenv',
        'httpx'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\n🔍 Checking .env file...")
    
    if not Path('.env').exists():
        print("❌ .env file not found")
        sys.exit(1)
    
    with open('.env') as f:
        content = f.read()
        if 'OPENAI_API_KEY=' in content and len(content) > 30:
            print("✅ .env file with API key found")
        else:
            print("❌ .env file missing OPENAI_API_KEY")
            sys.exit(1)

def check_project_structure():
    """Check if all required directories and files exist"""
    print("\n🔍 Checking project structure...")
    
    required = [
        'pm_env/',
        'api/',
        'tasks/',
        'graders/',
        'scenarios/',
        'requirements.txt',
        'main.py',
        'inference.py'
    ]
    
    for item in required:
        if Path(item).exists():
            print(f"✅ {item}")
        else:
            print(f"❌ {item}")
            sys.exit(1)

def main():
    print("="*70)
    print("AI Product Manager Environment - Setup Verification")
    print("="*70)
    
    check_python_version()
    check_dependencies()
    check_env_file()
    check_project_structure()
    
    print("\n" + "="*70)
    print("✅ ALL CHECKS PASSED - Ready to run!")
    print("="*70)
    
    print("\n📋 Next Steps:")
    print("\n1️⃣  Start API Server (Terminal 1):")
    print("   python main.py")
    print("\n2️⃣  Run Inference (Terminal 2, after server starts):")
    print("   python inference.py task_001 scenario_1_saas_analytics")
    print("\n3️⃣  Or run demo (no API server needed):")
    print("   python demo.py")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
