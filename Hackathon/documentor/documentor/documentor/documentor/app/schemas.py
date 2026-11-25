from pydantic import BaseModel, Field

class PracticeQuestion(BaseModel):
    question: str = Field(min_length=5)
    answer: str = Field(min_length=1)

class GuideResult(BaseModel):
    summary: str = Field(min_length=20)
    key_concepts: list[str] = Field(min_length=1)
    practice_questions: list[PracticeQuestion] = Field(min_length=1)
