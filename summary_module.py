from ai_service import AIService


async def summarize_text(
    ai: AIService,
    text: str
) -> str:
    """
    Summarize educational text using the AI service.
    """
    return await ai.summarize(text)