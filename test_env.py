"""Debug script to check environment variable loading."""

import os
from dotenv import load_dotenv

print("=" * 80)
print("ENVIRONMENT VARIABLE DEBUG")
print("=" * 80)

# Load without path first
print("\n[1] Loading without explicit path...")
load_dotenv()
key1 = os.getenv("OPENAI_API_KEY")
print(f"Result: {key1[:50]}..." if key1 else "Result: None")

# Load with explicit path
print("\n[2] Loading with explicit .env path...")
import os.path
env_path = os.path.join(os.getcwd(), ".env")
print(f"Looking for: {env_path}")
print(f"File exists: {os.path.exists(env_path)}")

# Clear and reload
os.environ.pop("OPENAI_API_KEY", None)
load_dotenv(dotenv_path=env_path, override=True)
key2 = os.getenv("OPENAI_API_KEY")
print(f"Result: {key2[:50]}..." if key2 else "Result: None")

# Check if they match
print("\n[3] Comparison:")
print(f"Keys match: {key1 == key2}")
if key1:
    print(f"Key1 starts with: {key1[:20]}")
if key2:
    print(f"Key2 starts with: {key2[:20]}")

# Check file contents
print("\n[4] Checking .env file contents...")
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'OPENAI' in line and '=' in line:
            key_part = line.split('=')[1].strip() if len(line.split('=')) > 1 else ""
            print(f"Line {i}: OPENAI_API_KEY={key_part[:50]}...")
        elif line.strip() and not line.startswith('#'):
            print(f"Line {i}: {line.strip()[:60]}")

print("\n" + "=" * 80)
