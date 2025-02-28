"""All regexes used in the project are defined here."""

import re


# regex that extracts the languages of code blocks from markdown text
FIND_LANGUAGE_REGEX = re.compile(
    pattern=r"^\s*```([^\s]+)$",
    flags=re.MULTILINE,
)

# regex to extract code blocks from markdown text
CODE_BLOCK_REGEX = re.compile(
    pattern=r"\`\`\`(\w*)\n(.*?)(?:\`\`\`|$)",
    flags=re.DOTALL,
)

# regex to extract imports from python code: `from module import thing`
FROM_MODULE_IMPORT_REGEX = re.compile(
    pattern=r"^\s*from\s+(\w[\w.]+)\s+import\s*\(?\s*(.*)$",
)

# regex to extract imports from python code: `import module`
IMPORT_MODULE_REGEX = re.compile(
    pattern=r"^\s*import\s+(.*)$",
)
