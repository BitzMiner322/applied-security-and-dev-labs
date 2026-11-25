import json
import httpx
from app.config import settings
from app.schemas import GuideResult

SYSTEM_PROMPT = """You are a precise study-guide generator.
Use only the provided source excerpts. If the excerpts do not contain enough information,
say so in the summary rather than inventing facts.
Return only valid JSON matching this shape:
{"summary": string, "key_concepts": [string], "practice_questions": [{"question": string, "answer": string}]}
"""

def build_prompt(topic: str, chunks: list[dict]) -> str:
    excerpts = "\n\n".join(
        f"[Source page {chunk['page']}]\n{chunk['content']}" for chunk in chunks
    )
    return f"""Create a study guide for the topic: {topic}

Source excerpts:
{excerpts}

Requirements:
1. Summarize only information supported by the excerpts.
2. Include 3-6 key concepts.
3. Include 3-5 practice questions with concise answers.
4. Return valid JSON only."""

async def generate_guide(topic: str, chunks: list[dict]) -> dict:
    payload = {
        "model": settings.model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(topic, chunks)},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {settings.model_api_key}"}
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{settings.model_base_url.rstrip('/')}/chat/completions",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("Model returned invalid JSON") from exc

    return GuideResult.model_validate(parsed).model_dump()
