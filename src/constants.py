import re


# the default system prompt to be used across tasks
BASE_SYSTEM_PROMPT = "You are a helpful and knowledgeable code assistant!"


# regex that looks for the language of code blocks in text
FIND_LANGUAGE_REGEX = re.compile(
    pattern=r"^\s*```([^\s]+)$",
    flags=re.MULTILINE,
)

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
