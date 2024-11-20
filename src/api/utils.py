from src.api.completion import (
    AnthropicCompletionAPI,
    LlamaCompletionAPI,
    OpenAICompletionAPI,
)
from src.api.protocol import CompletionProtocol
from src.constants import BASE_SYSTEM_PROMPT


def get_client(model: str) -> CompletionProtocol:
    """
    Initialise the correct completion interface for the given model.
    """
    if "claude" in model:
        return AnthropicCompletionAPI()

    if "llama" in model:
        return LlamaCompletionAPI()

    return OpenAICompletionAPI()


def quick_complete(
    user: str,
    system: str = BASE_SYSTEM_PROMPT,
    model: str = "gpt-4o-mini",
) -> str:
    """
    Simple function to quickly prompt a model for a response.
    """
    client = get_client(model=model)

    result = client.complete(
        user=user,
        system=system,
        model=model,
    )
    return result[0]
