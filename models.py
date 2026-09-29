from typing import List

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: str


class QARequest(BaseModel):
    question: str = Field(..., min_length=1)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = "beginner"


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1)
    num_questions: int = Field(default=5, ge=1, le=20)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = "beginner"
    duration: str = "4 weeks"


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(..., min_length=2)
    answer: str
    explanation: str


class QuizResponse(BaseModel):
    title: str
    questions: List[QuizQuestion]