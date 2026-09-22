# AI Tax Filing Assistant (Local Architecture)

An agentic AI assistant built with Google Agent Development Kit (ADK) that helps Indian salaried employees analyze their tax position. This version is completely local and runs on zero-cost infrastructure using the free Gemini API.

## Architecture
- **Frontend**: React (Vite) interface running on port 3000.
- **Backend**: FastAPI wrapping the ADK `InMemoryRunner`, exposing a `/chat` endpoint on port 8000.
- **Knowledge Base**: Instead of a cloud vector database, it uses a lightweight local text file (`data/tax_rules.txt`) to ground its tax advice.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed.
- Node.js (for the frontend).
- A free Gemini API Key from [Google AI Studio](https://aistudio.google.com/).

## Setup & Running

1. **Set your API Key**:
   Open a terminal and set your environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   export GOOGLE_GENAI_USE_VERTEXAI="false"
   ```

2. **Start the Backend**:
   Install dependencies and start the FastAPI server:
   ```bash
   uv sync
   uv run uvicorn main:app --reload
   ```

3. **Start the Frontend**:
   Open a **new terminal window** (don't forget to set the API keys here too if needed, though the frontend doesn't directly need them), and run:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Chat**:
   Open your browser to the URL provided by Vite (usually `http://localhost:3000`) and start chatting!

## Project Structure
- `main.py`: The FastAPI server wrapping the agent.
- `frontend/`: The React application.
- `app/agent.py`: Contains the system instructions, checklist rules, and agent orchestration.
- `app/tools.py`: Contains the mock extraction and local text-search tools.
- `data/tax_rules.txt`: Local knowledge base containing Indian tax rules.
