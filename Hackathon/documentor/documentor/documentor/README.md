# DocuMentor

DocuMentor is a FastAPI web application that turns an uploaded PDF into a grounded study guide.
It extracts text, retrieves the most relevant chunks for each requested topic, and asks an
OpenAI-compatible chat model to return structured JSON: summary, key concepts, and practice questions.

## Features
- PDF upload and text extraction
- Chunking and keyword-based retrieval
- Structured JSON generation with validation
- SQLite persistence for documents and generated guides
- Input validation and consistent API error handling
- Simple browser frontend
- Pytest test suite

## Stack
- Python 3.10+
- FastAPI, Uvicorn
- PyMuPDF for PDF extraction
- SQLite via SQLModel-compatible raw sqlite3
- OpenAI-compatible Chat Completions API
- Vanilla HTML/JavaScript frontend

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API key and base URL
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Environment variables
| Variable | Purpose |
|---|---|
| `MODEL_API_KEY` | API key for your OpenAI-compatible provider |
| `MODEL_BASE_URL` | API base URL, e.g. `https://api.meta.ai/v1` |
| `MODEL_NAME` | Chat model name |
| `DATABASE_URL` | SQLite database path |

## API
`POST /api/guides` with multipart form fields:
- `file`: PDF file
- `topic`: study topic, 3-200 characters

Response:
```json
{
  "id": 1,
  "topic": "photosynthesis",
  "summary": "...",
  "key_concepts": ["..."],
  "practice_questions": [{"question": "...", "answer": "..."}],
  "sources": [{"page": 3, "excerpt": "..."}]
}
```

## Tests
```bash
pytest -q
```

## Notes
The retrieval layer is intentionally lightweight: it uses TF-IDF-style keyword scoring rather than
a vector database. This keeps the hackathon-scale project easy to run, while still grounding model
output in source text and reducing hallucination.
