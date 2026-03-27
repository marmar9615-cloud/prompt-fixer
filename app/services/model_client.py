from __future__ import annotations

import os

from openai import OpenAI


class ModelClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str, model: str) -> str:
        if not self.client:
            return (
                "Answer: Demo mode output because OPENAI_API_KEY is not configured.\n"
                "Evidence: No live model call was made in this environment.\n"
                "Caveats: Configure OPENAI_API_KEY to run real model tests."
            )

        response = self.client.responses.create(
            model=model,
            input=prompt,
            temperature=0.2,
        )
        return response.output_text or ""
