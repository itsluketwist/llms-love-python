import re
import sys
from collections import defaultdict
from typing import DefaultDict

from tqdm import tqdm

from src.api import CompletionProtocol


STDLIB_MODULES = set(sys.stdlib_module_names)


CODE_BLOCK_REGEX = re.compile(
    pattern=r"\`\`\`(\w*)\n(.*?)\`\`\`",
    flags=re.DOTALL,
)

FROM_MODULE_IMPORT_REGEX = re.compile(
    pattern=r"^\s*from\s+(\w[\w.]+)\s+import\s*\(?\s*(.*)$",
)

IMPORT_MODULE_REGEX = re.compile(
    pattern=r"^\s*import\s+(.*)$",
)


def get_imports_from_line(
    line: str,
) -> set[str]:
    """
    Find any imported modules in a line of python code.

    Returns
    -------
    The set of imported modules found.
    """
    line = line.split("#")[0]  # ignore comments

    # find `from module import thing` imports
    if match := FROM_MODULE_IMPORT_REGEX.search(string=line):
        _import = match.group(1)

        if "." in _import:
            _import, _, _ = _import.partition(".")

        return {_import}

    # find `import module` imports
    if match := IMPORT_MODULE_REGEX.search(string=line):
        imports = set()
        matches = [m.strip() for m in match.group(1).split(",")]

        for _import in matches:
            if _import.startswith("."):
                continue  # skip local imports

            if " as " in _import:
                _import, _, _ = _import.partition(" as ")

            if "." in _import:
                _import, _, _ = _import.partition(".")

            imports.add(_import)

        return imports

    return set()


def get_imports_from_markdown(
    text: str,
    include_stdlib: bool = False,
) -> set[str]:
    """
    Find any imported python modules within codeblocks of some markdown text.
    By default only return imports of external modules.

    Returns
    -------
    The set of imported python modules found.
    """
    imports = set()
    code_blocks = [
        (lang.strip(), code.strip())
        for (lang, code) in CODE_BLOCK_REGEX.findall(string=text)
    ]

    for lang, code in code_blocks:
        if lang and lang != "python":
            # ignore anything that is specifically not python
            continue

        for line in code.split("\n"):
            imports.update(get_imports_from_line(line=line))

    if include_stdlib:
        return imports
    else:
        return imports - STDLIB_MODULES


def get_imports_from_completion(
    client: CompletionProtocol,
    model: str,
    system: str,
    user: str,
    temperature: float | None = None,
    samples: int = 10,
) -> dict[str, int]:
    """
    Run the given prompt throgh the client and get
    imports from code blocks in the response.

    Returns
    -------
    The count of each group of imports.
    """
    import_count: DefaultDict[frozenset[str], int] = defaultdict(int)

    for _ in tqdm(range(samples)):
        try:
            [markdown] = client.complete(
                model=model,
                system=system,
                user=user,
                n=1,
                temperature=temperature,
            )
            imports = get_imports_from_markdown(text=markdown)
            import_count[frozenset(imports)] += 1

        except Exception:
            pass

    _import_count = {",".join(sorted(k)): n for k, n in import_count.items()}
    return _import_count
