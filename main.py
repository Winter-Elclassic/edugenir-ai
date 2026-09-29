from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ai_service import AIService
from config import settings
from models import (
    ErrorResponse,
    ExplainRequest,
    LearningPathRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
)


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    description=(
        "AI-powered educational assistant for questions, "
        "explanations, quizzes, summaries and personalized "
        "learning paths."
    ),
    version="1.0.0",
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


# ============================================================
# HTML TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory="templates"
)


# ============================================================
# AI SERVICE
# ============================================================

ai = AIService(settings)


# ============================================================
# FRONTEND
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "gemini_model": settings.gemini_model,
        "local_explanation_enabled": (
            settings.local_explanation_enabled
        ),
    }


# ============================================================
# QUESTION ANSWERING
# ============================================================

@app.post("/qa")
async def qa(payload: QARequest):

    try:
        answer = await ai.answer_question(
            payload.question
        )

        return {
            "answer": answer
        }

    except Exception as exc:
        return ErrorResponse(
            error=str(exc)
        ).model_dump()


# ============================================================
# EXPLANATION
# ============================================================

@app.post("/explain")
async def explain(payload: ExplainRequest):

    try:
        explanation = await ai.explain(
            payload.topic,
            payload.level
        )

        return {
            "explanation": explanation
        }

    except Exception as exc:
        return ErrorResponse(
            error=str(exc)
        ).model_dump()


# ============================================================
# QUIZ
# ============================================================

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    try:
        quiz = await ai.generate_quiz(
            payload.text,
            payload.num_questions
        )

        return quiz.model_dump()

    except Exception as exc:
        return ErrorResponse(
            error=str(exc)
        ).model_dump()


# ============================================================
# SUMMARY
# ============================================================

@app.post("/summarize")
async def summarize(payload: SummaryRequest):

    try:
        summary = await ai.summarize(
            payload.text
        )

        return {
            "summary": summary
        }

    except Exception as exc:
        return ErrorResponse(
            error=str(exc)
        ).model_dump()


# ============================================================
# LEARNING PATH
# ============================================================

@app.post("/learn/recommendations")
async def learning_recommendations(
    payload: LearningPathRequest
):

    try:
        recommendations = await ai.learning_path(
            payload.topic,
            payload.level,
            payload.duration
        )

        return {
            "recommendations": recommendations
        }

    except Exception as exc:
        return ErrorResponse(
            error=str(exc)
        ).model_dump()


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup_event():
    print("========================================")
    print("EduGenie API started successfully")
    print(f"Gemini model: {settings.gemini_model}")
    print(
        "Gemini configured:",
        bool(settings.gemini_api_key)
    )
    print("========================================")