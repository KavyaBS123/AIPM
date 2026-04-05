"""FastAPI server for AI Product Manager Environment."""

from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from pm_env.environment import ProductManagerEnv
from pm_env.models import Action, Observation

# Global environment instance
_env_instance: Optional[ProductManagerEnv] = None


class ResetRequest(BaseModel):
    """Request to reset environment."""
    scenario_key: str = "scenario_1_ecommerce"
    task_id: Optional[str] = None
    seed: int = 42


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
    async def reset(request: ResetRequest = Body(...)) -> ResetResponse:
        """Reset the environment to initial state."""
        global _env_instance
        
        try:
            _env_instance = ProductManagerEnv()
            observation = _env_instance.reset()
            
            return ResetResponse(
                observation={"status": "reset"} if not isinstance(observation, dict) else observation,
                info={
                    "message": "Environment reset",
                    "scenario": request.scenario_key,
                    "task": request.task_id,
                },
            )
        except Exception as e:
            return ResetResponse(
                observation={"status": "reset"},
                info={"message": "Environment reset", "error": str(e)},
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
        if isinstance(result, tuple) and len(result) == 4:
            observation, reward, done, info = result
        else:
            observation = result.get("observation") if isinstance(result, dict) else None
            reward = result.get("reward", 0.0) if isinstance(result, dict) else 0.0
            done = result.get("done", False) if isinstance(result, dict) else False
            info = result.get("info", {}) if isinstance(result, dict) else {}
        
        return StepResponse(
            observation=observation if isinstance(observation, dict) else None,
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
