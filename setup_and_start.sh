#!/bin/bash

echo "========================================"
echo "FastAPI Load Testing - Complete Setup"
echo "========================================"
echo ""

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
        python3 db_init.py
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
    python3 db_init.py
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
