"""FastAPI server for AI Product Manager Environment."""

from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from env import create_environment, ProductManagerEnvironment
from models import Action, Observation, Reward

# Global environment instance
_env_instance: Optional[ProductManagerEnvironment] = None


class ResetRequest(BaseModel):
    """Request to reset environment."""
    scenario_key: str = "scenario_1_ecommerce"
    task_id: Optional[str] = None
    seed: int = 42


class ResetResponse(BaseModel):
    """Response from reset endpoint."""
    observation: Observation
    info: Dict[str, Any]


class StepRequest(BaseModel):
    """Request to step environment."""
    action: Action


class StepResponse(BaseModel):
    """Response from step endpoint."""
    observation: Observation
    reward: Reward
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
        _env_instance = create_environment()
    
    @app.post("/reset", response_model=ResetResponse, tags=["Environment"])
    async def reset(request: ResetRequest = Body(...)) -> ResetResponse:
        """
        Reset the environment to initial state.
        
        Args:
            request: Reset request with scenario and task configuration
        
        Returns:
            Initial observation and info
        """
        global _env_instance
        
        _env_instance = create_environment(
            scenario_key=request.scenario_key,
            task_id=request.task_id,
            seed=request.seed,
        )
        
        observation = _env_instance.reset()
        
        return ResetResponse(
            observation=observation,
            info={
                "message": "Environment reset",
                "scenario": request.scenario_key,
                "task": request.task_id,
            },
        )
    
    @app.post("/step", response_model=StepResponse, tags=["Environment"])
    async def step(request: StepRequest) -> StepResponse:
        """
        Execute one step in the environment.
        
        Args:
            request: Step request with action
        
        Returns:
            Observation, reward, done flag, and info
        """
        global _env_instance
        
        if _env_instance is None:
            raise HTTPException(
                status_code=400,
                detail="Environment not initialized. Call /reset first."
            )
        
        observation, reward, done, info = _env_instance.step(request.action)
        
        return StepResponse(
            observation=observation,
            reward=reward,
            done=done,
            info=info,
        )
    
    @app.get("/state", response_model=StateResponse, tags=["Environment"])
    async def state() -> StateResponse:
        """
        Get the current state of the environment.
        
        Returns:
            Current environment state
        """
        global _env_instance
        
        if _env_instance is None:
            raise HTTPException(
                status_code=400,
                detail="Environment not initialized. Call /reset first."
            )
        
        return StateResponse(state=_env_instance.state_dict())
    
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
            },
        }
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
