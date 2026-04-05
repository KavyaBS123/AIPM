"""Example script demonstrating the AI Product Manager Environment."""

from pm_env import create_environment, Action
from tasks import get_task
from graders import grade_task


def run_example_task_1():
    """Example: Task 1 - Easy Feature Identification."""
    print("\n" + "="*70)
    print("EXAMPLE: Task 1 - Critical Feature Identification (Easy)")
    print("="*70)
    
    # Create environment for scenario 1
    env = create_environment("scenario_1_saas_analytics", max_steps=3)
    
    # Reset and get initial observation
    obs = env.reset()
    print(f"\n📊 Scenario: {obs.scenario_id}")
    print(f"\n😞 User Complaints:")
    for complaint in obs.user_complaints[:3]:
        print(f"  • {complaint}")
    
    print(f"\n📈 Current Metrics:")
    print(f"  • Churn Rate: {obs.metrics.churn_rate:.1%}")
    print(f"  • User Satisfaction: {obs.metrics.user_satisfaction:.1f}/100")
    
    print(f"\n📋 Available Features:")
    for feature in obs.feature_backlog[:4]:
        print(f"  • F{feature.id[-2:]}: {feature.name} (votes: {feature.votes}, effort: {feature.effort})")
    
    # Step 1: Agent requests info
    print("\n\n🤖 Agent Step 1: Request more info")
    action = Action(action_type="request_info")
    result = env.step(action)
    print(f"   Reward: {result.reward:.2f}")
    
    # Step 2: Agent prioritizes top feature
    print("\n🤖 Agent Step 2: Prioritize F001 (Dashboard Performance)")
    action = Action(
        action_type="prioritize",
        feature_id="F001",
        justification="Highest user votes (245) + retention impact addresses churn"
    )
    result = env.step(action)
    print(f"   Reward: {result.reward:.2f}")
    
    # Step 3: Agent finalizes
    print("\n🤖 Agent Step 3: Finalize decision")
    action = Action(action_type="finalize")
    result = env.step(action)
    print(f"   Reward: {result.reward:.2f}")
    print(f"   Episode done: {result.done}")
    
    print(f"\n✅ Episode complete!")
    return env


def run_example_task_2():
    """Example: Task 2 - Roadmap Prioritization."""
    print("\n" + "="*70)
    print("EXAMPLE: Task 2 - Roadmap Prioritization (Medium)")
    print("="*70)
    
    env = create_environment("scenario_2_ecommerce", max_steps=6)
    obs = env.reset()
    
    print(f"\n📊 Scenario: {obs.scenario_id}")
    print(f"💰 Constraints: Budget ${obs.constraints['budget']:,}, Capacity {obs.constraints['sprint_capacity']} pts")
    
    # Step 1: Request info
    print("\n🤖 Step 1: Request information")
    action = Action(action_type="request_info")
    result = env.step(action)
    print(f"   Status: {result.info.get('validation', 'ok')}")
    
    # Step 2-4: Prioritize top 3 features
    features_to_prioritize = ["F101", "F102", "F103"]
    for i, feature_id in enumerate(features_to_prioritize, start=2):
        print(f"\n🤖 Step {i}: Prioritize {feature_id}")
        action = Action(
            action_type="prioritize",
            feature_id=feature_id,
            justification=f"Feature {feature_id} is in top 3 priorities"
        )
        result = env.step(action)
        print(f"   Reward: {result.reward:.2f}")
    
    # Final: Finalize
    print(f"\n🤖 Step 5: Finalize roadmap")
    action = Action(action_type="finalize")
    result = env.step(action)
    print(f"   Final Reward: {result.reward:.2f}")
    print(f"   Done: {result.done}")
    
    return env


def run_example_task_3():
    """Example: Task 3 - Trade-off Decisions."""
    print("\n" + "="*70)
    print("EXAMPLE: Task 3 - Strategic Trade-off Decisions (Hard)")
    print("="*70)
    
    env = create_environment("scenario_3_healthcare", max_steps=10)
    obs = env.reset()
    
    print(f"\n📊 Scenario: {obs.scenario_id}")
    print(f"💰 Budget: ${obs.constraints['budget']:,}")
    print(f"⚡ Sprint Capacity: {obs.constraints['sprint_capacity']} points")
    
    print(f"\n😞 Key Issues:")
    for i, complaint in enumerate(obs.user_complaints[:3], 1):
        print(f"   {i}. {complaint}")
    
    # Strategy: Prioritize high-impact features within capacity
    print("\n\n🤖 Agent Strategy: Balance retention + revenue within constraints")
    
    actions_sequence = [
        ("request_info", None, "Analyze metrics and trade-offs"),
        ("prioritize", "F202", "Video quality - high retention impact"),
        ("prioritize", "F204", "Records sync - critical retention feature"),
        ("delay", "F205", "EHR integration expensive, defer to later"),
        ("prioritize", "F203", "Recurring appointments - quick win"),
        ("finalize", None, "Submit roadmap"),
    ]
    
    for step, (action_type, feature_id, reasoning) in enumerate(actions_sequence, 1):
        print(f"\n🤖 Step {step}: {reasoning}")
        action = Action(
            action_type=action_type,
            feature_id=feature_id,
            justification=reasoning
        )
        result = env.step(action)
        print(f"   Reward: {result.reward:+.2f}")
        
        if result.done:
            print(f"   ✅ Episode Complete (Step {step}/{result.info.get('step', step)+1})")
            break
    
    return env


def demonstrate_grading():
    """Demonstrate the grading system."""
    print("\n" + "="*70)
    print("GRADING SYSTEM DEMONSTRATION")
    print("="*70)
    
    # Load scenario and task
    from pm_env import load_scenario
    from tasks import get_task
    
    scenario = load_scenario("scenario_1_saas_analytics")
    task = get_task("task_001")
    
    print(f"\n📋 Task: {task.name}")
    print(f"   Difficulty: {task.difficulty}")
    print(f"   Max Steps: {task.max_steps}")
    print(f"\n   Goal: {task.objective}")
    
    print(f"\n🎯 Correct Priority Order: {scenario['correct_priority_order']}")
    
    # Simulate different performance levels
    print("\n" + "-"*70)
    print("Performance Scenario 1: Perfect")
    actions = ["prioritize:F001"]  # Correct top feature
    env = create_environment("scenario_1_saas_analytics", max_steps=3)
    obs = env.reset()
    for action_str in actions:
        parts = action_str.split(":")
        action = Action(action_type=parts[0], feature_id=parts[1] if len(parts) > 1 else None)
        result = env.step(action)
    obs = result.observation
    
    score, explanation = grade_task("task_001", actions, scenario, obs)
    print(f"   Actions: {actions}")
    print(f"   Score: {score:.2f}/1.0 ✅")
    print(f"   Reason: {explanation.get('reason', '')}")
    
    # Performance 2: Second best
    print("\n" + "-"*70)
    print("Performance Scenario 2: Acceptable")
    actions = ["prioritize:F003"]  # Second-tier feature
    env = create_environment("scenario_1_saas_analytics", max_steps=3)
    obs = env.reset()
    for action_str in actions:
        parts = action_str.split(":")
        action = Action(action_type=parts[0], feature_id=parts[1] if len(parts) > 1 else None)
        result = env.step(action)
    obs = result.observation
    
    score, explanation = grade_task("task_001", actions, scenario, obs)
    print(f"   Actions: {actions}")
    print(f"   Score: {score:.2f}/1.0 ⚠️")
    print(f"   Reason: {explanation.get('reason', '')}")
    
    # Performance 3: Incorrect
    print("\n" + "-"*70)
    print("Performance Scenario 3: Incorrect")
    actions = ["prioritize:F005"]  # Wrong feature
    env = create_environment("scenario_1_saas_analytics", max_steps=3)
    obs = env.reset()
    for action_str in actions:
        parts = action_str.split(":")
        action = Action(action_type=parts[0], feature_id=parts[1] if len(parts) > 1 else None)
        result = env.step(action)
    obs = result.observation
    
    score, explanation = grade_task("task_001", actions, scenario, obs)
    print(f"   Actions: {actions}")
    print(f"   Score: {score:.2f}/1.0 ❌")
    print(f"   Reason: {explanation.get('reason', '')}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print(" AI PRODUCT MANAGER ENVIRONMENT - EXAMPLES & DEMONSTRATIONS")
    print("="*70)
    
    # Run examples
    run_example_task_1()
    run_example_task_2()
    run_example_task_3()
    
    # Demonstrate grading
    demonstrate_grading()
    
    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70)
