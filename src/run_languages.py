from collections import defaultdict
from datetime import datetime
from typing import DefaultDict

from tqdm import tqdm

from src.api import get_client
from src.constants import FIND_LANGUAGE_REGEX
from src.output import save_json
from src.prompts import BASE_SYSTEM_PROMPT, LANGUAGE_PROMPT_RANK


def get_solution_languages(
    tasks: list[str],
    models: list[str],
    pre_prompt: str | None = None,
    post_prompt: str | None = None,
    temperature: float | None = None,
    limit: int | None = None,
    repeat: bool = False,
    run_id: str | None = None,
    check_repeat: int = 1,
) -> dict:
    """
    Prompt a set of models to find out what coding languages they will try to
    solve coding problems in, and the distribution between them.

    Returns
    -------
    A summary of the prompts and solution languages.
    """
    print(f"Starting run {run_id}...")
    start = datetime.now().isoformat()

    user_check = LANGUAGE_PROMPT_RANK.format(task=tasks[0])

    if limit and repeat:
        if len(tasks) < limit:
            tasks = tasks * (int(limit / len(tasks)) + 1)
        tasks = tasks[:limit]
    elif limit:
        tasks = tasks[:limit]

    results = {}
    for model in models:
        print(f"Prompting model {model} for solutions...")
        client = get_client(model=model)

        checks = []
        for _ in range(check_repeat):
            [check] = client.complete(
                model=model,
                system=BASE_SYSTEM_PROMPT,
                user=user_check,
                n=1,
                temperature=temperature,
            )
            checks.append([k.strip() for k in check.split("\n")])

        languages: DefaultDict[str, int] = defaultdict(int)
        no_code_solutions = []
        for text in tqdm(tasks):
            user_solve = f"{pre_prompt or ''}{text}{post_prompt or ''}"
            try:
                [solution] = client.complete(
                    model=model,
                    system=BASE_SYSTEM_PROMPT,
                    user=user_solve,
                    n=1,
                    temperature=temperature,
                )

                matches = FIND_LANGUAGE_REGEX.findall(string=solution)

                for match in set(matches):
                    languages[match.lower().strip()] += 1

                if not matches:
                    languages["none"] += 1
                    no_code_solutions.append(solution)

            except Exception:
                languages["error"] += 1

        results[model] = {
            "check": checks,
            "counts": dict(languages),
            "none": no_code_solutions,
        }

    end = datetime.now().isoformat()
    data = {
        "metadata": {
            "dataset": run_id or "unspecified",
            "total": len(tasks),
            "start": start,
            "end": end,
            "temperature": temperature,
            "models": models,
        },
        "prompts": {
            "system": BASE_SYSTEM_PROMPT,
            "pre_prompt": pre_prompt,
            "post_prompt": post_prompt,
            "check": user_check,
            "solve": f"{pre_prompt or ''}{{code problem}}{post_prompt or ''}",
            "problem": tasks[0],
        },
        "results": results,
    }

    save_path = f"output/language/{run_id or 'lang'}_results_{end}.json"
    save_json(
        data=data,
        file_path=save_path,
    )
    print(f"Results saved to file: {save_path}")

    return data
