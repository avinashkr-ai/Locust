#!/bin/bash

echo "========================================"
echo "Starting Locust Load Test"
echo "========================================"
echo ""
echo "Make sure FastAPI server is running on http://localhost:8000"
echo ""
echo "Locust Web UI will open on: http://localhost:8089"
echo "========================================"
echo ""

# Activate virtual environment if present so 'locust' is available
if [ -f ".venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
else
    echo "⚠️ Virtual environment '.venv' not found. Attempting to run with system Python."
    echo "   If you see 'locust: command not found', run ./setup_and_start.sh once to create the .venv."
fi

echo "Opening browser in 3 seconds..."
sleep 3

# Try to open browser (works on Mac and most Linux distributions)
if command -v open &> /dev/null; then
    open http://localhost:8089
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8089
fi

echo ""
echo "Starting Locust..."
echo ""

locust -f locustfile.py --host=http://localhost:8000
