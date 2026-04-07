"""
OpenEnv AI Product Manager - Root Entry Point for HF Spaces

This is for HF Spaces compatibility.
The actual server implementation is in server/app.py
"""

from server.app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
