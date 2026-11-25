import fitz

def extract_pages(pdf_bytes: bytes) -> list[dict]:
    """Return page-numbered text chunks from a PDF."""
    pages = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for number, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if text:
                pages.append({"page": number, "text": text})
    return pages

def chunk_pages(pages: list[dict], chunk_size: int = 1200, overlap: int = 150) -> list[dict]:
    chunks = []
    for page in pages:
        text = " ".join(page["text"].split())
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append({"page": page["page"], "content": text[start:end]})
            if end == len(text):
                break
            start = end - overlap
    return chunks
