"""
OpenEnv AI Product Manager Server - Main Entry Point

This is the server entry point expected by OpenEnv validator.
Located at: server/app.py
"""

from api.server import create_app
import uvicorn

# Create the FastAPI app instance
app = create_app()


def main():
    """Main entry point for running the server."""
    port = 7860  # HF Spaces default, or 8000 for local
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
