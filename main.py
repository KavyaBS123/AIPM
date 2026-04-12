"""Main entry point for running the server locally or on HF Spaces."""

import os

if __name__ == "__main__":
    import uvicorn
    from api.server import app
    
    # Detect if running on HF Spaces
    is_hf_space = "SPACE_ID" in os.environ
    port = int(os.getenv("PORT", "7860" if is_hf_space else "8000"))
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
