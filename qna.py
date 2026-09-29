from ai_service import AIService


async def answer_question(
    ai: AIService,
    question: str
) -> str:
    """
    Answer a student's question using the AI service.
    """
    return await ai.answer_question(question)