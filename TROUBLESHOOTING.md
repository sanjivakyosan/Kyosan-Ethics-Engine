# Troubleshooting Guide

**©sanjivakyosan**
**Created by Sanjiva Kyosan**
## Issue: Health Endpoint 500 Error

**Fixed:** The health endpoint now handles serialization errors gracefully.

## Issue: No OpenRouter Activity

If you're not seeing activity in OpenRouter, check the following:

### 1. Check if AI Service is Initialized

When the server starts, look for these messages:
```
[Init] Checking for OPENROUTER_API_KEY...
[Init] ✓ AI Service (OpenRouter) initialized successfully
```

If you see:
```
[Init] ⚠ OPENROUTER_API_KEY not set, AI Service disabled
```

**Solution:** Set your API key:
```bash
export OPENROUTER_API_KEY='your-key-here'
```

### 2. Check if Checkbox is Checked

In browser console, when you click "Process", you should see:
```
=== API Request Details ===
Use AI Checkbox Checked: true  <-- Should be true
```

If it shows `false`, the checkbox isn't being read correctly.

### 3. Check Server Logs

When you process with AI enabled, look for these logs in the server terminal:

```
[API Request] Use AI Service: True
[AI Service] AI service requested by user: True
[AI Service] AI service available: True
[AIService.process_with_reasoning] Starting API call...
[AIService] Making chat completion call to https://openrouter.ai/api/v1
[AIService] Sending request to OpenAI client...
```

If you see:
```
[AI Service] AI service requested but not available (no API key set)
```

**Solution:** Set the OPENROUTER_API_KEY environment variable.

### 4. Check for Errors

Look for error messages in server logs:
```
[AI Service] ✗ Error from AI service: ...
```

Common errors:
- **"API key invalid"** - Check your API key
- **"Connection refused"** - Network issue
- **"Model not found"** - Check model name

### 5. Verify API Key

Test your API key directly:
```bash
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 6. Check Browser Console

Open browser console (F12) and look for:
```
Sending request to: http://localhost:8000/api/v1/ethics/process
Request payload: { use_ai_service: true, ... }
```

If `use_ai_service` is `false`, the checkbox isn't working.

## Debugging Steps

1. **Restart server** to see initialization logs
2. **Check browser console** for request details
3. **Check server terminal** for processing logs
4. **Verify API key** is set correctly
5. **Check checkbox** is actually checked in UI

## Expected Log Flow

When AI service is working correctly:

```
[API Request] Use AI Service: True
[AI Service] AI service requested by user: True
[AI Service] AI service available: True
[AI Service] Calling model <your OPENROUTER_MODEL>...
[AIService.process_with_reasoning] Starting API call...
[AIService] Making chat completion call to https://openrouter.ai/api/v1
[AIService] Sending request to OpenAI client...
[AIService] Response received from API
[AI Service] ✓ Response received: XXX characters
```

If any step is missing, that's where the issue is.

