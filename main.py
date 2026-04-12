"""Main entry point for running the server locally or on HF Spaces."""

import os
import sys

if __name__ == "__main__":
    import uvicorn
    from api.server import app
    
    # Detect if running on HF Spaces
    is_hf_space = "SPACE_ID" in os.environ
    # Explicitly use PORT env var first, then HF Spaces (7860), then default to 8000
    port = int(os.getenv("PORT", "7860" if is_hf_space else "8000"))
    
    # Log startup info
    print(f"[INFO] Starting server on port {port} (HF Space: {is_hf_space})", file=sys.stderr)
    print(f"[INFO] Health check endpoint: http://0.0.0.0:{port}/health", file=sys.stderr)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
