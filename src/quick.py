from src.api import CompletionProtocol, OpenAICompletionAPI
from src.constants import BASE_SYSTEM_PROMPT


def quick_prompt(
    user: str,
    system: str = BASE_SYSTEM_PROMPT,
    client: CompletionProtocol | None = None,
) -> str:
    """
    Simple function to quickly prompt a model for a response.

    Returns
    -------
    The model response.
    """
    if client is None:
        client = OpenAICompletionAPI()

    result = client.complete(
        user=user,
        system=system,
    )
    return result[0]
