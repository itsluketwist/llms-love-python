import os

from anthropic import NOT_GIVEN as ANTHOPIC_NOT_GIVEN
from anthropic import Anthropic
from openai import NOT_GIVEN as OPENAI_NOT_GIVEN
from openai import OpenAI


class OpenAICompletionAPI:
    """
    Class to access to OpenAI's API.
    """

    def __init__(self):
        self._client = OpenAI()
        self._model = "gpt-4o-mini"

    def complete(
        self,
        user: str,
        system: str,
        model: str,
        n: int = 1,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> list[str]:
        """
        Method to get the completion result of a prompt from an LLM model.

        Returns
        -------
        The textual response to the prompt.
        """
        response = self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            n=n,
            temperature=temperature or OPENAI_NOT_GIVEN,
            max_tokens=max_tokens or OPENAI_NOT_GIVEN,
        )
        choices = [c.message.content for c in response.choices]
        return choices


class LlamaCompletionAPI(OpenAICompletionAPI):
    """
    Class to access to Llama-API, using the OpenAI interface.
    """

    def __init__(self):
        self._client = OpenAI(
            api_key=os.environ["LLAMA_API_KEY"],
            base_url="https://api.llama-api.com/",
        )
        self._model = "llama3-8b"


class AnthropicCompletionAPI:
    """
    _summary_
    """

    def __init__(self) -> None:
        self._client = Anthropic()
        self._model = "claude-3-5-haiku-20241022"

    def complete(
        self,
        user: str,
        system: str,
        model: str,
        n: int = 1,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> list[str]:
        response = self._client.messages.create(
            model=model,
            temperature=temperature or ANTHOPIC_NOT_GIVEN,
            system=system,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user,
                        },
                    ],
                },
            ],
            max_tokens=max_tokens or 1000,
        )
        return [response.content[0].text]
