#!/usr/bin/env python
"""Quick demo script for the AI Product Manager Environment."""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set UTF-8 encoding for stdout (fixes Windows console issues)
if sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from env import create_environment
from models import Action, ActionType


def demo_local_env():
    """Demonstrate environment usage locally."""
    print("=" * 80)
    print("AI Product Manager Environment - Local Demo")
    print("=" * 80)
    
    # Create environment
    print("\n[1] Creating environment...")
    env = create_environment(
        scenario_key="scenario_1_ecommerce",
        task_id="task_001",
        seed=42
    )
    print("[OK] Environment created")
    
    # Reset
    print("\n[2] Resetting environment...")
    obs = env.reset()
    print(f"[OK] Environment reset")
    print(f"  Initial observation:")
    print(f"  - Summarized feedback: {obs.summarized_feedback[:80]}...")
    print(f"  - Metrics: {list(obs.metrics_summary.keys())}")
    print(f"  - Available actions: {obs.available_actions}")
    
    # Take actions
    print("\n[3] Taking sample actions...")
    actions = [
        Action(
            action_type=ActionType.REQUEST_MORE_INFO,
            reason="Get baseline understanding"
        ),
        Action(
            action_type=ActionType.PRIORITIZE_FEATURE,
            feature_id="F001",
            reason="Highest user requests"
        ),
        Action(
            action_type=ActionType.PRIORITIZE_FEATURE,
            feature_id="F002",
            reason="Best revenue impact"
        ),
        Action(
            action_type=ActionType.FINALIZE_ROADMAP,
            reason="Completing task"
        ),
    ]
    
    total_reward = 0.0
    
    for i, action in enumerate(actions, 1):
        obs, reward, done, info = env.step(action)
        total_reward += reward.total_reward
        
        print(f"\n  Step {i}: {action.action_type}")
        print(f"    Feature: {action.feature_id}")
        print(f"    Reward: {reward.total_reward:.3f} (total: {total_reward:.3f})")
        print(f"    Reason: {reward.reason}")
        print(f"    Done: {done}")
        
        if done:
            break
    
    # Final state
    print("\n[4] Final state:")
    state = env.state_dict()
    print(f"  Steps taken: {state['step_count']}")
    print(f"  Prioritized features: {state['prioritized_features']}")
    print(f"  Total reward: {total_reward:.3f}")
    
    print("\n" + "=" * 80)
    print(f"[OK] Demo complete! Total reward: {total_reward:.3f}")
    print("=" * 80)


def main():
    """Run all demos."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run demo")
    args = parser.parse_args()
    
    try:
        demo_local_env()
        
        return 0
    
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
