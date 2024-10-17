from openai import OpenAI


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
    ) -> str:
        """
        Method to get the result of a prompt from an OpenAI model.

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
        )
        completion = response.choices[0].message.content
        return completion
