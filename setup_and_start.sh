#!/bin/bash

echo "========================================"
echo "FastAPI Load Testing - Complete Setup"
echo "========================================"
echo ""

#
# Step 0: Ensure Python, virtual environment, and dependencies
#

# Detect Python command
PYTHON_CMD="python3"
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
    PYTHON_CMD="python"
fi

if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
    echo "❌ Python is not installed or not on PATH."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

echo "Using Python interpreter: $PYTHON_CMD"
echo ""

# Create virtual environment if it does not exist
if [ ! -d "venv" ]; then
    echo "========================================"
    echo "Step 0: Creating virtual environment (venv)"
    echo "========================================"
    echo ""
    "$PYTHON_CMD" -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment."
        exit 1
    fi
else
    echo "Virtual environment 'venv' already exists. Skipping creation."
    echo ""
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
else
    echo "❌ Could not find venv activation script at venv/bin/activate."
    exit 1
fi

# Ensure required libraries are installed
if [ -f "requirements.txt" ]; then
    echo "========================================"
    echo "Step 0: Ensuring Python dependencies from requirements.txt"
    echo "========================================"
    echo ""
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install required Python packages."
        exit 1
    fi
else
    echo "⚠️ requirements.txt not found. Skipping dependency installation."
    echo ""
fi

#
# Step 1: Initialize database (if needed)
#

# Check if database exists
if [ -f "products.db" ]; then
    echo "Database already exists: products.db"
    echo ""
    read -p "Do you want to recreate the database? (all data will be lost) [y/N]: " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping database initialization..."
        echo ""
    else
        echo ""
        echo "========================================"
        echo "Step 1: Initializing Database"
        echo "========================================"
        echo ""
        "$PYTHON_CMD" db_init.py
        if [ $? -ne 0 ]; then
            echo ""
            echo "❌ Database initialization failed!"
            echo "Please check the error above."
            exit 1
        fi
    fi
else
    echo ""
    echo "========================================"
    echo "Step 1: Initializing Database"
    echo "========================================"
    echo ""
    "$PYTHON_CMD" db_init.py
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Database initialization failed!"
        echo "Please check the error above."
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "Step 2: Starting FastAPI Server"
echo "========================================"
echo ""
echo "Server will run on: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo "========================================"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
