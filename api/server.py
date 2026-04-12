"""FastAPI server for AI Product Manager Environment."""

from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from pm_env.environment import ProductManagerEnv
from pm_env.models import Action, Observation
from scenarios.data import SCENARIOS

# Global environment instance
_env_instance: Optional[ProductManagerEnv] = None


class ResetRequest(BaseModel):
    """Request to reset environment."""
    scenario_id: Optional[str] = None  # Accept scenario_id from inference script
    scenario_key: Optional[str] = "scenario_1_ecommerce"  # Default scenario
    task_id: Optional[str] = None
    seed: Optional[int] = 42


class ResetResponse(BaseModel):
    """Response from reset endpoint."""
    observation: Optional[Dict[str, Any]] = None
    info: Dict[str, Any]


class StepRequest(BaseModel):
    """Request to step environment."""
    action: Action


class StepResponse(BaseModel):
    """Response from step endpoint."""
    observation: Optional[Dict[str, Any]] = None
    reward: float
    done: bool
    info: Dict[str, Any]


class StateResponse(BaseModel):
    """Response from state endpoint."""
    state: Dict[str, Any]


def create_app() -> FastAPI:
    """Create and configure FastAPI app."""
    app = FastAPI(
        title="AI Product Manager Environment",
        description="OpenEnv-compatible environment for simulating product manager decisions",
        version="1.0.0",
    )
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize environment on startup."""
        global _env_instance
        _env_instance = ProductManagerEnv()
    
    @app.post("/reset", response_model=ResetResponse, tags=["Environment"])
    async def reset(request: Optional[ResetRequest] = Body(None)) -> ResetResponse:
        """Reset the environment to initial state."""
        global _env_instance
        
        # Use provided request or create default
        if request is None:
            request = ResetRequest()
        
        # Determine which scenario to use
        scenario_key = request.scenario_id or request.scenario_key or "scenario_1_ecommerce"
        
        # Map human-readable names to actual scenario keys if needed
        scenario_mapping = {
            "scenario_1_saas_analytics": "scenario_2_saas",  # Map legacy name
            "scenario_1_ecommerce": "scenario_1_ecommerce",
            "scenario_2_saas": "scenario_2_saas",
            "scenario_3_social": "scenario_3_social",
        }
        
        # Use mapped name if available, otherwise use as-is
        if scenario_key in scenario_mapping:
            scenario_key = scenario_mapping[scenario_key]
        
        if scenario_key not in SCENARIOS:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown scenario: {scenario_key}. Available: {list(SCENARIOS.keys())}"
            )
        
        try:
            scenario_data = SCENARIOS[scenario_key]
            
            # Create and initialize environment with scenario data
            _env_instance = ProductManagerEnv(scenario_data=scenario_data)
            observation = _env_instance.reset()
            
            # Convert observation to dict if needed
            obs_dict = observation.dict() if hasattr(observation, 'dict') else observation
            
            return ResetResponse(
                observation=obs_dict,
                info={
                    "message": "Environment reset successfully",
                    "scenario": scenario_key,
                    "task": request.task_id,
                },
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to reset environment: {str(e)}"
            )
    
    @app.post("/step", response_model=StepResponse, tags=["Environment"])
    async def step(request: StepRequest) -> StepResponse:
        """Execute one step in the environment."""
        global _env_instance
        
        if _env_instance is None:
            raise HTTPException(
                status_code=400,
                detail="Environment not initialized. Call /reset first."
            )
        
        result = _env_instance.step(request.action)
        
        # Handle different return types
        # Result should be a StepResult object
        if hasattr(result, 'reward'):  # It's a StepResult object
            observation = result.observation
            reward = result.reward
            done = result.done
            info = result.info
            # Convert observation to dict if needed
            obs_dict = observation.dict() if hasattr(observation, 'dict') else observation
        elif isinstance(result, tuple) and len(result) == 4:
            observation, reward, done, info = result
            obs_dict = observation if isinstance(observation, dict) else observation.dict() if hasattr(observation, 'dict') else None
        elif isinstance(result, dict):
            obs_dict = result.get("observation")
            reward = result.get("reward", 0.0)
            done = result.get("done", False)
            info = result.get("info", {})
        else:
            obs_dict = None
            reward = 0.0
            done = False
            info = {}
        
        return StepResponse(
            observation=obs_dict,
            reward=float(reward),
            done=bool(done),
            info=info if isinstance(info, dict) else {},
        )
    
    @app.get("/state", response_model=StateResponse, tags=["Environment"])
    async def state() -> StateResponse:
        """Get the current state of the environment."""
        global _env_instance
        
        if _env_instance is None:
            raise HTTPException(
                status_code=400,
                detail="Environment not initialized. Call /reset first."
            )
        
        state_dict = _env_instance.state_dict() if hasattr(_env_instance, 'state_dict') else {}
        return StateResponse(state=state_dict)
    
    @app.get("/", tags=["Root"])
    async def root() -> Dict[str, Any]:
        """Root endpoint - returns service info and links to other endpoints."""
        return {
            "service": "AI Product Manager Environment",
            "status": "running",
            "version": "1.0.0",
            "openenv_compatible": True,
            "available_endpoints": {
                "root": "GET /",
                "health": "GET /health",
                "info": "GET /info",
                "reset": "POST /reset",
                "step": "POST /step",
                "state": "GET /state",
            },
        }
    
    @app.get("/health", tags=["Health"])
    async def health() -> Dict[str, str]:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "AI Product Manager Environment",
        }
    
    @app.get("/info", tags=["Info"])
    async def info() -> Dict[str, Any]:
        """Get information about the environment."""
        return {
            "name": "AI Product Manager Environment",
            "version": "1.0.0",
            "openenv_compatible": True,
            "endpoints": {
                "reset": "POST /reset",
                "step": "POST /step",
                "state": "GET /state",
                "health": "GET /health",
                "info": "GET /info",
                "validate": "GET /validate",
                "manifest": "GET /manifest",
                "tasks": "GET /tasks",
            },
        }
    
    @app.get("/validate", tags=["Validation"])
    async def validate() -> Dict[str, Any]:
        """
        Phase 2 Validation Endpoint: Confirm at least 3 tasks with graders
        
        This is the CRITICAL endpoint that the Meta Hackathon validator checks.
        Returns: {validation_status: 'PASS'/'FAIL', error_message: '...', tasks_with_graders_count: N}
        """
        try:
            from tasks import list_tasks
            from graders import EasyTaskGrader, MediumTaskGrader, HardTaskGrader
            
            tasks = list_tasks()
            grader_map = {
                'EasyTaskGrader': EasyTaskGrader,
                'MediumTaskGrader': MediumTaskGrader,
                'HardTaskGrader': HardTaskGrader
            }
            
            tasks_with_graders = []
            for task in tasks:
                if hasattr(task, 'grader_class') and task.grader_class:
                    grader_class = grader_map.get(task.grader_class)
                    if grader_class:
                        try:
                            grader = grader_class()
                            tasks_with_graders.append({
                                'task_id': task.task_id,
                                'name': task.name,
                                'difficulty': task.difficulty,
                                'grader_class': task.grader_class,
                                'grader_available': True
                            })
                        except Exception:
                            pass
            
            has_minimum_tasks = len(tasks_with_graders) >= 3
            
            return {
                'validation_status': 'PASS' if has_minimum_tasks else 'FAIL',
                'tasks_with_graders_count': len(tasks_with_graders),
                'required_count': 3,
                'tasks_with_graders': tasks_with_graders,
                'error_message': None if has_minimum_tasks else 'Not enough tasks with graders'
            }
        except Exception as e:
            return {
                'validation_status': 'ERROR',
                'error_message': str(e)
            }
    
    @app.get("/tasks", tags=["Validation"])
    async def get_tasks() -> list:
        """
        Get list of all available tasks with grader information
        Used by validator to confirm graders are present
        """
        try:
            from tasks import list_tasks
            
            tasks = list_tasks()
            return [
                {
                    'task_id': task.task_id,
                    'name': task.name,
                    'difficulty': task.difficulty,
                    'description': task.description,
                    'grader_class': getattr(task, 'grader_class', None)
                }
                for task in tasks
            ]
        except Exception as e:
            return {'error': str(e)}
    
    @app.get("/manifest", tags=["Validation"])
    async def get_manifest() -> Dict[str, Any]:
        """
        Explicit grader manifest - lists all tasks with their graders
        This is the definitive source for grader availability
        """
        try:
            from grader_manifest import get_tasks_with_graders, validate_grader_setup
            
            result = validate_grader_setup()
            return {
                'validation_status': result.get('validation_status'),
                'total_tasks': result.get('total_tasks'),
                'tasks_with_graders': result.get('tasks_with_graders'),
                'minimum_required': result.get('minimum_required'),
                'all_graders_valid': result.get('all_graders_valid'),
                'tasks': result.get('tasks', [])
            }
        except Exception as e:
            return {
                'validation_status': 'ERROR',
                'error': str(e)
            }
    
    return app


app = create_app()


def main():
    """Entry point for running the server."""
    import uvicorn
    port = 7860  # HF Spaces default, or 8000 for local
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
