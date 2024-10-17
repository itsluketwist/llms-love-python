from typing import Protocol


class CompletionProtocol(Protocol):
    """
    Protocol that describes how to access the completion API of an LLM service.
    """

    def complete(
        self,
        user: str,
        system: str,
        model: str,
    ) -> str:
        """
        Method to get the result of a prompt from an LLM model.

        Returns
        -------
        The textual response to the prompt.
        """
        pass
