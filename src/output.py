import json
from pathlib import Path


def save_json(
    data: dict | list,
    file_name: str,
    directory: str = "data/output",
):
    """
    Utility to save python dictionary or list to a json file.
    """
    file_path = Path(directory, file_name).with_suffix(".json")
    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(obj=data, fp=f, indent=4)


def read_json(
    file_path: str,
) -> dict | list:
    """
    Utility to load python dictionary or list from a json file.
    """
    with open(file_path, mode="r", encoding="utf-8") as f:
        return json.load(fp=f)
