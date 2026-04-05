# OpenEnv AI Product Manager - Quick Reference

## Installation
```bash
pip install pydantic>=2.0
```

## 5-Minute Start

### 1. Create Environment
```python
from pm_env import create_environment, Action

env = create_environment("scenario_1_saas_analytics", max_steps=10)
```

### 2. Reset
```python
observation = env.reset()
```

### 3. Take Action
```python
action = Action(
    action_type="prioritize",
    feature_id="F001",
    justification="Highest user votes"
)
```

### 4. Step Environment
```python
result = env.step(action)
# result.observation: Updated state
# result.reward: Reward (-1.0 to 1.0)
# result.done: Episode complete?
# result.info: Debug info
```

### 5. Get State
```python
state = env.state()
# Full environment state dict
```

## Action Types

```python
# Prioritize feature (add to roadmap)
Action(action_type="prioritize", feature_id="F001", justification="...")

# Reject feature (remove from backlog)
Action(action_type="reject", feature_id="F001", justification="...")

# Delay feature (defer to later)
Action(action_type="delay", feature_id="F001", justification="...")

# Request info (seek insight, no cost)
Action(action_type="request_info")

# Finalize roadmap (end episode)
Action(action_type="finalize")
```

## Reward Structure

| Action | Base Reward | Notes |
|---|---|---|
| Prioritize high-impact | +0.4 | Feature is in correct top 3 |
| + Valid justification | +0.2 | Justification > 5 characters |
| Prioritize low-priority | -0.1 | Feature not in top priorities |
| Reject high-priority | -0.3 | Feature is must-have |
| Reject low-priority | +0.05 | Feature is unimportant |
| Request info | 0.0 | Neutral exploration |
| Invalid action | -0.2 | Not allowed |
| Finalize (good) | +0.1 | Roadmap is sound |

**All rewards clipped to [-1.0, 1.0]**

## Scenarios

```python
# Available scenarios
scenarios = [
    "scenario_1_saas_analytics",
    "scenario_2_ecommerce",
    "scenario_3_healthcare",
    "scenario_4_collaboration",
    "scenario_5_finance"
]

env = create_environment("scenario_2_ecommerce")
```

## Tasks

```python
from tasks import get_task, list_tasks

# Get specific task
task = get_task("task_001")  # Easy
task = get_task("task_002")  # Medium
task = get_task("task_003")  # Hard

# List all
tasks = list_tasks()
```

### Task Specs

| Task | Difficulty | Max Steps | Objective |
|---|---|---|---|
| task_001 | Easy | 3 | Pick top feature |
| task_002 | Medium | 6 | Rank top 3 features |
| task_003 | Hard | 10 | Balance trade-offs |

## Grading

```python
from graders import grade_task

score, explanation = grade_task(
    task_id="task_001",
    actions_taken=["prioritize:F001", "finalize"],
    scenario=scenario_data,
    observation=final_observation
)

print(f"Score: {score:.2f}/1.0")
```

## Data Models

### Feature
```python
Feature(
    id="F001",
    name="Dark Mode",
    impact_area="satisfaction",  # retention|revenue|satisfaction
    effort=2,                     # 1-5
    votes=145
)
```

### Metrics
```python
Metrics(
    churn_rate=0.12,        # 0.0-1.0
    retention_rate=0.88,    # 0.0-1.0
    revenue_growth=8.5,     # percentage
    user_satisfaction=68.0  # 0-100
)
```

### Observation
```python
Observation(
    scenario_id="scenario_1",
    user_complaints=[...],          # 5+ common complaints
    metrics=Metrics(...),           # Current KPIs
    feature_backlog=[...],          # Features to prioritize
    constraints={                   # Budget/capacity
        "budget": 120000,
        "sprint_capacity": 50
    },
    previous_actions=[...],         # Action history
    step_count=0                    # Current step
)
```

### Action
```python
Action(
    action_type="prioritize",           # Required
    feature_id="F001",                  # For prioritize/reject/delay
    justification="Highest impact"      # Optional, +0.2 reward if good
)
```

### StepResult
```python
StepResult(
    observation=Observation(...),       # Updated state
    reward=0.4,                         # -1.0 to 1.0
    done=False,                         # Episode complete?
    info={                              # Debug info
        "action_executed": {...},
        "validation": "Valid",
        "reward_components": [...]
    }
)
```

## Common Patterns

### Pattern 1: Full Episode
```python
env = create_environment("scenario_1_saas_analytics", max_steps=10)
obs = env.reset()
total_reward = 0.0

while not done:
    action = get_next_action(obs)  # Your agent logic
    result = env.step(action)
    total_reward += result.reward
    obs = result.observation
    done = result.done

print(f"Total reward: {total_reward:.2f}")
```

### Pattern 2: Get State
```python
state = env.state()
print(f"Step: {state['step_count']}")
print(f"Prioritized: {state['prioritized_features']}")
print(f"Rejected: {state['rejected_features']}")
print(f"Delayed: {state['delayed_features']}")
```

### Pattern 3: Validate Action
```python
is_valid, info = env._validate_action(action)
if is_valid:
    result = env.step(action)
else:
    print(f"Invalid: {info['validation']}")
```

### Pattern 4: Grade Results
```python
from graders import grade_task

actions = [a for a in state['observation'].previous_actions]
score, explanation = grade_task(
    task_id="task_001",
    actions_taken=actions,
    scenario=get_scenario_data(),
    observation=state['observation']
)
```

## Features in Scenarios

```
scenario_1: F001-F006 (6 features)
scenario_2: F101-F105 (5 features)
scenario_3: F201-F205 (5 features)
scenario_4: F301-F306 (6 features)
scenario_5: F401-F405 (5 features)
```

## Key Constraints

```python
# Sprint capacity (max effort points)
constraints["sprint_capacity"]  # e.g., 50 points

# Budget limit
constraints["budget"]           # e.g., $120,000

# Check if action fits
total_effort = sum(
    f.effort for f in obs.feature_backlog
    if f.id in prioritized_features
)
fits = total_effort <= constraints["sprint_capacity"]
```

## Debugging

### See Feature Details
```python
for feature in obs.feature_backlog:
    print(f"{feature.id}: {feature.name}")
    print(f"  Effort: {feature.effort}/5")
    print(f"  Impact: {feature.impact_area}")
    print(f"  Votes: {feature.votes}")
```

### See Reward Breakdown
```python
result = env.step(action)
for component in result.info["reward_components"]:
    print(f"{component['component']}: {component['value']:+.2f}")
print(f"Total: {result.reward:+.2f}")
```

### See Action History
```python
obs = result.observation
for action_str in obs.previous_actions:
    print(f"Step {obs.step_count}: {action_str}")
```

## Performance Tips

1. **Cache scenario data**: Load once, reuse
2. **Batch validation**: Check multiple actions before stepping
3. **Use state()**: Get full state dict vs individual properties
4. **Reset wisely**: Create env once, reset multiple times

## Common Errors & Fixes

### Error: "Feature F999 not in backlog"
```python
# ❌ Wrong
action = Action(action_type="prioritize", feature_id="F999")

# ✅ Right
available_ids = [f.id for f in obs.feature_backlog]
if feature_id in available_ids:
    action = Action(action_type="prioritize", feature_id=feature_id)
```

### Error: "Exceeds sprint capacity"
```python
# ❌ Wrong - Too much effort
priorities = ["F001", "F002", "F003"]  # Total 9 effort > 8 capacity

# ✅ Right - Select carefully
priorities = ["F001"]  # 3 effort ≤ 8 capacity
```

### Error: "Feature already processed"
```python
# ❌ Wrong - Already prioritized F001
actions = ["prioritize:F001", "prioritize:F001"]

# ✅ Right - Each feature once
actions = ["prioritize:F001", "prioritize:F002"]
```

## Testing All Scenarios

```python
from pm_env import create_environment
from tasks import list_tasks

scenarios = [
    "scenario_1_saas_analytics",
    "scenario_2_ecommerce",
    "scenario_3_healthcare",
    "scenario_4_collaboration",
    "scenario_5_finance"
]

for scenario_id in scenarios:
    for task in list_tasks():
        env = create_environment(scenario_id, max_steps=task.max_steps)
        obs = env.reset()
        print(f"✅ {scenario_id} + {task.task_id}")
```

## Running Examples

```bash
# Full demonstrations
python example_run.py

# Scenario analysis
python scenario_explorer.py

# Custom testing
python -c "
from pm_env import create_environment, Action

env = create_environment('scenario_1_saas_analytics')
obs = env.reset()
action = Action(action_type='prioritize', feature_id='F001', justification='Test')
result = env.step(action)
print(f'Reward: {result.reward:.2f}')
"
```

## Quick Links

- **User Guide**: `README_OPENENV.md`
- **Specification**: `OPENENV_SPEC.md`
- **Examples**: `example_run.py`
- **Analysis**: `scenario_explorer.py`
- **Code**: `pm_env/`, `tasks/`, `graders/`

---

**📚 For complete documentation, see README_OPENENV.md**
