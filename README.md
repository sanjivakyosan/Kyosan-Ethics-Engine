# Kyosan Ethics Engine - UI & API Server

©sanjivakyosan  
Created by Sanjiva Kyosan

A locally runnable web interface and API for ethical AI processing. Built on Asimov's Laws (Zeroth–Third); principle-based only, no weighted scores in decisions. Optional OpenRouter-backed responses when you set your own API key and model.

**Quick start:** `pip install -r requirements.txt` → `cp .env.example .env` (edit with your keys) → `python server.py` → open http://localhost:8000

## Features

- **Modern Web UI**: Clean, responsive interface for text input and output
- **RESTful API**: FastAPI-based server with comprehensive ethical processing endpoints
- **Real-time Processing**: Live ethical analysis with status indicators
- **Multiple Processing Levels**: Basic, Standard, and Detailed processing modes
- **Ethical Analysis**: Comprehensive ethical scoring and analysis display

## Requirements

- **Python 3.9+**
- Dependencies in `requirements.txt`

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Keep all ethical processing modules in the project root**  
   Run the server from the project directory (e.g. `python server.py`) so Python can find modules like `PrincipleBasedEthicalProcessor`, `EthicalSystemIntegrator`, etc. The integrator also loads `Core Ethical Processing System Architecture.py` from the same directory as `EthicalSystemIntegrator.py`.

3. **Environment variables (optional — for AI-backed responses)**  
   The app loads variables from a `.env` file if present (via `python-dotenv`). You can:
   - **Use a `.env` file:** Copy `.env.example` to `.env`, then set your values:
     ```bash
     cp .env.example .env
     # Edit .env and set OPENROUTER_API_KEY and OPENROUTER_MODEL
     ```
   - **Or set in the shell:** e.g. `export OPENROUTER_API_KEY=...` and `export OPENROUTER_MODEL=openai/gpt-4o` (or use `source set_api_key.sh` after editing it).

   There is **no default model**; you must set `OPENROUTER_MODEL` to the OpenRouter model ID you want (e.g. `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`). The UI shows the active model name from the server.

## Running the Server

### Option 1: Direct Python execution
```bash
python server.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

**AI service:** If both `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` are set (in `.env` or the shell), the server connects to OpenRouter and the UI label shows the model name. If either is missing, the server runs without AI (ethical processing only).

## Usage

1. **Access the Web UI:**
   - Open your browser and navigate to `http://localhost:8000`
   - The main interface will be displayed

2. **Process Text:**
   - Enter your text in the input area
   - Select processing level: **Basic** (principle check only), **Standard** (core + extended systems), or **Detailed** (all systems)
   - Click "Process" or press Ctrl/Cmd + Enter
   - View the processed output and ethical analysis

3. **API Endpoints:**
   - **Main processing**: `POST /api/v1/ethics/process`
   - **Health**: `GET /api/health`
   - **Systems**: `GET /api/systems`
   - **Conversations**: `GET/POST/PUT/DELETE /api/conversations` (list, save, update, delete)
   - **Upgrade governance**: `POST /api/v1/ethics/upgrade/propose`, `/validate`, `GET /trace`, etc.
   - **Advanced reasoning**: `POST /api/v1/ethics/advanced/moral-dilemma`, `/harm-prediction`, `/process`, etc.
   - **Interactive API docs**: `http://localhost:8000/docs` (Swagger UI)

## API Examples

### Process Ethical Input
```bash
curl -X POST "http://localhost:8000/api/v1/ethics/process" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Your text here",
    "processing_level": "standard",
    "context": {}
  }'
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

## Documentation

- **[Framework documentation](docs/FRAMEWORK_DOCUMENTATION.md)** — Full description of the framework: core principles, architecture, all systems by category, processing levels, API reference, and project layout. Start here for contributing or integrating.

## Project Structure

```
.
├── server.py              # FastAPI server application
├── EthicalSystemIntegrator.py
├── PrincipleBasedEthicalProcessor.py
├── AIService.py           # OpenRouter / AI API client (model from OPENROUTER_MODEL)
├── .env.example           # Template for env vars; copy to .env and fill in
├── .gitignore             # Excludes .env, logs, venv, __pycache__, etc.
├── docs/
│   └── FRAMEWORK_DOCUMENTATION.md   # Comprehensive framework & systems doc
├── templates/
│   └── index.html         # Main web UI
├── static/
│   ├── style.css          # UI styling
│   └── app.js             # Frontend JavaScript
├── conversations/         # Saved conversations (created at runtime)
├── requirements.txt      # Python dependencies (includes python-dotenv)
├── set_api_key.sh        # Optional: set OPENROUTER_API_KEY and OPENROUTER_MODEL in shell
├── start_server.sh       # Optional: venv + deps + server
├── start_server_simple.sh
├── restart_server.sh
├── check_api_key.sh
├── setup_ai.sh
└── README.md              # This file
```

## Features in Detail

### Web UI
- Responsive design that works on desktop and mobile
- Real-time status indicators
- Processing time display
- Ethical score visualization
- Detailed analysis breakdown

### API Server
- FastAPI with automatic OpenAPI documentation
- CORS enabled for local development
- Error handling and validation
- Integration with ethical processing modules
- Health monitoring endpoints

## Troubleshooting

1. **Port already in use:**
   - Change the port in `server.py` (line with `uvicorn.run`)
   - Or kill the process using port 8000

2. **Module import errors:**
   - Run the server from the project root so all ethical processing `.py` files are on Python’s path (same directory as `server.py` and `EthicalSystemIntegrator.py`)
   - Check that Python can find the modules (`sys.path` includes the project directory)

3. **UI not loading:**
   - Check browser console for errors
   - Ensure `templates/` and `static/` directories exist
   - Verify server is running and accessible

4. **AI service not available:**
   - Set both `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` (in `.env` or shell). The server logs `[Init] ⚠ OPENROUTER_MODEL not set...` or `No API key found` if either is missing.
   - If using `.env`, ensure it's in the project root and you've run `pip install -r requirements.txt` (so `python-dotenv` is installed).

## Development

To modify the UI:
- Edit `templates/index.html` for structure
- Edit `static/style.css` for styling
- Edit `static/app.js` for functionality

To modify the API:
- Edit `server.py` to add/modify endpoints
- API documentation auto-updates at `/docs`

## Repo and security

- No API keys or secrets are committed. Use `.env` for local config; it is in `.gitignore`.
- Model and provider are chosen by you via `OPENROUTER_MODEL` (no default).

## License

This system is part of the Kyosan Ethics Engine framework.

