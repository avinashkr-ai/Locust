@echo off
echo ========================================
echo Starting Locust Load Test
echo ========================================
echo.
echo Make sure FastAPI server is running on http://localhost:8000
echo.
echo Locust Web UI will open on: http://localhost:8089
echo ========================================
echo.

REM Activate virtual environment if present so "locust" is available
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else (
    echo ⚠️ Virtual environment ".venv" not found. Attempting to run with system Python.
    echo    If you see "locust is not recognized", run setup_and_start.bat once to create the .venv.
)

echo Opening browser...
timeout /t 2 /nobreak > nul
start http://localhost:8089
echo.
echo Starting Locust...
echo.

locust -f locustfile.py --host=http://localhost:8000
