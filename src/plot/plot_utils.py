from collections import defaultdict

import plotly.express as px


DEFAULT_COLOURS = px.colors.qualitative.Bold * 2


def new_colours(colours: list[str] = DEFAULT_COLOURS):
    """
    Generate a new colour from the default plotly colours.
    """

    def _generator_func():
        for colour in colours:
            yield colour

    _generator = _generator_func()

    return defaultdict(lambda: next(_generator))


LANGUAGE_COLOURS = {
    "python": DEFAULT_COLOURS[0],
    "java": DEFAULT_COLOURS[1],
    "javascript": DEFAULT_COLOURS[2],
    "cpp": DEFAULT_COLOURS[3],
    "c": DEFAULT_COLOURS[4],
    "go": DEFAULT_COLOURS[6],
    "dart": DEFAULT_COLOURS[7],
    "csharp": DEFAULT_COLOURS[9],
    "none": "DarkSlateBlue",
}

LIBRARY_COLOURS = [
    "DodgerBlue",
    DEFAULT_COLOURS[3],
    DEFAULT_COLOURS[4],
    "Crimson",
    "Violet",
]

IGNORE_FILETYPES = [
    # data files
    "json",
    "xml",
    "yaml",
    "yml",
    "batch",
    "toml",
    "qml",
    # other
    "makefile",
    "cmake",
    "css",
    "plaintext",
    "plain",
    "txt",
    "markdown",
    "mark",
    "html",
    "nginx",
    "docker",
    "dockerfile",
    "graphql",
    "textlint",
    # tracking keys
    "error",
    # "none",
]

SCRIPTING_LANGUAGES = [
    "bash",
    "shell",
    "sh",
    "powershell",
]

MODEL_MAP: dict[str, str] = {
    "gpt-4o-mini": "gpt-4o",
    "gpt-3.5-turbo": "gpt-3.5",
    "gpt-4o-mini-2024-07-18": "GPT-4o",
    "gpt-3.5-turbo-0125": "GPT-3.5",
    "meta-llama/Llama-3.2-3B-Instruct-Turbo": "Llama3.2",
    "Qwen/Qwen2.5-Coder-32B-Instruct": "Qwen2.5",
    "deepseek-ai/deepseek-llm-67b-chat": "DeepSeekLLM",
    "mistralai/Mistral-7B-Instruct-v0.3": "Mistral7b",
    "claude-3-5-sonnet-20241022": "Sonnet3.5",
    "claude-3-5-haiku-20241022": "Haiku3.5",
}


def format_model(model: str) -> str:
    """
    Format and return the model name for displaying.
    """
    if model in MODEL_MAP:
        short = MODEL_MAP[model]
    else:
        short = model.lower().split("/")[-1]

    return f"<b>{short}</b>"
