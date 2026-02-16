# Model Configuration

**©sanjivakyosan**
**Created by Sanjiva Kyosan**

## Configuration

There is no default model. You specify which model to use via the environment.

### OpenRouter
- **OPENROUTER_MODEL**: Model ID (e.g. `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`). Required for AI service.
- **OPENROUTER_API_KEY**: Your API key
- `extra_headers` support for rankings (`HTTP-Referer`, `X-Title`)
- Reasoning can be enabled per request if the model supports it

## Configuration

### Environment Variables

```bash
# Required
export OPENROUTER_API_KEY='your-api-key-here'

# Required for AI (no default model)
export OPENROUTER_MODEL='openai/gpt-4o'

# Optional - for OpenRouter rankings
export OPENROUTER_SITE_URL='https://your-site.com'
export OPENROUTER_SITE_NAME='Your Site Name'
```

### API Key
**Important:** Never hardcode your API key in the code. Always use the `OPENROUTER_API_KEY` environment variable:

```bash
export OPENROUTER_API_KEY='your-openrouter-api-key'
```

## Updated Files

1. **AIService.py**
   - Model from `OPENROUTER_MODEL` or constructor (no default)
   - Added `extra_headers` support
   - Added `site_url` and `site_name` parameters
   - Reasoning optional per request

2. **server.py**
   - Passes `OPENROUTER_MODEL` to AIService; AI disabled if unset
   - Site URL/name from env

3. **static/app.js**
   - Displays model name from `/api/health`

## Usage

Set the model via environment:

```bash
export OPENROUTER_MODEL='openai/gpt-4o'   # or any OpenRouter model ID
export OPENROUTER_API_KEY='your-key'
python server.py
```

The UI shows the active model from the server.

## Testing

After setting `OPENROUTER_MODEL` and restarting:
1. Server logs show "Model: <your model>"
2. Processing uses that model
3. Check OpenRouter dashboard for usage

