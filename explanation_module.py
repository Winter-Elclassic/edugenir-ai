from ai_service import AIService


async def explain_topic(
    ai: AIService,
    topic: str,
    level: str = "beginner"
) -> str:
    """
    Explain an educational topic using the AI service.
    """
    return await ai.explain(topic, level)