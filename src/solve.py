import json
from collections import defaultdict
from datetime import datetime
from typing import DefaultDict

from tqdm import tqdm

from src.api import CompletionProtocol
from src.constants import BASE_SYSTEM_PROMPT, FIND_LANGUAGE_REGEX
from src.output import save_json


def get_solution_languages(
    input_file: str,
    client: CompletionProtocol,
    models: list[str],
    system_extra: str | None = None,
    user_extra: str | None = None,
    limit: int | None = None,
) -> dict:
    """
    Prompt a set of models to find out what coding languages they will try to
    solve coding problems in, and the distribution between them.

    Returns
    -------
    A summary of the prompts and solution languages.
    """
    start = datetime.now().isoformat()

    with open(input_file, mode="r", encoding="utf-8") as f:
        input_texts = json.load(fp=f)

    if limit:
        input_texts = input_texts[:limit]

    if system_extra:
        system_solve = f"{BASE_SYSTEM_PROMPT} {system_extra}"
    else:
        system_solve = BASE_SYSTEM_PROMPT

    system_known = f"{BASE_SYSTEM_PROMPT} Your reply should be a comma seperated list of coding language names only."
    user_known = "What coding languages can you solve problems in?"

    results = {}
    for model in models:
        print(f"Prompting model {model} for solutions...")
        [known] = client.complete(
            model=model,
            system=system_known,
            user=user_known,
            n=1,
        )

        languages: DefaultDict[str, int] = defaultdict(int)
        for text in tqdm(input_texts):
            if user_extra:
                user_solve = f"{text} {user_extra}"
            else:
                user_solve = text

            [solution] = client.complete(
                model=model,
                system=system_solve,
                user=user_solve,
                n=1,
            )

            matches = FIND_LANGUAGE_REGEX.findall(string=solution)
            for match in matches:
                languages[match] += 1

        results[model] = {
            "known": known.split(", "),
            "solutions": dict(languages),
        }

    end = datetime.now().isoformat()
    data = {
        "prompt": {
            "known": {
                "system": system_known,
                "user": user_known,
            },
            "solve": {
                "system": system_solve,
                "user": user_solve,
            },
        },
        "datetime": {
            "start": start,
            "end": end,
        },
        "results": results,
    }

    file_name = f"solve_language_{end}"
    save_json(
        data=data,
        file_name=file_name,
    )
    print(f"Results saved to file: {file_name}")

    return data
