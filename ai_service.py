import asyncio
import json
from typing import Optional

from google import genai
from google.genai import types

from models import QuizResponse
from prompts import (
    EXPLAIN_PROMPT,
    LEARNING_PATH_PROMPT,
    QA_PROMPT,
    QUIZ_PROMPT,
    SUMMARY_PROMPT,
    SYSTEM_PROMPT,
)


class AIService:
    def __init__(self, settings):
        self.settings = settings

        self.client: Optional[genai.Client] = None

        if settings.gemini_api_key:
            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

        self.local_model = None
        self.local_tokenizer = None

    def _check_client(self):
        if self.client is None:
            raise RuntimeError(
                "Gemini API key is not configured. "
                "Add GEMINI_API_KEY to your .env file."
            )

    def _generate(self, prompt: str) -> str:
        self._check_client()

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()

    async def _generate_async(self, prompt: str) -> str:
        return await asyncio.to_thread(
            self._generate,
            prompt
        )

    async def answer_question(
        self,
        question: str
    ) -> str:

        if len(question) > self.settings.max_input_chars:
            raise ValueError(
                "Question is too long."
            )

        prompt = QA_PROMPT.format(
            question=question
        )

        return await self._generate_async(prompt)

    async def explain(
        self,
        topic: str,
        level: str
    ) -> str:

        if len(topic) > self.settings.max_input_chars:
            raise ValueError(
                "Topic is too long."
            )

        prompt = EXPLAIN_PROMPT.format(
            topic=topic,
            level=level
        )

        return await self._generate_async(prompt)

    async def summarize(
        self,
        text: str
    ) -> str:

        if len(text) > self.settings.max_input_chars:
            raise ValueError(
                "Text is too long."
            )

        prompt = SUMMARY_PROMPT.format(
            text=text
        )

        return await self._generate_async(prompt)

    async def learning_path(
        self,
        topic: str,
        level: str,
        duration: str
    ) -> str:

        prompt = LEARNING_PATH_PROMPT.format(
            topic=topic,
            level=level,
            duration=duration
        )

        return await self._generate_async(prompt)

    async def generate_quiz(
        self,
        text: str,
        num_questions: int
    ) -> QuizResponse:

        if len(text) > self.settings.max_input_chars:
            raise ValueError(
                "Text is too long."
            )

        prompt = QUIZ_PROMPT.format(
            text=text,
            num_questions=num_questions
        )

        self._check_client()

        def generate():
            response = self.client.models.generate_content(
                model=self.settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3,
                    response_mime_type="application/json",
                    response_schema=QuizResponse,
                ),
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty quiz."
                )

            return response.text

        raw_response = await asyncio.to_thread(
            generate
        )

        try:
            data = json.loads(raw_response)
            return QuizResponse.model_validate(data)

        except Exception as exc:
            raise RuntimeError(
                f"Could not parse Gemini quiz response: {exc}"
            ) from exc