from ai_service import AIService


async def create_learning_path(
    ai: AIService,
    topic: str,
    level: str = "beginner",
    duration: str = "4 weeks"
) -> str:
    """
    Create a personalized learning path using the AI service.
    """
    return await ai.learning_path(
        topic,
        level,
        duration
    )