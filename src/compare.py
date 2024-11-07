from datetime import datetime

from src.api import CompletionProtocol
from src.constants import BASE_SYSTEM_PROMPT
from src.output import save_json
from src.python_imports import get_imports_from_completion


COMPARE_PROMPT = (
    "Compare the usage of {language} libraries {libraries} "
    "for writing a function to solve:\n{problem}"
)

LIBRARY_PROMPT = (
    "Write a python function to solve:\n{problem}\n\n"
    "You should write self-contained {language} code.\n"
    "Import and use the {library} library, and explain if it's a good choice."
)

SOLVE_PROMPT = (
    "Write a python function to solve:\n{problem}\n\n"
    "You should write self-contained {language} code.\n"
    "Choose, import and utilise at least one external library."
)


def get_compare_libraries(
    libraries: list[str],
    input_texts: dict[str, str],
    client: CompletionProtocol,
    models: list[str],
    language: str = "python",
    system_extra: str | None = None,
    temperature: float | None = None,
    samples: int = 10,
    save_directory: str = "data/output/library_compare",
) -> dict:
    """
    Prompt a set of models to compare their usage of specific
    coding libraries for solving coding problems.

    Returns
    -------
    A summary of the prompts and solution languages.
    """
    start = datetime.now().isoformat()

    if system_extra:
        system_prompt = f"{BASE_SYSTEM_PROMPT} {system_extra}"
    else:
        system_prompt = BASE_SYSTEM_PROMPT

    results: dict[str, dict] = {}
    for model in models:
        print(f"Prompting model {model} for solutions...")
        results[model] = {}

        for id, text in input_texts.items():
            print(f"Getting solutions for problem {id}...")
            results[model][id] = {}

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
            results[model][id]["import_counts"] = import_counts

    end = datetime.now().isoformat()
    data = {
        "prompt": {
            "system": system_prompt,
            "compare_prompt": COMPARE_PROMPT,
            "library_prompt": LIBRARY_PROMPT,
            "solve_prompt": SOLVE_PROMPT,
            "problem_texts": input_texts,
        },
        "datetime": {
            "start": start,
            "end": end,
        },
        "results": results,
    }

    file_name = f"compare_library_{end}"
    save_json(
        data=data,
        file_name=file_name,
        directory=save_directory,
    )
    print(f"Results saved to file: {file_name}")

    return data
