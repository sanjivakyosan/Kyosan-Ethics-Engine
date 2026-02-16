# Debugging API Connection Issues

**©sanjivakyosan**
**Created by Sanjiva Kyosan**
## Problem: UI Not Connecting to Server API

If the UI is not connecting to the server API or responses are just copies of input, follow these steps:

## 1. Check Server is Running

```bash
# Check if server is running
lsof -i :8000

# Or test directly
curl http://localhost:8000/api/health
```

## 2. Check Browser Console

1. Open browser (F12 or Cmd+Option+I)
2. Go to Console tab
3. Look for errors when clicking "Process"
4. Check Network tab to see if API calls are being made

## 3. Check Server Logs

The server now logs detailed information:
- `[API Request]` - Shows incoming requests
- `[Processing]` - Shows processing steps
- `[AI Service]` - Shows AI service calls
- `[API Response]` - Shows final response

Look for these in the terminal where server is running.

## 4. Verify API Connection

The JavaScript now:
- Logs all API calls to console
- Shows request/response details
- Detects if response matches input
- Shows detailed error messages

## 5. Common Issues

### Issue: Response is same as input
**Fix:** The server now validates and prevents this. Check server logs for `[Warning] Response matches input`

### Issue: AI Service not working
**Fix:** 
1. Set OPENROUTER_API_KEY environment variable
2. Check server startup logs for "AI Service initialized"
3. Enable "Use AI Service" checkbox in UI

### Issue: CORS errors
**Fix:** CORS is enabled for all origins. If still seeing errors, check browser console.

### Issue: 500 Internal Server Error
**Fix:** 
1. Check server terminal for error traceback
2. Verify all Python files are in correct directory
3. Check that EthicalSystemIntegrator loads successfully

## 6. Testing API Directly

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test process endpoint
curl -X POST http://localhost:8000/api/v1/ethics/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Hello",
    "processing_level": "standard",
    "use_ai_service": false
  }'
```

## 7. Enable Debug Mode

The server now has extensive logging. All API requests are logged with:
- Input received
- Processing steps
- AI service calls (if used)
- Final response

Check the terminal running the server to see these logs.

## 8. Verify Response Generation

The system now:
1. Always generates a response different from input
2. Uses ResponseGenerator for intelligent responses
3. Calculates dynamic ethical scores
4. Logs all processing steps

If you see input echoed back, check server logs for warnings.

