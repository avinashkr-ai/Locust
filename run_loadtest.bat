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
echo Opening browser...
timeout /t 2 /nobreak > nul
start http://localhost:8089
echo.
echo Starting Locust...
echo.

locust -f locustfile.py --host=http://localhost:8000
