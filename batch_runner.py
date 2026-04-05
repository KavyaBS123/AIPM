#!/usr/bin/env python
"""Batch runner for all scenarios and tasks."""

import json
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from env import create_environment
from models import Action, ActionType
from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
from tasks import get_task


class BatchRunner:
    """Run environment through multiple scenarios and tasks."""
    
    def __init__(self, output_dir: Path = None):
        """Initialize runner."""
        self.output_dir = output_dir or Path("results")
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
    
    def run_scenario_task(self, scenario_key: str, task_id: str) -> Dict:
        """Run a single scenario-task combination."""
        print(f"\n🔧 Running {scenario_key} + {task_id}...")
        
        start_time = time.time()
        
        # Create and reset environment
        env = create_environment(
            scenario_key=scenario_key,
            task_id=task_id,
            seed=42
        )
        obs = env.reset()
        
        # Get task definition
        task_def = get_task(task_id)
        
        # Simple baseline strategy: request info, then prioritize top features
        actions_taken = []
        total_reward = 0.0
        
        # Step 1: Request more info
        action = Action(
            action_type=ActionType.REQUEST_MORE_INFO,
            reason="Initial information gathering"
        )
        obs, reward, done, info = env.step(action)
        actions_taken.append(action)
        total_reward += reward.total_reward
        
        if not done:
            # Steps 2+: Prioritize features
            feature_scores = {}
            for feature in env.state.available_features:
                # Simple heuristic scoring
                score = (
                    (min(feature.user_requests, 1000) / 1000.0) * 0.4 +
                    max(0, feature.impact_on_satisfaction) * 0.3 +
                    max(0, -feature.impact_on_churn) * 0.3
                )
                feature_scores[feature.feature_id] = (score, feature)
            
            # Sort by score
            sorted_features = sorted(
                feature_scores.items(),
                key=lambda x: x[1][0],
                reverse=True
            )
            
            # Prioritize top features
            prioritized = 0
            max_prioritize = 3
            
            for feature_id, (score, feature) in sorted_features:
                if prioritized >= max_prioritize or done:
                    break
                
                action = Action(
                    action_type=ActionType.PRIORITIZE_FEATURE,
                    feature_id=feature_id,
                    reason=f"Score: {score:.2f}"
                )
                
                obs, reward, done, info = env.step(action)
                actions_taken.append(action)
                total_reward += reward.total_reward
                prioritized += 1
                
                if done:
                    break
        
        # Finalize if not done
        if not done:
            action = Action(
                action_type=ActionType.FINALIZE_ROADMAP,
                reason="Task completion"
            )
            obs, reward, done, info = env.step(action)
            actions_taken.append(action)
            total_reward += reward.total_reward
        
        elapsed_time = time.time() - start_time
        
        result = {
            "scenario": scenario_key,
            "task": task_id,
            "task_difficulty": task_def.difficulty,
            "total_reward": total_reward,
            "steps_taken": len(actions_taken),
            "max_steps": task_def.max_steps,
            "time_elapsed": elapsed_time,
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
        }
        
        return result
    
    def run_all(self) -> List[Dict]:
        """Run all scenario-task combinations."""
        scenarios = [
            "scenario_1_ecommerce",
            "scenario_2_saas",
            "scenario_3_social",
        ]
        tasks = [
            "task_001",
            "task_002",
            "task_003",
        ]
        
        print("=" * 80)
        print("🚀 Starting Batch Run")
        print(f"Scenarios: {len(scenarios)}, Tasks: {len(tasks)}")
        print(f"Total combinations: {len(scenarios) * len(tasks)}")
        print("=" * 80)
        
        overall_start = time.time()
        
        try:
            for scenario in scenarios:
                for task in tasks:
                    try:
                        result = self.run_scenario_task(scenario, task)
                        self.results.append(result)
                        
                        print(f"✓ Reward: {result['total_reward']:.3f}, "
                              f"Steps: {result['steps_taken']}, "
                              f"Time: {result['time_elapsed']:.2f}s")
                    
                    except Exception as e:
                        print(f"❌ Error: {e}")
                        self.results.append({
                            "scenario": scenario,
                            "task": task,
                            "status": "failed",
                            "error": str(e),
                        })
        
        finally:
            overall_time = time.time() - overall_start
            self._save_results(overall_time)
        
        return self.results
    
    def _save_results(self, total_time: float):
        """Save results to file."""
        output_file = self.output_dir / f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_time": total_time,
            "total_combinations": len(self.results),
            "successful": sum(1 for r in self.results if r.get("status") == "completed"),
            "failed": sum(1 for r in self.results if r.get("status") == "failed"),
            "average_reward": (
                sum(r.get("total_reward", 0) for r in self.results if r.get("status") == "completed") /
                sum(1 for r in self.results if r.get("status") == "completed")
                if any(r.get("status") == "completed" for r in self.results)
                else 0.0
            ),
            "results": self.results,
        }
        
        with open(output_file, "w") as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 80)
        print("📊 Batch Run Complete")
        print("=" * 80)
        print(f"Total time: {total_time:.2f}s")
        print(f"Successful: {summary['successful']}/{len(self.results)}")
        print(f"Failed: {summary['failed']}/{len(self.results)}")
        print(f"Average reward: {summary['average_reward']:.3f}")
        print(f"Results saved to: {output_file}")
        
        # Print summary table
        print("\n" + "Scenario".ljust(25) + "Task".ljust(15) + "Reward".ljust(12) + "Steps")
        print("-" * 65)
        for r in self.results:
            if r.get("status") == "completed":
                print(
                    f"{r['scenario'].ljust(25)}"
                    f"{r['task'].ljust(15)}"
                    f"{r['total_reward']:<12.3f}"
                    f"{r['steps_taken']}/{r['max_steps']}"
                )


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run batch tests")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results"),
        help="Output directory for results"
    )
    
    args = parser.parse_args()
    
    runner = BatchRunner(output_dir=args.output_dir)
    runner.run_all()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
