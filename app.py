"""
OpenEnv AI Product Manager Server Entry Point

This is the root-level entry point for the OpenEnv hackathon.
The validator expects app.py at the repo root.
"""

from api.server import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
