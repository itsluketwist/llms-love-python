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
    run_id: str | None = None,
    check_repeat: int = 3,
    samples: int = 3,
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

    if limit:
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
        languages_per_problem = {}
        for idx, text in tqdm(enumerate(tasks)):
            solve_prompt = f"{pre_prompt or ''}{text}{post_prompt or ''}"
            try:
                _used_set = set()
                _used_groups = []
                for _ in range(samples):
                    [solution] = client.complete(
                        model=model,
                        system=BASE_SYSTEM_PROMPT,
                        user=solve_prompt,
                        n=1,
                        temperature=temperature,
                    )

                    matches = FIND_LANGUAGE_REGEX.findall(string=solution)
                    if not matches:
                        parsed = {"none"}
                        no_code_solutions.append(solution)
                    else:
                        parsed = set([m.lower().strip() for m in matches])

                    _used_set.update(parsed)
                    _used_groups.append(",".join(parsed))

                languages_per_problem[idx] = _used_groups
                for lang in _used_set:
                    languages[lang] += 1

            except Exception:
                languages["error"] += 1

        results[model] = {
            "check": checks,
            "counts": dict(languages),
            "used": languages_per_problem,
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
            "check": user_check if check_repeat else "none",
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
