from collections import defaultdict
from datetime import datetime
from typing import DefaultDict

from tqdm import tqdm

from src.api import get_client
from src.constants import BASE_SYSTEM_PROMPT, FIND_LANGUAGE_REGEX
from src.output import save_json


def get_solution_languages(
    tasks: list[str],
    models: list[str],
    system_extra: str | None = None,
    user_extra: str | None = None,
    temperature: float | None = None,
    limit: int | None = None,
    repeat: int | None = None,
    save_directory: str = "data/output/language",
    run_id: str | None = None,
) -> dict:
    """
    Prompt a set of models to find out what coding languages they will try to
    solve coding problems in, and the distribution between them.

    Returns
    -------
    A summary of the prompts and solution languages.
    """
    start = datetime.now().isoformat()

    if len(tasks) == 1:
        user_check = (
            f"What is the best coding language for the following task: {tasks[0]}"
        )
    else:
        user_check = "What coding languages can you complete tasks in?"

    if limit:
        if len(tasks) < limit:
            tasks = tasks * (limit % len(tasks) + 1)
        tasks = tasks[:limit]
    elif repeat:
        tasks = tasks * repeat

    if system_extra:
        system_prompt = f"{BASE_SYSTEM_PROMPT} {system_extra}"
    else:
        system_prompt = BASE_SYSTEM_PROMPT

    results = {}
    for model in models:
        print(f"Prompting model {model} for solutions...")
        client = get_client(model=model)
        [check] = client.complete(
            model=model,
            system=BASE_SYSTEM_PROMPT,
            user=user_check,
            n=1,
            temperature=temperature,
        )

        languages: DefaultDict[str, int] = defaultdict(int)
        for text in tqdm(tasks):
            try:
                if user_extra:
                    user_solve = f"{text} {user_extra}"
                else:
                    user_solve = text

                [solution] = client.complete(
                    model=model,
                    system=system_prompt,
                    user=user_solve,
                    n=1,
                    temperature=temperature,
                )

                matches = FIND_LANGUAGE_REGEX.findall(string=solution)
                for match in set(matches):
                    languages[match.lower().strip()] += 1

            except Exception:
                pass

        results[model] = {
            "check": [k.strip() for k in check.split("\n")],
            "counts": dict(languages),
        }

    end = datetime.now().isoformat()
    data = {
        "metadata": {
            "dataset": run_id or "unspecified",
            "start": start,
            "end": end,
        },
        "prompts": {
            "system": system_prompt,
            "check": user_check,
            "solve": f"{{code problem}} {user_extra}",
        },
        "results": results,
    }

    if run_id:
        file_name = f"solve_language_{run_id}_{end}"
    else:
        file_name = f"solve_language_{end}"

    save_json(
        data=data,
        file_name=file_name,
        directory=save_directory,
    )
    print(f"Results saved to file: {file_name}")

    return data
