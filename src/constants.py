import re


# regex that looks for the language of code blocks in text
FIND_LANGUAGE_REGEX = re.compile(
    pattern=r"^\s*```([^\s]+)$",
    flags=re.MULTILINE,
)

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
