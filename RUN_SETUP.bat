@echo off
REM AI Product Manager Environment - Setup and Run Script

echo ======================================================================
echo AI Product Manager Environment - Full Setup
echo ======================================================================

echo.
echo Step 1: Verify Environment...
python setup_verify.py

if errorlevel 1 (
    echo.
    echo ❌ Setup verification failed
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo Ready to Start!
echo ======================================================================
echo.
echo You can now run:
echo.
echo Option 1 - Start API Server:
echo   python main.py
echo.
echo Option 2 - Run Demo (no API needed):
echo   python demo.py
echo.
echo Option 3 - Run AI Inference (requires API server running):
echo   python inference.py task_001 scenario_1_saas_analytics
echo.
echo ======================================================================
pause
