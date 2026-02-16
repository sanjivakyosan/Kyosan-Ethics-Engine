# AI Model Integration - Kyosan Ethics Engine

**Date**: Generated automatically  
**Status**: ✅ **INTEGRATED**

## Overview

The Kyosan Ethics Engine connects to OpenRouter (or compatible API). You specify which model to use via the `OPENROUTER_MODEL` environment variable.

## Configuration

### API Connection
- **Base URL**: `https://openrouter.ai/api/v1`
- **API Key**: Set via `OPENROUTER_API_KEY` environment variable (do not hardcode)
- **Model**: Set via `OPENROUTER_MODEL` (e.g. `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`). No default; you choose the model.

### Extra Headers (for OpenRouter rankings)
- **HTTP-Referer**: `https://kyosan-ethics-engine.local`
- **X-Title**: `Kyosan Ethics Engine`

## Implementation Details

### AIService.py
The `AIService` class:
- Uses `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` (no hardcoded key or model)
- Configures extra headers for OpenRouter rankings
- Requires a model (env or constructor) to make requests
- Handles chat completions with proper error handling

### server.py
The server:
- Uses `AIService` with model from `OPENROUTER_MODEL`
- If `OPENROUTER_MODEL` is not set, AI service is disabled even when API key is set
- UI displays the active model name from the health endpoint

### UI
- Checkbox: "Use AI Service"; label shows the model name from the server (e.g. "AI Service (openai/gpt-4o)")
- Checkbox is checked by default when AI is available

## Code Structure

```python
from AIService import AIService

# API key from OPENROUTER_API_KEY environment variable
client = AIService(
    base_url="https://openrouter.ai/api/v1",
    site_url="https://kyosan-ethics-engine.local",
    site_name="Kyosan Ethics Engine"
)

# Use client.model (from OPENROUTER_MODEL)
completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "https://kyosan-ethics-engine.local",
        "X-Title": "Kyosan Ethics Engine",
    },
    extra_body={},
    model=client.model,
    messages=[
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
    ]
)
```

## System Prompt

The AI service includes a system prompt that identifies it as the Kyosan Ethics Engine:
```
"You are the Kyosan Ethics Engine, an advanced AI system that provides comprehensive ethical analysis. Provide detailed, thoughtful responses that consider multiple ethical perspectives, including Asimov's Laws..."
```

## Testing

A test script `test_ai_connection.py` has been created and verified:
- ✅ Connection successful
- ✅ API key valid
- ✅ Model responds correctly
- ✅ Extra headers configured properly

## Usage

The AI service is automatically enabled when:
1. The "Use AI Service" checkbox is checked (default: checked)
2. The API key is configured (default: provided)
3. The server is running

## Status

✅ **AI Model Integration Complete**
✅ **Connection Tested and Verified**
✅ **Ready for Production Use**

©sanjivakyosan  
Created by Sanjiva Kyosan

