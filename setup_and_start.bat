@echo off
echo ========================================
echo FastAPI Load Testing - Complete Setup
echo ========================================
echo.

REM ----------------------------------------
REM Step 0: Ensure virtualenv and dependencies
REM ----------------------------------------

REM Prefer python, fall back to py if needed
where python >nul 2>&1
if errorlevel 1 (
    where py >nul 2>&1
    if errorlevel 1 (
        echo ❌ Neither "python" nor "py" was found on PATH.
        echo Please install Python 3.8+ and try again.
        pause
        exit /b 1
    ) else (
        set "PYTHON_CMD=py"
    )
) else (
    set "PYTHON_CMD=python"
)

echo Using Python interpreter: %PYTHON_CMD%
echo.

REM Create virtual environment if it does not exist
if not exist .venv (
    echo ========================================
    echo Step 0: Creating virtual environment (.venv)
    echo ========================================
    echo.
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment ".venv" already exists. Skipping creation.
    echo.
)

REM Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else (
    echo ❌ Could not find venv activation script at .venv\Scripts\activate.bat
    pause
    exit /b 1
)

REM Ensure required libraries are installed
if exist requirements.txt (
    echo ========================================
    echo Step 0: Ensuring Python dependencies from requirements.txt
    echo ========================================
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install required Python packages.
        pause
        exit /b 1
    )
) else (
    echo ⚠️ requirements.txt not found. Skipping dependency installation.
    echo.
)

REM ----------------------------------------
REM Step 1: Database initialization
REM ----------------------------------------

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
%PYTHON_CMD% db_init.py
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
