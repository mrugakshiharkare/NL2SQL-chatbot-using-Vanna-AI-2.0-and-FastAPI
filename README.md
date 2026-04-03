# Clinic AI Assistant (Vanna 2.0)

A RAG-based AI agent that answers natural language questions about a Clinic Management Database.

## Tech Stack
- **Framework:** Vanna 2.0
- **LLM:** Google Gemini 1.5 Flash
- **Database:** SQLite
- **API:** FastAPI

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add your `GOOGLE_API_KEY` to a `.env` file.
3. Run `python seed_memory.py` to train the agent.
4. Run `python main.py` to start the server.

## Endpoints
- `POST /chat`: Ask questions about the database.
- `GET /health`: Check system status.