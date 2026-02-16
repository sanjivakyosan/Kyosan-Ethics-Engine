#!/bin/bash
# ©sanjivakyosan
# Created by Sanjiva Kyosan
# Simple server startup script for Kyosan Ethics Engine

cd "$(dirname "$0")"

echo "============================================================"
echo "Starting Kyosan Ethics Engine Server"
echo "============================================================"

# Check if port is in use
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "⚠ Port 8000 is already in use. Stopping existing process..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Install dependencies if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    python3 -m pip install fastapi "uvicorn[standard]" pydantic python-multipart openai --quiet
fi

# Start server
echo ""
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo "============================================================"
echo ""

python3 server.py

