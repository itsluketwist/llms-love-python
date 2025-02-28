"""Code to run language preference experiments."""

from collections import defaultdict
from datetime import datetime
from typing import DefaultDict

from tqdm import tqdm

from src.api import get_client
from src.json_utils import save_json
from src.prompts import BASE_SYSTEM_PROMPT, LANGUAGE_PROMPT_RANK
from src.regexes import FIND_LANGUAGE_REGEX


def get_solution_languages(
    tasks: list[str],
    models: list[str],
    limit: int | None = None,
    pre_prompt: str | None = None,
    post_prompt: str | None = None,
    temperature: float | None = None,
    samples: int = 3,
    rank_repeat: int = 3,
    run_id: str | None = None,
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

    # rank languages for first task, to be used as a check
    rank_prompt = LANGUAGE_PROMPT_RANK.format(task=tasks[0])

    # limit the number of tasks if needed
    if limit:
        tasks = tasks[:limit]

    results = {}
    for model in models:
        print(f"Prompting model {model} for solutions...")
        client = get_client(model=model)  # configure the client for the model

        # get the ranks of the languages recommended to solve the first problem
        rank_results = []
        for _ in range(rank_repeat):
            [check] = client.complete(
                model=model,
                system=BASE_SYSTEM_PROMPT,
                user=rank_prompt,
                n=1,
                temperature=temperature,
            )
            rank_results.append([k.strip() for k in check.split("\n")])

        # initialise result storage
        counts_per_problem: DefaultDict[str, int] = defaultdict(int)
        counts_per_response: DefaultDict[str, int] = defaultdict(int)
        used_per_problem = {}
        no_code_solutions = []

        # get languages used to solve each task
        for idx, text in tqdm(enumerate(tasks)):
            solve_prompt = (
                f"{pre_prompt or ''}{text}{post_prompt or ''}"  # build prompt
            )
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

                    # extract and parse languages from the solution
                    matches = FIND_LANGUAGE_REGEX.findall(string=solution)
                    if not matches:
                        parsed = {"none"}
                        no_code_solutions.append(solution)
                    else:
                        parsed = set([m.lower().strip() for m in matches])

                    # save sample results
                    _used_set.update(parsed)
                    _used_groups.append(",".join(parsed))
                    for lang in parsed:
                        counts_per_response[lang] += 1

                # save task results
                used_per_problem[idx] = _used_groups
                for lang in _used_set:
                    counts_per_problem[lang] += 1

            except Exception:
                counts_per_problem["error"] += 1

        results[model] = {
            "ranks": rank_results,
            "counts_per_response": dict(counts_per_response),
            "counts_per_problem": dict(counts_per_problem),
            "used_per_problem": used_per_problem,
            "none": no_code_solutions,
        }

    # save the results to file
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
            "check": rank_prompt if rank_repeat else "none",
            "problem": tasks[0],
        },
        "results": results,
    }
    save_path = f"output/language_results/{run_id or 'lang'}_results_{end}.json"
    save_json(
        data=data,
        file_path=save_path,
    )
    print(f"Results saved to file: {save_path}")

    return data
