import os
from typing import Protocol

from openai import NOT_GIVEN, OpenAI


class CompletionProtocol(Protocol):
    """
    Protocol that describes how to access the completion API of an LLM service.
    """

    def complete(
        self,
        user: str,
        system: str,
        model: str,
        n: int = 1,
        temperature: float | None = None,
    ) -> list[str]:
        pass


class OpenAICompletionAPI:
    """
    Class to access to OpenAI's API.
    """

    def __init__(self):
        self._client = OpenAI()

    def complete(
        self,
        user: str,
        system: str,
        model: str,
        n: int = 1,
        temperature: float | None = None,
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
            temperature=temperature or NOT_GIVEN,
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
