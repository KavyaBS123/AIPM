# 🎨 VISUAL GUIDE - Complete Project Architecture & Execution Flow

## SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AI PRODUCT MANAGER ENVIRONMENT                   │
│                        COMPLETE SYSTEM                              │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 1: BUSINESS LOGIC (pm_env/)                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ProductManagerEnvironment()                                       │
│  ├─ Manages game state                                            │
│  ├─ Processes actions                                             │
│  ├─ Calculates rewards                                            │
│  └─ Tracks metrics                                                │
│                                                                     │
│  Scenarios (5 total)                                               │
│  ├─ SaaS Analytics       (12% churn, $120K)                       │
│  ├─ E-Commerce          (15% churn, $180K)                       │
│  ├─ Healthcare SaaS     (8% churn, $200K)                        │
│  ├─ Collaboration Tool  (22% churn, $150K)                       │
│  └─ Personal Finance    (18% churn, $140K)                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 2: TASK SYSTEM (tasks/, graders/)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Task Definitions                                                  │
│  ├─ task_001: Easy   (3 steps)  → Identify 1 feature            │
│  ├─ task_002: Medium (6 steps)  → Rank 3 features               │
│  └─ task_003: Hard   (10 steps) → Build roadmap                 │
│                                                                     │
│  Grading System                                                    │
│  ├─ Easy Grader    → Correct/partial/wrong scoring              │
│  ├─ Medium Grader  → Ranking accuracy scoring                    │
│  └─ Hard Grader    → Multi-factor scoring                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 3: API LAYER (api/)                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FastAPI Server (Port 8000)                                        │
│  ├─ /health      → Health check                                   │
│  ├─ /reset       → Initialize environment                         │
│  ├─ /step        → Execute action                                 │
│  ├─ /state       → Get current state                              │
│  ├─ /tasks       → List all tasks                                 │
│  └─ /docs        → Swagger UI                                     │
│                                                                     │
│  Uvicorn ASGI Server                                               │
│  ├─ Handles HTTP requests                                         │
│  ├─ Manages global environment                                    │
│  ├─ Serializes responses as JSON                                  │
│  └─ Provides Swagger documentation                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 4: AI INFERENCE (inference.py)                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Script Flow                                                       │
│  1. Connect to API Server                                         │
│  2. Call /reset endpoint                                          │
│  3. Receive initial observation                                   │
│  4. Build prompt for GPT-4o                                       │
│  5. Call OpenAI API (GPT-4o)                                      │
│  6. Parse response into action                                    │
│  7. Call /step endpoint                                           │
│  8. Log results [STEP N]                                          │
│  9. Repeat 3-8 until done or max steps                           │
│  10. Display final grader_score                                   │
│                                                                    │
│  OpenAI GPT-4o                                                     │
│  ├─ Analyzes product situation                                    │
│  ├─ Reasons about feature prioritization                          │
│  ├─ Makes strategic decisions                                     │
│  └─ Returns action with reasoning                                 │
│                                                                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 5: DATA MODELS (models/)                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Input Models                                                      │
│  ├─ Action          → action_type, feature_id, reasoning         │
│  └─ request bodies  → Validated with Pydantic                    │
│                                                                    │
│  Output Models                                                     │
│  ├─ Observation     → Current game state                         │
│  ├─ Reward          → Reward breakdown                           │
│  └─ Response bodies → Type-safe JSON                             │
│                                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## EXECUTION PATHS

### PATH 1: LOCAL DEMO (Standalone)

```
User Terminal
    │
    ├─── Execute: python demo.py
    │
    ├─ Import: from env import create_environment
    │
    ├─ Create: ProductManagerEnvironment(scenario_1_ecommerce, task_001)
    │
    ├─ Method: env.reset()
    │           │
    │           ├─ Load scenario data
    │           ├─ Load task definition
    │           ├─ Initialize state
    │           └─ Return observation
    │
    ├─ Method: env.step(Action(prioritize_feature, F001))
    │           │
    │           ├─ Validate action
    │           ├─ Update environment state
    │           ├─ Calculate reward
    │           ├─ Calculate new metrics
    │           └─ Return (observation, reward, done, info)
    │
    ├─ Repeat: env.step() for multiple actions
    │
    ├─ Output: Console logs with:
    │           ├─ Step-by-step details
    │           ├─ Rewards for each action
    │           ├─ Total accumulated reward
    │           └─ Final results
    │
    └─ Exit: Script terminates (< 2 seconds)


Flow Diagram:
┌─────────────┐
│  demo.py    │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Create Environment  │
│ (scenario_1,task_1) │
└──────┬──────────────┘
       │
       ▼
┌──────────────────┐
│ env.reset()      │
│ Get observation  │
└──────┬───────────┘
       │
       ▼
    ┌──────────────────────┐
    │ Step 1: action_1     │
    │ Reward: 0.020        │
    │ Total: 0.020         │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Step 2: action_2     │
    │ Reward: 0.204        │
    │ Total: 0.224         │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Step 3: action_3     │
    │ Reward: 0.135        │
    │ Total: 0.359         │
    │ Done: TRUE           │
    └──────┬───────────────┘
           │
           ▼
    ┌─────────────────────┐
    │ Print Results       │
    │ Total Reward: 0.359 │
    └─────────────────────┘
```

---

### PATH 2: API SERVER + REST

```
Server Start
    │
    ├─── Execute: python main.py
    │
    ├─ Create: FastAPI app
    │
    ├─ Start: Uvicorn server on 0.0.0.0:8000
    │
    ├─ Ready: Listening for HTTP requests
    │
    
Client Connection (Another terminal/browser)
    │
    ├─── GET /health
    │     │
    │     └─► Returns: HTTP 200 OK
    │                  {"status": "healthy"}
    │
    ├─── POST /reset ({"task_id": "task_001"})
    │     │
    │     ├─ Server calls env.reset()
    │     │
    │     └─► Returns: HTTP 200 OK
    │                  {"observation": {...}, "info": {...}}
    │
    ├─── POST /step ({"action": {...}})
    │     │
    │     ├─ Server calls env.step(action)
    │     │
    │     └─► Returns: HTTP 200 OK
    │                  {"observation": {...}, "reward": {...}, "done": false}
    │
    └─── Server continues listening for more requests


Architecture:
┌──────────────┐
│ HTTP Client  │  (Browser, curl, Python script)
│  (Port 8000) │
└──────┬───────┘
       │
       ▼ HTTP Request
┌──────────────────────┐
│  Uvicorn Server      │
│  (ASGI Container)    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  FastAPI Router      │
│  - Route matching    │
│  - Request validation│
│  - Response creation │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Environment Ops     │
│  - env.reset()       │
│  - env.step()        │
│  - env.get_state()   │
└──────┬───────────────┘
       │
       ▼ JSON
┌──────────────────────┐
│  Response (JSON)     │
│  - Pydantic model    │
│  - Serialized JSON   │
└──────┬───────────────┘
       │
       ▼ HTTP Response
┌──────────────────────┐
│  HTTP Client         │
│  Receives JSON       │
└──────────────────────┘
```

---

### PATH 3: FULL AI INFERENCE

```
Terminal 1: python main.py
    │
    └─► API Server running (port 8000)


Terminal 2: python inference.py task_001 scenario_1_saas_analytics
    │
    ├─ Load .env (OpenAI API key)
    │
    ├─ Connect to http://localhost:8000
    │
    ├─ POST /reset
    │   │
    │   └─► Get initial observation
    │
    ├─ Loop:
    │   │
    │   ├─ Build Prompt:
    │   │   "You are a product manager. Here's the situation..."
    │   │   [observation data]
    │   │   "What should you prioritize?"
    │   │
    │   ├─ Call OpenAI API
    │   │   │
    │   │   ├─ Model: gpt-4o
    │   │   ├─ Send: prompt + context
    │   │   │
    │   │   └─► Receive: reasoning + action recommendation
    │   │
    │   ├─ Parse Response:
    │   │   Action(
    │   │     action_type="prioritize_feature",
    │   │     feature_id="F001",
    │   │     reason="High impact on churn..."
    │   │   )
    │   │
    │   ├─ POST /step
    │   │   │
    │   │   └─► Get: observation, reward, done
    │   │
    │   ├─ Log Results:
    │   │   [STEP N] action=... feature=... reward=...
    │   │
    │   └─ If done=true: Exit loop, else continue
    │
    ├─ Calculate Score:
    │   grader_score = grade_task(...)
    │
    ├─ Display Results:
    │   [END] total_reward=X grader_score=Y steps=Z
    │
    └─ Exit (10-15 seconds)


Detailed Flow:
┌──────────────────┐
│ inference.py     │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│ Load environment:        │
│ - API endpoint           │
│ - OpenAI API key         │
│ - Task definition        │
│ - Scenario definition    │
└────────┬─────────────────┘
         │
         ▼ POST /reset
┌──────────────────────────┐
│ API Server               │
│ env.reset()              │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Initial Observation:     │
│ - Feedback summary       │
│ - Current metrics        │
│ - Available features     │
│ - Action options         │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Build GPT-4o Prompt:     │
│ - Situation analysis     │
│ - Feature descriptions   │
│ - Current metrics        │
│ - Constraints            │
└────────┬─────────────────┘
         │
         ▼ OpenAI API
┌──────────────────────────┐
│ GPT-4o Response:         │
│ - Reasoning              │
│ - Recommended Action     │
│ - Justification          │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Parse & Validate:        │
│ - Extract action_type    │
│ - Extract feature_id     │
│ - Create Action object   │
└────────┬─────────────────┘
         │
         ▼ POST /step
┌──────────────────────────┐
│ API Server               │
│ env.step(action)         │
│ - Update state           │
│ - Calculate reward       │
│ - Determine winner       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Step Result:             │
│ - Reward (float)         │
│ - New observation        │
│ - Done flag              │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Log & Accumulate:        │
│ [STEP N] action=...      │
│ reward=...               │
│ total_reward += reward   │
└────────┬─────────────────┘
         │
         ▼ Continue?
        ╱ ╲
    YES╱   ╲NO
      ╱     ╲
     ▼       ▼
   Loop    Calculate
           Final Score
             │
             ▼
           Display
           Results
             │
             ▼
            Exit
```

---

## DATA FLOW EXAMPLES

### Example 1: Single Action Flow

```
┌─────────────────────────────────────┐
│ Agent Decision                      │
│ "Prioritize F001 - high impact"     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Create Action Object                │
│ Action(                             │
│   action_type="prioritize_feature"  │
│   feature_id="F001"                 │
│   reason="High impact..."           │
│ )                                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Environment.step(action)            │
│ 1. Validate action                  │
│ 2. Check feature exists             │
│ 3. Update state.prioritized         │
│ 4. Recalculate metrics              │
│ 5. Calculate reward components:     │
│    - High impact prioritization     │
│    - Clear justification            │
│    - Alignment with goals           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Reward Calculation                  │
│ Decision Quality:     0.8            │
│ Alignment:            0.9            │
│ Clipped Reward:       0.204 (max)   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Return Values                       │
│ observation: {...new state...}      │
│ reward:      {total: 0.204, ...}    │
│ done:        false (task continues) │
│ info:        {}                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Agent Receives Updated State        │
│ Ready for next step                 │
└─────────────────────────────────────┘
```

---

## SCENARIO LIFECYCLE

```
Scenario Start: task_001 + scenario_1_saas_analytics
│
├─ Load Scenario Data:
│  ├─ Business: SaaS Analytics
│  ├─ Churn Rate: 12%
│  ├─ Budget: $120,000
│  ├─ Team Capacity: 40 points/sprint
│  ├─ User Complaints: [238 about checkout, 156 about reports, ...]
│  ├─ Feature Backlog:
│  │  ├─ F001: One-Click Checkout (effort: 30)
│  │  ├─ F002: AI Recommendations (effort: 50)
│  │  ├─ F003: Advanced Analytics (effort: 60)
│  │  └─ ...
│  └─ Correct Prioritization: [F001, F002, F003]
│
├─ Load Task Definition:
│  ├─ Difficulty: Easy
│  ├─ Max Steps: 3
│  ├─ Objective: Identify #1 critical feature
│  └─ Success: Score 1.0 if correct
│
├─ Initialize Environment:
│  ├─ Set random seed
│  ├─ Create state object
│  ├─ Store initial metrics
│  └─ Reset step counter
│
├─ Agent Starts Decision Loop:
│  │
│  ├─ Step 1: request_info
│  │  └─ Reward: 0.020 (neutral)
│  │
│  ├─ Step 2: prioritize_feature(F001)
│  │  └─ Reward: 0.204 (correct, high-impact)
│  │
│  └─ Step 3: prioritize_feature(F002)
│     └─ Reward: 0.135 (additional good choice)
│
├─ Scenario Ends:
│  ├─ Total Reward: 0.359
│  ├─ Correct Prioritization: [F001, F002]
│  ├─ Grade: Correct top feature → grader_score: 1.0
│  └─ Final Score: 0.85 (98.5% of max possible)
│
└─ Results Logged and Displayed

Final Output:
[END] total_reward=0.359 grader_score=0.85 steps=3
```

---

## KEY METRICS EXPLAINED

```
total_reward
├─ Sum of all step rewards
├─ Range: Usually 0.0 - 1.0 (can exceed)
├─ Good: > 0.3
└─ Indicates: Quality of decisions

grader_score
├─ Task completion evaluation
├─ Range: 0.0 - 1.0
├─ Good: > 0.7
└─ Indicates: Correctness of final answer

reward per step
├─ Points for single action
├─ Range: -1.0 - 1.0
├─ Components: decision_quality + alignment
└─ Indicates: Individual decision merit

steps
├─ Number of actions taken
├─ Good: ≤ max_steps
├─ Example: task_001 max_steps = 3
└─ Indicates: Efficiency
```

---

This visual guide shows you exactly how every component works together! 🎨
