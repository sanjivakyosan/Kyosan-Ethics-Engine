#!/bin/bash
# ©sanjivakyosan
# Created by Sanjiva Kyosan

# Setup script for AI Service integration

echo "Setting up AI Service integration..."
echo ""

# Check if API key is provided as argument
if [ -z "$1" ]; then
    echo "Usage: ./setup_ai.sh <your-openrouter-api-key>"
    echo ""
    echo "Or set it manually:"
    echo "export OPENROUTER_API_KEY='sk-or-v1-your-key-here'"
    echo ""
    exit 1
fi

API_KEY=$1

# Set environment variable for current session
export OPENROUTER_API_KEY="$API_KEY"

# Add to shell profile for persistence
SHELL_PROFILE=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_PROFILE="$HOME/.bash_profile"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_PROFILE="$HOME/.bashrc"
fi

if [ -n "$SHELL_PROFILE" ]; then
    # Remove old key if exists
    sed -i.bak '/OPENROUTER_API_KEY/d' "$SHELL_PROFILE"
    # Add new key
    echo "" >> "$SHELL_PROFILE"
    echo "# OpenRouter API Key for Ethical Processing System" >> "$SHELL_PROFILE"
    echo "export OPENROUTER_API_KEY='$API_KEY'" >> "$SHELL_PROFILE"
    echo ""
    echo "API key added to $SHELL_PROFILE"
    echo "Run 'source $SHELL_PROFILE' or restart your terminal to apply."
else
    echo "Could not find shell profile. Please manually add:"
    echo "export OPENROUTER_API_KEY='$API_KEY'"
fi

echo ""
echo "API key set for current session!"
echo "You can now start the server with: python server.py"

