#!/bin/bash
# ©sanjivakyosan
# Created by Sanjiva Kyosan
# Set OPENROUTER_API_KEY and OPENROUTER_MODEL (edit values below), then: source set_api_key.sh

export OPENROUTER_API_KEY='your-openrouter-api-key-here'
export OPENROUTER_MODEL='your-model-id-here'   # e.g. openai/gpt-4o, anthropic/claude-3.5-sonnet

echo "✓ OPENROUTER_API_KEY set"
echo "✓ OPENROUTER_MODEL set: $OPENROUTER_MODEL"
echo ""
echo "⚠ IMPORTANT: You must restart the server for this to take effect!"
echo ""
echo "To restart:"
echo "1. Stop current server (Ctrl+C if running)"
echo "2. Run: python3 server.py"
echo "   OR"
echo "2. Double-click 'Launch Kyosan Ethics Engine.command' on desktop"
echo ""
echo "After restart, look for this in server logs:"
echo "  [Init] ✓ AI Service (OpenRouter) initialized successfully"

