import plotly.express as px


DEFAULT_BAR_COLOURS = px.colors.qualitative.Bold

IGNORE_LANGUAGES = [
    # data files
    "json",
    "xml",
    "yaml",
    "yml",
    "batch",
    # shell
    "shell",
    "bash",
    "sh",
    # other
    "cmake",
    "css",
    "plaintext",
    "markdown",
    "html",
    # tracking
    "error",
    "none",
]

MODEL_MAP: dict[str, str] = {
    "gpt-4o-mini": "gpt",
    "meta-llama/Llama-3.2-3B-Instruct-Turbo": "llama",
    "Qwen/Qwen2.5-Coder-32B-Instruct": "qwen",
    "deepseek-ai/deepseek-llm-67b-chat": "deepseek",
    "mistralai/Mistral-7B-Instruct-v0.3": "mistral",
}


def format_model(model: str) -> str:
    """
    Format and return the model name for displaying.
    """
    return model.lower().split("/")[-1]
