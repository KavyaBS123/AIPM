#!/usr/bin/env python3
"""
OpenEnv AI Product Manager Inference Script

Runs an AI agent (via OpenAI API) against the AI Product Manager environment.

Usage:
    python inference.py task_001 scenario_1_saas_analytics
    
Expected Output Format:
    [START] task=task_001 env=openenv-aipm model=gpt-4o
    [STEP] step=1 action=prioritize_feature feature=F001 reward=0.20 done=false error=null
    [STEP] step=2 action=prioritize_feature feature=F004 reward=0.15 done=false error=null
    [STEP] step=3 action=finalize_roadmap feature=null reward=0.25 done=true error=null
    [END] success=true steps=3 score=0.60 rewards=0.20,0.15,0.25

Environment Variables:
    API_BASE_URL: Environment API endpoint (default: http://localhost:8000)
    OPENAI_API_KEY: OpenAI API key (for GPT inference)
    GROQ_API_KEY: Groq API key (fallback if OpenAI not available)
    MODEL_NAME: Override model name (default: gpt-4o)
"""

import asyncio
import json
import os
import sys
from typing import Optional, Dict, Any, List

import httpx
from dotenv import load_dotenv

# Load environment
load_dotenv()

# ============================================================================
# Configuration
# ============================================================================

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral-large-latest")

# Choose provider - PRIORITY: Mistral (OpenAI-compatible) > OpenAI > Groq > Fallback
USE_MISTRAL = bool(MISTRAL_API_KEY)
USE_OPENAI = bool(OPENAI_API_KEY) and not USE_MISTRAL
USE_GROQ = bool(GROQ_API_KEY) and not USE_MISTRAL and not USE_OPENAI
USE_FALLBACK = not USE_MISTRAL and not USE_OPENAI and not USE_GROQ

if USE_FALLBACK:
    print("[WARNING] No API key configured. Using fallback heuristic strategy.", file=sys.stderr)

MAX_STEPS = 10
TEMPERATURE = 0.5
MAX_TOKENS = 500


# ============================================================================
# LLM API Calls
# ============================================================================

async def call_llm(messages: list) -> str:
    """Call LLM API (Mistral, OpenAI, Groq, or Fallback) with the given messages."""
    
    if USE_MISTRAL:
        return await call_mistral(messages)
    elif USE_OPENAI:
        return await call_openai(messages)
    elif USE_GROQ:
        # Groq is sync, but wrap in async
        return await asyncio.to_thread(call_groq_sync, messages)
    else:
        # Fallback: use heuristic strategy
        return await call_fallback(messages)


async def call_mistral(messages: list) -> str:
    """Call Mistral API using OpenAI-compatible client."""
    try:
        from openai import OpenAI
    except ImportError:
        raise Exception("openai package not installed. Run: pip install openai")
    
    if not MISTRAL_API_KEY:
        raise Exception("MISTRAL_API_KEY not configured")
    
    # Mistral is OpenAI-compatible
    client = OpenAI(
        api_key=MISTRAL_API_KEY,
        base_url="https://api.mistral.ai/v1"
    )
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Mistral API error: {str(e)}")


async def call_openai(messages: list) -> str:
    """Call OpenAI API using openai Client."""
    try:
        from openai import OpenAI
    except ImportError:
        raise Exception("openai package not installed. Run: pip install openai")
    
    if not OPENAI_API_KEY:
        raise Exception("OPENAI_API_KEY not configured")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")


def call_groq_sync(messages: list) -> str:
    """Call Groq API using groq Client (synchronous)."""
    try:
        from groq import Groq
    except ImportError:
        raise Exception("groq package not installed. Run: pip install groq")
    
    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY not configured")
    
    client = Groq(api_key=GROQ_API_KEY)
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Groq API error: {str(e)}")


async def call_fallback(messages: list) -> str:
    """Fallback strategy when no API key is available.
    
    Uses heuristics to make decisions based on the observation.
    Extracts features and their vote counts, then strategically prioritizes.
    """
    # Parse the last user message to extract features and votes
    last_message = messages[-1]["content"] if messages else ""
    
    # Try to parse features from the prompt
    features_data = []
    if "AVAILABLE FEATURES" in last_message:
        features_section = last_message.split("AVAILABLE FEATURES")[1].split("CONSTRAINTS")[0]
        for line in features_section.split("\n"):
            if "[F" in line and "Votes:" in line:
                # Extract feature ID and votes
                try:
                    feature_id = line.split("[")[1].split("]")[0]
                    votes_str = line.split("Votes: ")[1].split(",")[0]
                    votes = int(votes_str)
                    features_data.append((feature_id, votes))
                except:
                    pass
    
    # Strategy: Prioritize highest vote features first, then finalize
    decision_count = len([m for m in messages if m["role"] == "user"]) - 1
    
    if features_data:
        # Sort by votes descending
        features_data.sort(key=lambda x: x[1], reverse=True)
        
        if decision_count < 2:
            # Prioritize the top feature
            feature_id, votes = features_data[0]
            return json.dumps({
                "action_type": "prioritize",
                "feature_id": feature_id,
                "justification": f"Highest user demand with {votes} votes. Strategic priority."
            })
        elif decision_count == 2:
            # Finalize to lock in decisions
            return json.dumps({
                "action_type": "finalize",
                "feature_id": None,
                "justification": "Finalizing roadmap after strategic prioritization."
            })
        else:
            # Reject or delay lower priority features
            return json.dumps({
                "action_type": "reject",
                "feature_id": features_data[-1][0],
                "justification": "Focusing on high-impact features."
            })
    else:
        # Default fallback if we can't parse features
        return json.dumps({
            "action_type": "request_info",
            "feature_id": None,
            "justification": "Analyzing current status to make informed decision."
        })


# ============================================================================
# Environment Interaction
# ============================================================================

async def reset_environment(
    task_id: str,
    scenario_id: Optional[str] = None
) -> Dict[str, Any]:
    """Reset environment and return initial observation."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/reset",
            json={
                "task_id": task_id,
                "scenario_id": scenario_id,
            }
        )
        if response.status_code != 200:
            raise Exception(f"Reset failed: {response.text}")
        return response.json()


async def step_environment(
    action_type: str,
    feature_id: Optional[str],
    justification: str
) -> Dict[str, Any]:
    """Execute one step in environment."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/step",
            json={
                "action": {
                    "action_type": action_type,
                    "feature_id": feature_id,
                    "justification": justification,
                }
            }
        )
        if response.status_code != 200:
            error_detail = response.json().get("detail", "Unknown error")
            return {
                "error": str(error_detail),
                "observation": None,
                "reward": {"step_reward": 0.0, "total_reward": 0.0},
                "done": False,
            }
        return response.json()


async def get_environment_state() -> Dict[str, Any]:
    """Get final environment state (for scoring)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/state")
        if response.status_code != 200:
            raise Exception(f"State fetch failed: {response.text}")
        return response.json()


# ============================================================================
# Prompt Building
# ============================================================================

def build_system_prompt() -> str:
    """System prompt for product manager task."""
    return """You are an expert Product Manager AI making strategic decisions about feature prioritization.

SCORING FORMULA (Higher is better):
CRITICALITY = (user_votes / 1000 × 0.30) + (satisfaction_impact × 0.40) + (churn_reduction × 0.30)

STRATEGY:
1. FIRST: Always prioritize the feature with HIGHEST user votes (highest demand)
2. SECOND: Prioritize features with highest satisfaction impact
3. THIRD: Prioritize features that reduce churn most
4. FINAL STEP: After 2-3 prioritizations, call finalize_roadmap to lock in decisions and earn completion bonus

EXAMPLES OF GOOD DECISIONS:
- High votes (180+) = Prioritize immediately → High reward (0.40+)
- Medium votes (100-150) = Second priority → Medium-high reward (0.28+)
- Low votes (50-100) = Delay or reject → Lower reward (0.0-0.1)
- After good picks: Finalize to earn bonus

CRITICAL: You must respond ONLY with valid JSON (no markdown, no explanation).

Response format:
{
    "action_type": "prioritize" | "reject" | "delay" | "request_info" | "finalize",
    "feature_id": "F001" (required for prioritize/reject/delay) or null (for finalize/request_info),
    "justification": "Brief explanation (1-2 sentences). For prioritize: mention why important. For finalize: mention strategy executed"
}"""


def build_user_prompt(step: int, observation: Dict[str, Any], previous_decisions: list) -> str:
    """Build user prompt from observation."""
    
    if observation is None:
        observation = {}
    
    # Handle both legacy and new observation formats
    # New format (from API):
    feedback = observation.get("user_complaints", [])
    if isinstance(feedback, list):
        feedback = "\n".join([f"  - {c}" for c in feedback]) or "No complaints"
    
    metrics = observation.get("metrics", {})
    if isinstance(metrics, dict):
        churn_rate = metrics.get('churn_rate', 0)
        retention_rate = metrics.get('retention_rate', 0)
        user_satisfaction = metrics.get('user_satisfaction', 0)
        revenue_growth = metrics.get('revenue_growth', 0)
    else:
        churn_rate = retention_rate = user_satisfaction = revenue_growth = 0
    
    features = observation.get("feature_backlog", [])
    if isinstance(features, list):
        features_text = "\n".join([
            f"  - [{f.get('id', 'F?')}] {f.get('name', 'Unknown')} (Votes: {f.get('votes', 0)}, Effort: {f.get('effort', 1)}/5)"
            if isinstance(f, dict) else str(f)
            for f in features
        ]) or "No features"
    else:
        features_text = str(features)
    
    constraints = observation.get("constraints", {})
    if isinstance(constraints, dict):
        constraints_text = "\n".join([
            f"  - {k}: {v}"
            for k, v in constraints.items()
        ]) or "No constraints"
    else:
        constraints_text = str(constraints)
    
    decisions_text = ""
    if previous_decisions:
        decisions_text = "Previous decisions:\n"
        for d in previous_decisions[-3:]:  # Last 3 decisions
            decisions_text += f"  - {d}\n"
        decisions_text += "\n"
    
    strategy_hint = ""
    if step <= 2:
        strategy_hint = "\n⚠️  IMMEDIATE ACTION: Pick the HIGHEST demand feature (most user votes) to maximize reward."
    elif step == 3:
        strategy_hint = "\n⚠️  FINAL STEP: Call 'finalize_roadmap' to lock in decisions and earn completion bonus!"
    
    return f"""Step {step}/{MAX_STEPS}

USER FEEDBACK:
{feedback}

BUSINESS METRICS:
- Churn: {churn_rate:.1%}
- Retention: {retention_rate:.1%}
- User Satisfaction: {user_satisfaction:.1f}/100
- Revenue Growth: {revenue_growth:.1f}%

AVAILABLE FEATURES (RANK BY VOTES):
{features_text}

CONSTRAINTS:
{constraints_text}

{decisions_text}{strategy_hint}

Make your next strategic decision."""


# ============================================================================
# Response Parsing
# ============================================================================

def parse_action(response_text: str) -> Dict[str, Any]:
    """Parse LLM response into action."""
    try:
        # Extract JSON
        json_str = response_text.strip()
        if json_str.startswith("```"):
            json_str = json_str.split("```")[1]
            if json_str.startswith("json"):
                json_str = json_str[4:]
            json_str = json_str.strip()
        
        data = json.loads(json_str)
        
        # Validate
        if "action_type" not in data:
            raise ValueError("Missing action_type")
        if "justification" not in data:
            raise ValueError("Missing justification")
        
        action_type = data["action_type"]
        feature_id = data.get("feature_id")
        justification = data["justification"]
        
        # Validate action_type
        valid_types = [
            "prioritize",
            "reject",
            "delay",
            "request_info",
            "finalize",
        ]
        if action_type not in valid_types:
            raise ValueError(f"Invalid action_type: {action_type}")
        
        return {
            "action_type": action_type,
            "feature_id": feature_id,
            "justification": justification,
            "error": None,
        }
    except Exception as e:
        return {
            "error": str(e),
            "action_type": None,
            "feature_id": None,
            "justification": None,
        }


# ============================================================================
# Main Inference Loop
# ============================================================================

async def run_inference(task_id: str, scenario_id: Optional[str] = None) -> None:
    """Run full inference episode."""
    
    # Determine provider
    provider = "openai" if USE_OPENAI else "groq"
    
    print(f"[START] task={task_id} env=openenv-aipm model={MODEL_NAME}")
    
    try:
        # Reset
        reset_data = await reset_environment(task_id, scenario_id)
        observation = reset_data["observation"]
        current_scenario = reset_data["info"].get("scenario", scenario_id or "unknown")
        
        # Initialize tracking
        step_num = 1
        steps_rewards: List[float] = []
        previous_decisions: List[str] = []
        success = False
        done = False
        error = None
        
        # Build messages
        system_prompt = build_system_prompt()
        messages = [{"role": "system", "content": system_prompt}]
        
        # Step loop
        while not done and step_num <= MAX_STEPS:
            # Build user prompt
            user_prompt = build_user_prompt(step_num, observation, previous_decisions)
            messages.append({"role": "user", "content": user_prompt})
            
            # Get LLM response
            try:
                response_text = await call_llm(messages)
                parsed = parse_action(response_text)
                
                if parsed["error"]:
                    # Parsing failed, use default action
                    action_type = "request_more_info"
                    feature_id = None
                    justification = f"[Parse error: {parsed['error']}]"
                    error = parsed["error"]
                else:
                    action_type = parsed["action_type"]
                    feature_id = parsed["feature_id"]
                    justification = parsed["justification"]
                    messages.append({"role": "assistant", "content": response_text})
            
            except Exception as e:
                # API error
                action_type = "request_more_info"
                feature_id = None
                justification = "[API error]"
                error = str(e)
            
            # Execute step
            step_data = await step_environment(action_type, feature_id, justification)
            
            if "error" in step_data and step_data["error"]:
                # Environment error
                reward = 0.0
                error = step_data["error"]
            else:
                observation = step_data.get("observation", {})
                # Extract reward (it's a float, not a dict)
                reward = step_data.get("reward", 0.0)
                if isinstance(reward, dict):
                    # Fallback if reward is a dict
                    reward = reward.get("total_reward", 0.0)
                done = step_data.get("done", False)
            
            steps_rewards.append(reward)
            previous_decisions.append(f"{action_type}({feature_id or 'N/A'})")
            
            # Log step
            print(
                f"[STEP] step={step_num} "
                f"action={action_type} "
                f"feature={feature_id or 'null'} "
                f"reward={reward:.2f} "
                f"done={str(done).lower()} "
                f"error={error or 'null'}"
            )
            
            step_num += 1
        
        # Get final state and score
        try:
            final_state = (await get_environment_state())["state"]
            final_score = final_state.get("grader_score", 0.0)
            success = final_score >= 0.36  # Threshold for success (was 0.25, now 0.36)
        except:
            final_score = 0.0
            success = False
        
        # Log end
        rewards_str = ",".join(f"{r:.2f}" for r in steps_rewards)
        total_reward = sum(steps_rewards)
        
        print(
            f"[END] success={str(success).lower()} "
            f"steps={step_num - 1} "
            f"score={final_score:.2f} "
            f"rewards={rewards_str}"
        )
    
    except Exception as e:
        error_msg = str(e)
        print(
            f"[END] success=false steps=0 score=0.00 rewards=",
            file=sys.stderr
        )
        print(f"[ERROR] {error_msg}", file=sys.stderr)
        sys.exit(1)


# ============================================================================
# Entry Point
# ============================================================================

async def main():
    """Main entry point."""
    task_id = sys.argv[1] if len(sys.argv) > 1 else "task_001"
    scenario_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    await run_inference(task_id, scenario_id)


if __name__ == "__main__":
    asyncio.run(main())
