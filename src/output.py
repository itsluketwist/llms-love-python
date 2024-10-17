import json
from pathlib import Path


def save_json(
    data: dict,
    file_name: str,
    directory: str = "data/output",
):
    """
    Utility to save python dictionary to a json file.
    """
    file_path = Path(directory, file_name).with_suffix(".json")
    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(obj=data, fp=f, indent=4)
