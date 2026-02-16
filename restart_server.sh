#!/bin/bash
# Quick server restart script
# ©sanjivakyosan
# Created by Sanjiva Kyosan

PROJECT_DIR="/Users/sanjivakyosan/Desktop/new model"
cd "$PROJECT_DIR" || exit 1

echo "Stopping existing server..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
sleep 2

echo "Loading API key..."
source set_api_key.sh 2>/dev/null || true

echo "Starting server..."
python3 server.py

