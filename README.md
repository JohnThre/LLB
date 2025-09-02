# LLB - AI Sexual Health Education

## Setup

1. Get API keys from at least one provider:
   - OpenAI: https://platform.openai.com/api-keys
   - Claude: https://console.anthropic.com/
   - Gemini: https://makersuite.google.com/app/apikey
   - Ollama: https://ollama.ai/ (local)

2. Install dependencies:
   ```bash
   cd backend && python3.11 -m venv llb-env && source llb-env/bin/activate && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

   **Apple Silicon (M1/M2/M3) Users:**
   ```bash
   # Use the optimized setup script for Apple Silicon
   cd backend && ./setup_whisper.sh
   cd ../frontend && npm install
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Start:
   ```bash
   make dev
   ```

## Usage

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

## Commands

- `make dev` - Start development
- `make test` - Run tests
- `make build` - Build for production
- `make build-arm64` - Build for Apple Silicon (ARM64)
- `make dev-arm64` - Start development on Apple Silicon