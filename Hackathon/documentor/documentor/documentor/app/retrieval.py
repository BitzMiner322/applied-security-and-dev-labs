import re
from collections import Counter

STOPWORDS = set("""a an the and or but if then than of to in on for with by from as at is are was
were be been being this that these those it its into about over under can could should would will
""".split())

def tokenize(text: str) -> list[str]:
    return [word for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in STOPWORDS and len(word) > 2]

def retrieve_chunks(chunks: list[dict], query: str, top_k: int = 4) -> list[dict]:
    query_terms = Counter(tokenize(query))
    scored = []
    for chunk in chunks:
        chunk_terms = Counter(tokenize(chunk["content"]))
        score = sum(count * chunk_terms.get(term, 0) for term, count in query_terms.items())
        scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [chunk for score, chunk in scored[:top_k] if score > 0]
    return selected or chunks[:top_k]
