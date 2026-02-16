#!/bin/bash
# ©sanjivakyosan
# Created by Sanjiva Kyosan
# Quick script to check if OPENROUTER_API_KEY is set

echo "Checking OPENROUTER_API_KEY..."
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ OPENROUTER_API_KEY is NOT set"
    echo ""
    echo "To set it, run:"
    echo "export OPENROUTER_API_KEY='your-key-here'"
else
    echo "✓ OPENROUTER_API_KEY is set"
    echo "Key length: ${#OPENROUTER_API_KEY} characters"
    echo "Key starts with: ${OPENROUTER_API_KEY:0:20}..."
fi

