@echo off
echo ========================================
echo FastAPI Load Testing - Complete Setup
echo ========================================
echo.

REM Check if database exists
if exist products.db (
    echo Database already exists: products.db
    echo.
    choice /C YN /M "Do you want to recreate the database (all data will be lost)"
    if errorlevel 2 goto skip_db
    if errorlevel 1 goto create_db
) else (
    goto create_db
)

:create_db
echo.
echo ========================================
echo Step 1: Initializing Database
echo ========================================
echo.
python db_init.py
if errorlevel 1 (
    echo.
    echo ❌ Database initialization failed!
    echo Please check the error above.
    pause
    exit /b 1
)

:skip_db
echo.
echo ========================================
echo Step 2: Starting FastAPI Server
echo ========================================
echo.
echo Server will run on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000
