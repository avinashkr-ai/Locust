#!/bin/bash

echo "========================================"
echo "Starting FastAPI Server"
echo "========================================"
echo ""
echo "Server will run on: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo "========================================"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
