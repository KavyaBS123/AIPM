"""
FastAPI Application for AI Product Manager Environment

Provides REST API endpoints for:
- Resetting environment with task/scenario
- Stepping through actions
- Querying current state
- Listing available tasks
- Health checks

Single global environment instance per session.
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import json
import traceback

from pm_env import (
    create_environment,
    ProductManagerEnv,
    Action,
    Observation,
    StepResult
)
from tasks import list_tasks, get_task


# =============================================================================
# Request/Response Models
# =============================================================================

class ResetRequest(BaseModel):
    """Request model for /reset endpoint"""
    task_id: str = Field(..., description="ID of task to run")
    scenario_id: Optional[str] = Field(None, description="Optional scenario ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "task_001",
                "scenario_id": "scenario_1_saas_analytics"
            }
        }


class StepRequest(BaseModel):
    """Request model for /step endpoint"""
    action_type: str = Field(..., description="Type: prioritize, reject, delay, finalize, or request_info")
    feature_id: Optional[str] = Field(None, description="Feature ID (required for prioritize/reject/delay)")
    justification: str = Field(..., description="Explanation for the action")
    
    class Config:
        json_schema_extra = {
            "example": {
                "action_type": "prioritize",
                "feature_id": "F001",
                "justification": "Highest user votes and retention impact"
            }
        }


class HealthResponse(BaseModel):
    """Response model for /health endpoint"""
    status: str = Field(..., description="Health status")
    environment_active: bool = Field(..., description="Whether environment is initialized")


class TaskInfo(BaseModel):
    """Task information in /tasks response"""
    task_id: str
    name: str
    difficulty: str
    description: str
    max_steps: int
    objective: str
    grader_class: str = Field(..., description="Grader class name for this task")


class StateResponse(BaseModel):
    """Response model for /state endpoint"""
    environment_active: bool
    current_task_id: Optional[str]
    current_scenario_id: Optional[str]
    observation: Optional[Dict[str, Any]]
    steps_taken: int
    total_reward: float


# =============================================================================
# Global State
# =============================================================================

app = FastAPI(
    title="AI Product Manager Environment API",
    description="REST API for the AI Product Manager environment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
_environment: Optional[ProductManagerEnv] = None
_current_task_id: Optional[str] = None
_current_scenario_id: Optional[str] = None
_steps_taken: int = 0
_total_reward: float = 0.0
_actions_taken: List[str] = []


# =============================================================================
# Helper Functions
# =============================================================================

def _reset_global_state():
    """Reset global tracking variables"""
    global _steps_taken, _total_reward, _actions_taken
    _steps_taken = 0
    _total_reward = 0.0
    _actions_taken = []


def _get_default_scenario(task_id: str) -> str:
    """Get default scenario based on task difficulty"""
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    # Map difficulties to default scenarios
    difficulty_map = {
        "easy": "scenario_1_saas_analytics",
        "medium": "scenario_2_ecommerce",
        "hard": "scenario_5_finance"
    }
    return difficulty_map.get(task.difficulty, "scenario_1_saas_analytics")


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        environment_active=_environment is not None
    )


@app.post("/reset", response_model=StateResponse)
async def reset(request: ResetRequest):
    """
    Reset the environment for a new task
    
    Args:
        request: ResetRequest with task_id and optional scenario_id
        
    Returns:
        StateResponse with initial observation and state
        
    Raises:
        HTTPException: If task_id not found or invalid
    """
    global _environment, _current_task_id, _current_scenario_id
    
    try:
        # Validate task exists
        task = get_task(request.task_id)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Task {request.task_id} not found")
        
        # Determine scenario
        scenario_id = request.scenario_id or _get_default_scenario(request.task_id)
        
        # Create environment
        _environment = create_environment(scenario_id, max_steps=task.max_steps)
        _current_task_id = request.task_id
        _current_scenario_id = scenario_id
        _reset_global_state()
        
        # Reset environment
        observation = _environment.reset()
        
        return StateResponse(
            environment_active=True,
            current_task_id=_current_task_id,
            current_scenario_id=_current_scenario_id,
            observation=observation.model_dump(),
            steps_taken=_steps_taken,
            total_reward=_total_reward
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error resetting environment: {str(e)}"
        )


@app.post("/step", response_model=StateResponse)
async def step(request: StepRequest):
    """
    Execute one step in the environment
    
    Args:
        request: StepRequest with action details
        
    Returns:
        StateResponse with new observation and result
        
    Raises:
        HTTPException: If environment not initialized or action invalid
    """
    global _environment, _steps_taken, _total_reward, _actions_taken
    
    if _environment is None:
        raise HTTPException(
            status_code=400,
            detail="Environment not initialized. Call /reset first."
        )
    
    try:
        # Create action
        action = Action(
            action_type=request.action_type,
            feature_id=request.feature_id,
            justification=request.justification
        )
        
        # Execute step
        result: StepResult = _environment.step(action)
        
        # Update tracking
        _steps_taken += 1
        _total_reward += result.reward
        _actions_taken.append(f"{action.action_type}:{action.feature_id or 'N/A'}")
        
        return StateResponse(
            environment_active=True,
            current_task_id=_current_task_id,
            current_scenario_id=_current_scenario_id,
            observation=result.observation.model_dump(),
            steps_taken=_steps_taken,
            total_reward=_total_reward
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid action: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error executing step: {str(e)}\n{traceback.format_exc()}"
        )


@app.get("/state", response_model=StateResponse)
async def get_state():
    """
    Get current state without modifying it
    
    Returns:
        StateResponse with current state
    """
    if _environment is None:
        return StateResponse(
            environment_active=False,
            current_task_id=None,
            current_scenario_id=None,
            observation=None,
            steps_taken=0,
            total_reward=0.0
        )
    
    return StateResponse(
        environment_active=True,
        current_task_id=_current_task_id,
        current_scenario_id=_current_scenario_id,
        observation=_environment.state().model_dump(),
        steps_taken=_steps_taken,
        total_reward=_total_reward
    )


@app.get("/tasks", response_model=List[TaskInfo])
async def get_tasks():
    """
    Get list of all available tasks
    
    Returns:
        List of TaskInfo objects with task details and graders
    """
    try:
        tasks = list_tasks()
        return [
            TaskInfo(
                task_id=task.task_id,
                name=task.name,
                difficulty=task.difficulty,
                description=task.description,
                max_steps=task.max_steps,
                objective=task.objective,
                grader_class=task.grader_class
            )
            for task in tasks
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching tasks: {str(e)}"
        )


# =============================================================================
# Root Endpoint
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AI Product Manager Environment API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health - Health check",
            "reset": "POST /reset - Initialize environment for task",
            "step": "POST /step - Execute action",
            "state": "GET /state - Get current state",
            "tasks": "GET /tasks - List available tasks",
            "docs": "GET /docs - Interactive API documentation"
        }
    }


# =============================================================================
# Application Entry Point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
