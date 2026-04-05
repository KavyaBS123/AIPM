@echo off
REM Start API Server

cd /d "%~dp0"

echo ======================================================================
echo Starting API Server...
echo ======================================================================
echo.
echo API will run on: http://localhost:8000
echo API Docs will be at: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
echo Press CTRL+C to stop the server
echo.
echo ======================================================================
echo.

python main.py
