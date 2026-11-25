from app.pdf import chunk_pages
from app.retrieval import retrieve_chunks

def test_retrieval_prefers_relevant_chunk():
    chunks = [
        {"page": 1, "content": "Photosynthesis converts light energy into chemical energy."},
        {"page": 2, "content": "The mitochondrion produces ATP through cellular respiration."},
    ]
    result = retrieve_chunks(chunks, "photosynthesis light energy")
    assert result[0]["page"] == 1

def test_chunking_creates_overlapping_chunks():
    pages = [{"page": 1, "text": "word " * 3000}]
    chunks = chunk_pages(pages, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert chunks[0]["page"] == 1
