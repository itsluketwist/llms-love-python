from collections import defaultdict
from datetime import datetime
from typing import DefaultDict

from tqdm import tqdm

from src.api import CompletionProtocol
from src.constants import BASE_SYSTEM_PROMPT
from src.output import save_json


def get_library_suggestions(
    library_type: str,
    code_language: str,
    client: CompletionProtocol,
    models: list[str],
    samples: int = 100,
    batch_size: int = 1,
    prompt_extra: str | None = None,
    temperature: float | None = None,
) -> dict:
    """
    Prompt a set of models to find out what coding libraries they know and how
    the models distribute their suggestions between them.

    Returns
    -------
    A summary of the prompts and suggestions.
    """
    system_known = f"{BASE_SYSTEM_PROMPT} Your reply should be a comma seperated list of library names only."
    user_known = f"What {library_type} libraries in {code_language} can I choose from?"

    system_suggest = f"{BASE_SYSTEM_PROMPT} Your reply should be the library name only."
    user_suggest = f"What {library_type} library in {code_language} should I use for my new project?"

    if prompt_extra is not None:
        user_suggest += f" {prompt_extra}"

    return _get_suggestions(
        suggest_type="library",
        system_known=system_known,
        user_known=user_known,
        system_suggest=system_suggest,
        user_suggest=user_suggest,
        client=client,
        models=models,
        samples=samples,
        batch_size=batch_size,
        temperature=temperature,
    )


def get_language_suggestions(
    client: CompletionProtocol,
    models: list[str],
    samples: int = 100,
    batch_size: int = 1,
    prompt_extra: str | None = None,
    temperature: float | None = None,
) -> dict:
    """
    Prompt a set of models to find out what coding languages they know and how
    the models distribute their suggestions between them.

    Returns
    -------
    A summary of the prompts and suggestions.
    """
    system_known = f"{BASE_SYSTEM_PROMPT} Your reply should be a comma seperated list of coding language names only."
    user_known = "What coding languages can I choose from?"

    system_suggest = (
        f"{BASE_SYSTEM_PROMPT} Your reply should be the coding language name only."
    )
    user_suggest = "What coding language should I use for my new project? I will choose the project after I know the language."

    if prompt_extra is not None:
        user_suggest += f" {prompt_extra}"

    return _get_suggestions(
        suggest_type="language",
        system_known=system_known,
        user_known=user_known,
        system_suggest=system_suggest,
        user_suggest=user_suggest,
        client=client,
        models=models,
        samples=samples,
        batch_size=batch_size,
        temperature=temperature,
    )


def _get_suggestions(
    suggest_type: str,
    system_known: str,
    user_known: str,
    system_suggest: str,
    user_suggest: str,
    client: CompletionProtocol,
    models: list[str],
    samples: int = 100,
    batch_size: int = 1,
    temperature: float | None = None,
) -> dict:
    """
    Prompt a set of models to find out what options are known and how
    the models distribute their suggestions between them.

    Returns
    -------
    A summary of the prompts and suggestions.
    """
    start = datetime.now().isoformat()

    results = {}
    for model in models:
        print(f"Prompting model {model} for {suggest_type} suggestions...")
        [known] = client.complete(
            model=model,
            system=system_known,
            user=user_known,
            n=1,
            temperature=temperature,
        )

        suggestions: DefaultDict[str, int] = defaultdict(int)
        for _ in tqdm(range(samples // batch_size)):
            choices = client.complete(
                model=model,
                system=system_suggest,
                user=user_suggest,
                n=batch_size,
                temperature=temperature,
            )
            for choice in choices:
                suggestions[choice.lower()] += 1

        results[model] = {
            "known": known.split(", "),
            "suggestions": dict(suggestions),
        }

    end = datetime.now().isoformat()
    data = {
        "prompt": {
            "known": {
                "system": system_known,
                "user": user_known,
            },
            "suggest": {
                "system": system_suggest,
                "user": user_suggest,
            },
        },
        "datetime": {
            "start": start,
            "end": end,
        },
        "results": results,
    }

    file_name = f"suggest_{suggest_type}_{end}"
    save_json(
        data=data,
        file_name=file_name,
    )
    print(f"Results saved to file: {file_name}")

    return data
