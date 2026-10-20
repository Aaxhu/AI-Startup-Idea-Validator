import json
import os
import time
from typing import Any, Type, TypeVar

import httpx
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from app.config import settings

load_dotenv()

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    """
    Local Ollama LLM client.

    Normal generation:
        Ollama OpenAI-compatible API

    Structured generation:
        Ollama native API with JSON Schema
    """

    def __init__(self) -> None:

        self.base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        ).rstrip("/")
        self.ollama_api_key = os.getenv("OLLAMA_API_KEY", "").strip()

        self.client = OpenAI(
            base_url=f"{self.base_url}/v1",
            api_key=self.ollama_api_key or settings.OPENAI_API_KEY or "ollama",
            timeout=300.0,
        )

        self.model = settings.MODEL_NAME
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
        self.max_retries = settings.MAX_RETRIES
        self.retry_delay = settings.RETRY_DELAY

    # =========================================================
    # NORMAL TEXT GENERATION
    # =========================================================

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        json_mode: bool = False,
    ) -> str:

        last_error = None

        for attempt in range(self.max_retries):

            try:

                request = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                }

                if json_mode:
                    request["response_format"] = {
                        "type": "json_object"
                    }

                response = self.client.chat.completions.create(
                    **request
                )

                content = response.choices[0].message.content

                if content is None:
                    return ""

                return content.strip()

            except Exception as exc:

                last_error = exc

                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        raise RuntimeError(
            f"LLM request failed after "
            f"{self.max_retries} attempts: {last_error}"
        )

    # =========================================================
    # JSON PARSER
    # =========================================================

    def _extract_json(self, raw_response: str) -> Any:

        if not raw_response:
            raise ValueError(
                "LLM returned an empty response."
            )

        raw_response = raw_response.strip()

        # Direct JSON
        try:
            return json.loads(raw_response)

        except json.JSONDecodeError:
            pass

        # Remove markdown fences
        cleaned = raw_response

        if "```json" in cleaned:
            cleaned = cleaned.replace(
                "```json", ""
            )

        if "```JSON" in cleaned:
            cleaned = cleaned.replace(
                "```JSON", ""
            )

        cleaned = cleaned.replace(
            "```", ""
        ).strip()

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError:
            pass

        # Find JSON object
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end != -1 and end > start:

            json_text = cleaned[start:end + 1]

            try:
                return json.loads(json_text)

            except json.JSONDecodeError:
                pass

        raise ValueError(
            "LLM did not return valid JSON.\n\n"
            f"Raw response:\n{raw_response}"
        )

    # =========================================================
    # STRUCTURED OUTPUT
    # =========================================================

    def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[T],
    ) -> T:

        # Get Pydantic JSON schema
        schema = response_model.model_json_schema()

        # Strong system prompt
        structured_system_prompt = f"""
You are a structured data extraction system.

You MUST return ONLY JSON.

The JSON MUST follow this exact JSON Schema:

{json.dumps(schema, indent=2)}

IMPORTANT RULES:

- Return only JSON.
- Do not use Markdown.
- Do not write explanations.
- Do not write headings.
- Do not write bullet points.
- Do not create a wrapper such as "idea".
- Use the exact field names from the schema.
- Include every required field.
- Do not add unnecessary fields.
- Strings must be strings.
- Integers must be integers.
- Arrays must be JSON arrays.
"""

        last_error = None

        for attempt in range(self.max_retries):

            try:

                # -------------------------------------------------
                # Ollama Native API
                # -------------------------------------------------

                payload = {
                    "model": self.model,

                    "messages": [
                        {
                            "role": "system",
                            "content": structured_system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],

                    # IMPORTANT:
                    # Ollama supports passing the complete
                    # Pydantic JSON schema here.
                    "format": schema,

                    "stream": False,

                    "options": {
                        "temperature": 0.1,
                    },
                }

                headers = (
                    {"Authorization": f"Bearer {self.ollama_api_key}"}
                    if self.ollama_api_key
                    else {}
                )
                response = httpx.post(
                    f"{self.base_url}/api/chat",
                    headers=headers,
                    json=payload,
                    timeout=300.0,
                )

                response.raise_for_status()

                result = response.json()

                raw_response = (
                    result
                    .get("message", {})
                    .get("content", "")
                )

                if not raw_response:
                    raise ValueError(
                        "Ollama returned an empty structured response."
                    )

                # -------------------------------------------------
                # Parse JSON
                # -------------------------------------------------

                data = self._extract_json(
                    raw_response
                )

                # -------------------------------------------------
                # Validate using Pydantic
                # -------------------------------------------------

                return response_model.model_validate(
                    data
                )

            except Exception as exc:

                last_error = exc

                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        raise ValueError(
            f"Structured LLM generation failed for "
            f"{response_model.__name__}.\n\n"
            f"Error:\n{last_error}"
        ) from last_error


# =============================================================
# GLOBAL LLM CLIENT
# =============================================================

llm_client = LLMClient()
