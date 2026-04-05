"""Main entry point for running the server locally."""

if __name__ == "__main__":
    import uvicorn
    from api.server import app
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
