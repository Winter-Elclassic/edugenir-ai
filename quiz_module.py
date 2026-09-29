from ai_service import AIService
from models import QuizResponse


async def generate_quiz(
    ai: AIService,
    text: str,
    num_questions: int = 5
) -> QuizResponse:
    """
    Generate a quiz from the supplied educational text.
    """
    return await ai.generate_quiz(
        text,
        num_questions
    )