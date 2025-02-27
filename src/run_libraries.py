from datetime import datetime

from tqdm import tqdm

from src.api import get_client
from src.json_utils import save_json
from src.prompts import (
    BASE_SYSTEM_PROMPT,
    LIBRARY_PROMPT_COMPARE,
    LIBRARY_PROMPT_RANK,
    LIBRARY_PROMPT_USE_ANY,
    LIBRARY_PROMPT_USE_ONE,
)
from src.python_analysis import get_imports_from_completion


def get_solution_libraries(
    problems: dict[str, str],
    models: list[str],
    libraries: list[str] | None = None,
    language: str = "python",
    pre_prompt: str | None = None,
    post_prompt: str | None = None,
    temperature: float | None = None,
    samples: int = 3,
    rank_repeat: int = 0,
    run_id: str | None = None,
) -> dict:
    """
    Prompt a set of models to compare their usage of specific
    coding libraries for solving coding problems.

    Returns
    -------
    A summary of the prompts, responses and libraries used in the solutions.
    """
    print(f"Starting run {run_id}...")
    start = datetime.now().isoformat()

    results: dict[str, dict] = {}
    for model in models:
        print(f"Prompting model {model} for solutions...")
        client = get_client(model=model)  # configure the client for the model

        results[model] = {}
        for id, text in tqdm(problems.items()):
            results[model][id] = {}
            text = f"{pre_prompt or ''}{text}{post_prompt or ''}"  # build prompt

            # if libraries:
            #     compare_prompt = LIBRARY_PROMPT_COMPARE.format(
            #         language=language,
            #         libraries=f"{', '.join(libraries[:-1])} and {libraries[-1]} ",
            #         problem=text,
            #     )
            #     [compare_response] = client.complete(
            #         model=model,
            #         system=BASE_SYSTEM_PROMPT,
            #         user=compare_prompt,
            #         n=1,
            #         temperature=temperature,
            #     )
            #     results[model][id]["compare"] = compare_response

            #     for library in libraries:
            #         library_prompt = LIBRARY_PROMPT_USE_ONE.format(
            #             problem=text,
            #             language=language,
            #             library=library,
            #         )
            #         [library_response] = client.complete(
            #             model=model,
            #             system=BASE_SYSTEM_PROMPT,
            #             user=library_prompt,
            #             n=1,
            #             temperature=temperature,
            #         )
            #         results[model][id][library] = library_response

            # get the ranks of the libraries recommended to solve the problem
            if rank_repeat:
                rank_prompt = LIBRARY_PROMPT_RANK.format(
                    problem=text,
                    language=language,
                )
                ranks = []
                for _ in range(rank_repeat):
                    [rank_response] = client.complete(
                        model=model,
                        system=BASE_SYSTEM_PROMPT,
                        user=rank_prompt,
                        n=1,
                        temperature=temperature,
                    )
                    ranks.append([k.strip() for k in rank_response.split("\n")])
                results[model][id]["ranks"] = ranks

            # get libraries used to solve the problem
            if samples:
                solve_prompt = LIBRARY_PROMPT_USE_ANY.format(
                    problem=text,
                    language=language,
                )
                import_counts = get_imports_from_completion(
                    client=client,
                    model=model,
                    system=BASE_SYSTEM_PROMPT,
                    user=solve_prompt,
                    temperature=temperature,
                    samples=samples,
                )
                results[model][id]["counts"] = import_counts

    # save the results to file
    end = datetime.now().isoformat()
    data = {
        "metadata": {
            "dataset": run_id or "unspecified",
            "total": samples * len(problems),
            "start": start,
            "end": end,
            "temperature": temperature,
            "models": models,
        },
        "prompt": {
            "system": BASE_SYSTEM_PROMPT,
            "compare_prompt": LIBRARY_PROMPT_COMPARE,
            "library_prompt": LIBRARY_PROMPT_USE_ONE,
            "solve_prompt": LIBRARY_PROMPT_USE_ANY,
            "pre_prompt": pre_prompt,
            "post_prompt": post_prompt,
            "problem_texts": problems,
        },
        "results": results,
    }
    save_path = f"output/library_results/{run_id or 'library'}_results_{end}.json"
    save_json(
        data=data,
        file_path=save_path,
    )
    print(f"Results saved to file: {save_path}")

    return data
