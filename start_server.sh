#!/bin/bash
# ©sanjivakyosan
# Created by Sanjiva Kyosan

# Startup script for Kyosan Ethics Engine Server

echo "Starting Kyosan Ethics Engine Server..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p templates static

# Start the server
echo ""
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
python server.py

