# AI Service Integration Guide

**©sanjivakyosan**
**Created by Sanjiva Kyosan**
## Overview

The ethical processing server integrates with OpenRouter. You choose which model to use by setting the `OPENROUTER_MODEL` environment variable. All requests still pass through the 40+ ethical processing systems.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install the `openai` package needed for OpenRouter integration.

### 2. Set API Key and Model

Set your OpenRouter API key and the model you want to use:

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
export OPENROUTER_MODEL="openai/gpt-4o"   # or any OpenRouter model ID
```

Or on Windows:
```cmd
set OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
set OPENROUTER_MODEL=openai/gpt-4o
```

### 3. Start Server

```bash
python server.py
```

The server will initialize the AI service when both `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` are set.

## Usage

### Option 1: Process with AI Service (via UI)

1. Open http://localhost:8000
2. Check "Use AI Service" (label shows your model name from OPENROUTER_MODEL)
3. Enter your text
4. Click "Process"

The system will:
- Pre-process through ethical systems
- Send to AI service (your chosen model via OpenRouter)
- Post-process AI response through ethical systems
- Return combined results

### Option 2: Process with AI Service (via API)

```bash
curl -X POST "http://localhost:8000/api/v1/ethics/process" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "How many r'\''s are in the word '\''strawberry'\''?",
    "processing_level": "standard",
    "use_ai_service": true,
    "follow_up": "Are you sure? Think carefully."
  }'
```

### Option 3: Direct AI Chat Endpoint

```bash
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "How many r'\''s are in the word '\''strawberry'\''?"}
    ],
    "model": "<same as OPENROUTER_MODEL or override>",
    "reasoning_enabled": true
  }'
```

## Features

### Ethical Pre-Processing

Before sending to AI service:
- Input validated through all ethical systems
- Harm detection
- Bias detection
- Context validation
- Ethical score calculated

### AI Processing

- Uses the model set in OPENROUTER_MODEL
- Supports follow-up questions
- Preserves reasoning details (if provided by the model)
- Tracks token usage

### Ethical Post-Processing

After receiving AI response:
- Response analyzed through ethical systems
- Output safety filtering
- Impact assessment
- Final ethical score

## API Endpoints

### POST /api/v1/ethics/process

Main processing endpoint with optional AI service.

**Parameters:**
- `user_input` (required): Text to process
- `processing_level` (optional): "basic", "standard", or "detailed"
- `use_ai_service` (optional): Boolean, enable AI service
- Model is determined by server config (`OPENROUTER_MODEL`), not per-request
- `follow_up` (optional): Follow-up question for AI

**Response includes:**
- `response`: Processed text
- `ethical_score`: Overall ethical score
- `analysis`: Detailed analysis including:
  - `ethical_pre_analysis`: Pre-processing results
  - `ethical_post_analysis`: Post-processing results
  - `ai_response`: AI service response with reasoning

### POST /api/v1/ai/chat

Direct AI chat endpoint with ethical oversight.

**Parameters:**
- `messages` (required): List of message objects
- `model` (optional): Model name
- `reasoning_enabled` (optional): Enable reasoning mode

**Response includes:**
- `content`: AI response
- `reasoning_details`: Reasoning chain (if enabled)
- `usage`: Token usage statistics
- `ethical_analysis`: Post-processing ethical analysis

## Reasoning Mode

If your chosen model supports reasoning, you can enable it:

```python
response = ai_service.chat_completion(
    messages=[{"role": "user", "content": "Question"}],
    reasoning_enabled=True   # uses client.model (OPENROUTER_MODEL)
)
```

## Security & Ethics

- All AI inputs are pre-validated through ethical systems
- All AI outputs are post-validated through ethical systems
- Low ethical scores (< 0.5) block AI chat requests
- Full audit trail of ethical analysis
- Token usage tracking

## Error Handling

- Missing API key: AI service disabled, falls back to ethical processing only
- API errors: Returned in response, doesn't crash server
- Ethical validation failures: Request blocked with explanation

## Example Workflow

1. User submits: "How many r's are in strawberry?"
2. **Pre-processing**: Ethical systems validate input (score: 0.95)
3. **AI Processing**: Sent to your configured model (OPENROUTER_MODEL)
4. **AI Response**: "There are 3 r's in strawberry" + reasoning details
5. **Post-processing**: Ethical systems validate response (score: 0.92)
6. **Final Response**: Combined result with full ethical analysis

## Models Supported

Set `OPENROUTER_MODEL` to any model ID available on OpenRouter (e.g. `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`). There is no default; you choose the model.

## Troubleshooting

**AI Service not available:**
- Set both OPENROUTER_API_KEY and OPENROUTER_MODEL
- Verify API key is valid
- Check server logs for errors

**Reasoning not working:**
- Not all models support reasoning; check your model’s docs
- Ensure `reasoning_enabled` is True when supported

**Ethical validation blocking requests:**
- Review ethical analysis in response
- Adjust input to align with ethical guidelines

