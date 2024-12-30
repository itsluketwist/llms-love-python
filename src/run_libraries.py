from datetime import datetime

from tqdm import tqdm

from src.api import get_client
from src.constants import BASE_SYSTEM_PROMPT
from src.output import save_json
from src.python_imports import get_imports_from_completion


COMPARE_PROMPT = (
    "Compare the usage of {language} libraries {libraries} "
    "for the following task:\n\n{problem}"
)

LIBRARY_PROMPT = (
    "{problem}\n\n"
    "You should write self-contained {language} code.\n"
    "Import and use the {library} library, and explain if it's a good choice."
)

SOLVE_PROMPT = (
    "{problem}\n\n"
    "You should write self-contained {language} code.\n"
    "Choose, import and utilise at least one external library."
)


def get_solution_libraries(
    problems: dict[str, str],
    models: list[str],
    libraries: list[str] | None = None,
    language: str = "python",
    system_extra: str | None = None,
    temperature: float | None = None,
    samples: int = 10,
    save_directory: str = "output/library",
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

    if system_extra:
        system_prompt = f"{BASE_SYSTEM_PROMPT} {system_extra}"
    else:
        system_prompt = BASE_SYSTEM_PROMPT

    results: dict[str, dict] = {}
    for model in models:
        print(f"Prompting model {model} for solutions...")
        client = get_client(model=model)
        results[model] = {}

        for id, text in tqdm(problems.items()):
            print(f"Getting solutions for problem {id}...")
            results[model][id] = {}

            if libraries:
                compare_prompt = COMPARE_PROMPT.format(
                    language=language,
                    libraries=f"{', '.join(libraries[:-1])} and {libraries[-1]} ",
                    problem=text,
                )
                [compare_response] = client.complete(
                    model=model,
                    system=system_prompt,
                    user=compare_prompt,
                    n=1,
                    temperature=temperature,
                )
                results[model][id]["compare"] = compare_response

                for library in libraries:
                    library_prompt = LIBRARY_PROMPT.format(
                        problem=text,
                        language=language,
                        library=library,
                    )
                    [library_response] = client.complete(
                        model=model,
                        system=system_prompt,
                        user=library_prompt,
                        n=1,
                        temperature=temperature,
                    )
                    results[model][id][library] = library_response

            solve_prompt = SOLVE_PROMPT.format(
                problem=text,
                language=language,
            )
            import_counts = get_imports_from_completion(
                client=client,
                model=model,
                system=system_prompt,
                user=solve_prompt,
                temperature=temperature,
                samples=samples,
            )
            results[model][id]["counts"] = import_counts

    end = datetime.now().isoformat()
    data = {
        "metadata": {
            "dataset": run_id or "unspecified",
            "total": samples * len(problems),
            "start": start,
            "end": end,
            "temperature": temperature,
        },
        "prompt": {
            "system": system_prompt,
            "compare_prompt": COMPARE_PROMPT,
            "library_prompt": LIBRARY_PROMPT,
            "solve_prompt": SOLVE_PROMPT,
            "problem_texts": problems,
        },
        "results": results,
    }

    if run_id:
        file_name = f"solve_library_{run_id}_{end}"
    else:
        file_name = f"solve_library_{end}"

    save_json(
        data=data,
        file_name=file_name,
        directory=save_directory,
    )
    print(f"Results saved to file: {file_name}")

    return data
