from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.ai import generate_guide
from app.database import get_connection, init_db
from app.pdf import chunk_pages, extract_pages
from app.retrieval import retrieve_chunks

app = FastAPI(title="DocuMentor", version="1.0.0")
init_db()

MAX_PDF_BYTES = 10 * 1024 * 1024

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/guides")
async def create_guide(file: UploadFile = File(...), topic: str = Form(...)):
    topic = topic.strip()
    if not 3 <= len(topic) <= 200:
        raise HTTPException(status_code=422, detail="Topic must be between 3 and 200 characters.")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    if len(pdf_bytes) == 0:
        raise HTTPException(status_code=422, detail="Uploaded file is empty.")
    if len(pdf_bytes) > MAX_PDF_BYTES:
        raise HTTPException(status_code=413, detail="PDF must be 10 MB or smaller.")

    try:
        pages = extract_pages(pdf_bytes)
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Could not read the PDF.") from exc

    if not pages:
        raise HTTPException(status_code=422, detail="No selectable text found in the PDF.")

    chunks = chunk_pages(pages)
    relevant = retrieve_chunks(chunks, topic)

    try:
        guide = await generate_guide(topic, relevant)
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="AI provider request failed.") from exc

    with get_connection() as conn:
        document = conn.execute(
            "INSERT INTO documents (filename) VALUES (?)", (file.filename,)
        )
        document_id = document.lastrowid
        conn.executemany(
            "INSERT INTO chunks (document_id, page, content) VALUES (?, ?, ?)",
            [(document_id, chunk["page"], chunk["content"]) for chunk in chunks],
        )
        saved = conn.execute(
            "INSERT INTO guides (document_id, topic, result_json) VALUES (?, ?, ?)",
            (document_id, topic, __import__("json").dumps(guide)),
        )
        guide_id = saved.lastrowid

    return {"id": guide_id, "topic": topic, **guide, "sources": relevant}

app.mount("/static", StaticFiles(directory="static"), name="static")
