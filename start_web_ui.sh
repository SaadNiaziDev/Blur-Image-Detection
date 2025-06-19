#!/bin/bash

# Blur Detection Web UI Startup Script

echo "Starting Blur Detection Web UI..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Start the Flask application
echo "Starting Flask application..."
echo "Web UI will be available at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py 