"""Configuration for the AI Product Manager Environment."""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "false").lower() == "true"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "500"))

# Environment Configuration
DEFAULT_SCENARIO = os.getenv("DEFAULT_SCENARIO", "scenario_1_ecommerce")
DEFAULT_TASK = os.getenv("DEFAULT_TASK")
DEFAULT_SEED = int(os.getenv("DEFAULT_SEED", "42"))
MAX_STEPS = int(os.getenv("MAX_STEPS", "30"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE")

# Directories
LOGS_DIR = PROJECT_ROOT / "logs"
RESULTS_DIR = PROJECT_ROOT / "results"

# Create directories if needed
LOGS_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)


def get_config() -> dict:
    """Get full configuration as dictionary."""
    return {
        "api": {
            "host": API_HOST,
            "port": API_PORT,
            "reload": API_RELOAD,
        },
        "openai": {
            "api_key": "***" if OPENAI_API_KEY else None,
            "model": OPENAI_MODEL,
            "temperature": OPENAI_TEMPERATURE,
            "max_tokens": OPENAI_MAX_TOKENS,
        },
        "environment": {
            "default_scenario": DEFAULT_SCENARIO,
            "default_task": DEFAULT_TASK,
            "default_seed": DEFAULT_SEED,
            "max_steps": MAX_STEPS,
        },
        "logging": {
            "level": LOG_LEVEL,
            "file": LOG_FILE,
        },
        "paths": {
            "project_root": str(PROJECT_ROOT),
            "logs_dir": str(LOGS_DIR),
            "results_dir": str(RESULTS_DIR),
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(get_config(), indent=2))
