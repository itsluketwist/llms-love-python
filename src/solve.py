from collections import defaultdict
from datetime import datetime
from typing import DefaultDict

from tqdm import tqdm

from src.api import get_client
from src.constants import BASE_SYSTEM_PROMPT, FIND_LANGUAGE_REGEX
from src.output import read_json, save_json
from src.python_imports import get_imports_from_completion


def get_solution_languages(
    input_file: str,
    models: list[str],
    system_extra: str | None = None,
    user_extra: str | None = None,
    temperature: float | None = None,
    limit: int | None = None,
    repeat: int | None = None,
    save_directory: str = "data/output",
) -> dict:
    """
    Prompt a set of models to find out what coding languages they will try to
    solve coding problems in, and the distribution between them.

    Returns
    -------
    A summary of the prompts and solution languages.
    """
    start = datetime.now().isoformat()

    input_texts = read_json(file_path=input_file)
    assert isinstance(input_texts, list)
    if repeat:
        input_texts = input_texts * repeat
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
        client = get_client(model=model)
        [known] = client.complete(
            model=model,
            system=system_known,
            user=user_known,
            n=1,
            temperature=temperature,
        )

        languages: DefaultDict[str, int] = defaultdict(int)
        for text in tqdm(input_texts):
            try:
                if user_extra:
                    user_solve = f"{text} {user_extra}"
                else:
                    user_solve = text

                [solution] = client.complete(
                    model=model,
                    system=system_solve,
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
            "known": [k.strip() for k in known.split(", ")],
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
                "user": f"{{code problem}} {user_extra}",
            },
            "problem_texts": input_file,
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
        directory=save_directory,
    )
    print(f"Results saved to file: {file_name}")

    return data


def get_solution_libraries(
    input_texts: list[str],
    models: list[str],
    system_extra: str | None = None,
    user_extra: str | None = None,
    temperature: float | None = None,
    samples: int = 10,
    save_directory: str = "data/output",
) -> dict:
    """
    Prompt a set of models to find out what coding languages they will try to
    solve coding problems in, and the distribution between them.

    Returns
    -------
    A summary of the prompts and solution languages.
    """
    start = datetime.now().isoformat()

    if system_extra:
        system_solve = f"{BASE_SYSTEM_PROMPT} {system_extra}"
    else:
        system_solve = BASE_SYSTEM_PROMPT

    results: dict[str, list] = {}
    for model in models:
        client = get_client(model=model)
        results[model] = []

        for text in input_texts:
            if user_extra:
                user_solve = f"{text} {user_extra}"
            else:
                user_solve = text

            libraries = get_imports_from_completion(
                client=client,
                model=model,
                system=system_solve,
                user=user_solve,
                temperature=temperature,
                samples=samples,
            )

            results[model].append(
                {
                    "problem": text,
                    "libraries": libraries,
                }
            )

    end = datetime.now().isoformat()
    data = {
        "prompt": {
            "solve": {
                "system": system_solve,
                "user": f"{{code problem}} {user_extra}",
            },
            "problem_texts": input_texts,
        },
        "datetime": {
            "start": start,
            "end": end,
        },
        "results": results,
    }

    file_name = f"solve_library_{end}"
    save_json(
        data=data,
        file_name=file_name,
        directory=save_directory,
    )
    print(f"Results saved to file: {file_name}")

    return data
