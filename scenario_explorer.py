"""Scenario explorer and tester for the AI Product Manager Environment."""

import json
from pm_env import create_environment, load_scenario
from tasks import list_tasks, get_task


def explore_scenario(scenario_id: str):
    """Interactively explore a scenario."""
    print("\n" + "="*70)
    print(f"SCENARIO EXPLORER: {scenario_id}")
    print("="*70)
    
    try:
        scenario = load_scenario(scenario_id)
    except Exception as e:
        print(f"❌ Error loading scenario: {e}")
        return
    
    print(f"\n📋 Scenario Details:")
    print(f"   Name: {scenario.get('name', 'Unknown')}")
    print(f"   Description: {scenario.get('description', 'N/A')}")
    
    print(f"\n📊 Metrics:")
    metrics = scenario.get('metrics', {})
    print(f"   Churn Rate: {metrics.get('churn_rate', 0):.1%}")
    print(f"   Retention Rate: {metrics.get('retention_rate', 0):.1%}")
    print(f"   Revenue Growth: {metrics.get('revenue_growth', 0):.1f}%")
    print(f"   User Satisfaction: {metrics.get('user_satisfaction', 0):.1f}/100")
    
    print(f"\n😞 User Complaints ({len(scenario.get('user_complaints', []))}):")
    for i, complaint in enumerate(scenario.get('user_complaints', []), 1):
        print(f"   {i}. {complaint}")
    
    print(f"\n💰 Constraints:")
    constraints = scenario.get('constraints', {})
    for key, value in constraints.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n📦 Features ({len(scenario.get('features', []))}):")
    for feature in scenario.get('features', []):
        print(f"\n   {feature['id']}: {feature['name']}")
        print(f"      Impact Area: {feature['impact_area']}")
        print(f"      Effort: {feature['effort']}/5")
        print(f"      User Votes: {feature['votes']}")
    
    print(f"\n🎯 Correct Priority Order:")
    priority = scenario.get('correct_priority_order', [])
    for i, feature_id in enumerate(priority, 1):
        # Find feature name
        feature_name = next(
            (f['name'] for f in scenario.get('features', []) if f['id'] == feature_id),
            "Unknown"
        )
        print(f"   {i}. {feature_id}: {feature_name}")
    
    print(f"\n📈 Expected Effort Distribution:")
    total_effort = sum(
        next((f['effort'] for f in scenario.get('features', []) if f['id'] == fid), 0)
        for fid in priority
    )
    print(f"   Total effort for priority features: {total_effort} points")
    print(f"   Available capacity: {constraints.get('sprint_capacity', 'N/A')} points")
    
    if total_effort <= constraints.get('sprint_capacity', float('inf')):
        print(f"   ✅ Fits within sprint capacity!")
    else:
        print(f"   ⚠️  Exceeds sprint capacity by {total_effort - constraints.get('sprint_capacity', 0)} points")


def compare_scenarios():
    """Compare all scenarios side-by-side."""
    print("\n" + "="*70)
    print("SCENARIO COMPARISON")
    print("="*70)
    
    scenarios_file = "scenarios/scenarios.json"
    with open(scenarios_file, 'r') as f:
        data = json.load(f)
    
    scenarios = data.get('scenarios', [])
    
    print(f"\n{'Scenario':<8} {'Churn':<8} {'Sat':<8} {'Growth':<8} {'Budget':<10} {'Features':<8}")
    print("-" * 70)
    
    for scenario in scenarios:
        scenario_id = scenario['id'].replace('scenario_', '').replace('_', ' ')[:8]
        metrics = scenario.get('metrics', {})
        constraints = scenario.get('constraints', {})
        
        print(
            f"{scenario_id:<8} "
            f"{metrics.get('churn_rate', 0):.0%}      "
            f"{metrics.get('user_satisfaction', 0):>5.0f}   "
            f"{metrics.get('revenue_growth', 0):>6.1f}%  "
            f"${constraints.get('budget', 0):>8,}  "
            f"{len(scenario.get('features', [])):<8}"
        )
    
    print("\n📊 Key Differences:")
    churn = [(s['id'], s['metrics']['churn_rate']) for s in scenarios]
    highest_churn = max(churn, key=lambda x: x[1])
    lowest_churn = min(churn, key=lambda x: x[1])
    
    print(f"   Highest Churn: {highest_churn[0]} ({highest_churn[1]:.0%})")
    print(f"   Lowest Churn: {lowest_churn[0]} ({lowest_churn[1]:.0%})")
    
    satisfaction = [(s['id'], s['metrics']['user_satisfaction']) for s in scenarios]
    highest_sat = max(satisfaction, key=lambda x: x[1])
    lowest_sat = min(satisfaction, key=lambda x: x[1])
    
    print(f"   Highest Satisfaction: {highest_sat[0]} ({highest_sat[1]:.0f}/100)")
    print(f"   Lowest Satisfaction: {lowest_sat[0]} ({lowest_sat[1]:.0f}/100)")


def list_all_scenarios():
    """List all available scenarios."""
    print("\n" + "="*70)
    print("AVAILABLE SCENARIOS")
    print("="*70)
    
    scenarios_file = "scenarios/scenarios.json"
    with open(scenarios_file, 'r') as f:
        data = json.load(f)
    
    scenarios = data.get('scenarios', [])
    
    print(f"\n{len(scenarios)} scenarios available:\n")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['id']}")
        print(f"   Name: {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        print()


def list_all_tasks():
    """List all available tasks."""
    print("\n" + "="*70)
    print("AVAILABLE TASKS")
    print("="*70)
    
    tasks = list_tasks()
    
    for i, task in enumerate(tasks, 1):
        print(f"\n{i}. {task.task_id}: {task.name}")
        print(f"   Difficulty: {task.difficulty.upper()}")
        print(f"   Max Steps: {task.max_steps}")
        print(f"   Objective: {task.objective}")
        print(f"   Success Criteria: {task.success_criteria}")


def test_scenario_task_combo(scenario_id: str, task_id: str):
    """Test a specific scenario-task combination."""
    print("\n" + "="*70)
    print(f"TESTING: {scenario_id} + {task_id}")
    print("="*70)
    
    try:
        env = create_environment(scenario_id)
        task = get_task(task_id)
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    obs = env.reset()
    
    print(f"\n✅ Environment initialized successfully")
    print(f"   Scenario: {obs.scenario_id}")
    print(f"   Features available: {len(obs.feature_backlog)}")
    print(f"   User complaints: {len(obs.user_complaints)}")
    print(f"   Constraints: {obs.constraints}")
    
    print(f"\n✅ Task loaded successfully")
    print(f"   Task: {task.name} ({task.difficulty})")
    print(f"   Max steps: {task.max_steps}")
    
    print(f"\n✅ Compatibility check PASSED")
    print(f"   Ready to run task in scenario!")


def show_feature_impact_analysis(scenario_id: str):
    """Analyze feature impact for a scenario."""
    print("\n" + "="*70)
    print(f"FEATURE IMPACT ANALYSIS: {scenario_id}")
    print("="*70)
    
    scenario = load_scenario(scenario_id)
    
    print(f"\n{'Feature':<8} {'Name':<25} {'Impact':<12} {'Effort':<8} {'Votes':<8}")
    print("-" * 70)
    
    features = scenario.get('features', [])
    features_sorted = sorted(features, key=lambda x: x['votes'], reverse=True)
    
    for f in features_sorted:
        print(
            f"{f['id']:<8} "
            f"{f['name'][:24]:<25} "
            f"{f['impact_area']:<12} "
            f"{f['effort']:<8} "
            f"{f['votes']:<8}"
        )
    
    print(f"\n💡 Insights:")
    
    # Effort vs Impact
    high_effort = [f for f in features if f['effort'] >= 4]
    low_effort = [f for f in features if f['effort'] <= 2]
    
    print(f"\n   High Effort Features ({len(high_effort)}):")
    for f in high_effort:
        print(f"      {f['id']}: {f['name']} ({f['votes']} votes)")
    
    print(f"\n   Low Effort Features ({len(low_effort)}):")
    for f in low_effort:
        print(f"      {f['id']}: {f['name']} ({f['votes']} votes)")
    
    # Impact areas
    impact_areas = {}
    for f in features:
        area = f['impact_area']
        if area not in impact_areas:
            impact_areas[area] = {'count': 0, 'avg_votes': 0, 'features': []}
        impact_areas[area]['count'] += 1
        impact_areas[area]['avg_votes'] += f['votes']
        impact_areas[area]['features'].append(f['id'])
    
    print(f"\n   Impact Area Distribution:")
    for area, data in impact_areas.items():
        avg = data['avg_votes'] / data['count'] if data['count'] > 0 else 0
        print(f"      {area.title()}: {data['count']} features, avg {avg:.0f} votes")


def main():
    """Interactive menu for scenario exploration."""
    while True:
        print("\n" + "="*70)
        print("AI PRODUCT MANAGER - SCENARIO EXPLORER")
        print("="*70)
        print("\n1. List all scenarios")
        print("2. List all tasks")
        print("3. Compare scenarios")
        print("4. Explore scenario (detailed)")
        print("5. Analyze feature impact")
        print("6. Test scenario-task combo")
        print("7. Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == "1":
            list_all_scenarios()
        elif choice == "2":
            list_all_tasks()
        elif choice == "3":
            compare_scenarios()
        elif choice == "4":
            scenario_id = input("Enter scenario ID (e.g., scenario_1_saas_analytics): ").strip()
            explore_scenario(scenario_id)
        elif choice == "5":
            scenario_id = input("Enter scenario ID: ").strip()
            show_feature_impact_analysis(scenario_id)
        elif choice == "6":
            scenario_id = input("Enter scenario ID: ").strip()
            task_id = input("Enter task ID (e.g., task_001): ").strip()
            test_scenario_task_combo(scenario_id, task_id)
        elif choice == "7":
            print("\n✅ Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    # Run a quick demo
    print("\n" + "="*70)
    print("QUICK SCENARIO OVERVIEW")
    print("="*70)
    
    compare_scenarios()
    
    print("\n\n" + "="*70)
    print("DETAILED SCENARIO SAMPLE: SaaS Analytics")
    print("="*70)
    
    explore_scenario("scenario_1_saas_analytics")
    
    print("\n\n" + "="*70)
    print("FEATURE IMPACT: Healthcare SaaS")
    print("="*70)
    
    show_feature_impact_analysis("scenario_3_healthcare")
    
    print("\n\n" + "="*70)
    print("For interactive exploration, uncomment main() and run directly")
    print("="*70)
