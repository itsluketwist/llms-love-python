"""Utility functions for processing the benchmark datasets."""

import random
import sys
from pathlib import Path

from src.json_utils import read_json, save_json


PYTHON_STDLIB_MODNAMES = getattr(sys, "stdlib_module_names", [])

# only remove stdlib modules with more than 4 characters to ensure matches are accurate
_BAD_PYTHON_STDLIB = [x for x in PYTHON_STDLIB_MODNAMES if len(x) > 4]

_BAD_WORDS = [
    "aspose-words",
    "bs4",
    "configparser",
    "datetime",
    "django",
    "docxtpl",
    "flask",
    "lxml",
    "matplotlib",
    "mechanize",
    "mock",
    "multidict",
    "numpy",
    "pytorch",
    "obspy",
    "openpyxl",
    "pandas",
    "pytz",
    "scikit-learn",
    "scipy",
    "seaborn",
    "selenium",
    "sqlalchemy",
    "statistics",
    "sympy",
    "tensorflow",
    "texttable",
    "xlrd",
    "xlwt",
    "python",
    "c++",
    "csharp",
    "java",
    "typescript",
    "php",
    "golang",
    "swift",
    "matlab",
    "ruby",
    "perl ",
    "objective-c",
    "dataframe",
    "brainfuck",
    "c#",
    "kotlin",
    "scala ",
    "cpp",
    "js ",
]


def remove_bad_records(
    data: list[str], include_python_stdlib: bool = False
) -> list[str]:
    """
    Remove records from a list of strings that contain 'bad' words.
    """
    _bad_words = _BAD_WORDS
    if include_python_stdlib:
        _bad_words += _BAD_PYTHON_STDLIB

    new_data = []
    for item in data:
        item_lower = item.lower()
        if not any(word in item_lower for word in _BAD_WORDS):
            new_data.append(item)

    return new_data


def process_data(
    file_path: str,
    remove_bias: bool = True,
    random_shuffle: bool = True,
    include_python_stdlib: bool = False,
):
    """
    Process a list of json data, removing bias and shuffling the data.
    """
    _path = Path(file_path)
    data = read_json(file_path=str(_path))

    if not isinstance(data, list):
        raise TypeError("Data file must contain a json list.")

    if remove_bias:
        data = remove_bad_records(
            data=data,
            include_python_stdlib=include_python_stdlib,
        )

    if random_shuffle:
        random.shuffle(data)

    save_json(
        data=data,
        file_path=str(_path),
    )
