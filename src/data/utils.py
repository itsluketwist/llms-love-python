import random
from pathlib import Path

from src.data.constants import BAD_WORDS
from src.output import read_json, save_json


def remove_bad_records(data: list[str]) -> list[str]:
    """
    Remove records from a list of strings that contain 'bad' words.
    """
    new_data = []
    for item in data:
        item_lower = item.lower()
        if not any(word in item_lower for word in BAD_WORDS):
            new_data.append(item)

    return new_data


def process_data(
    file_path: str,
    remove_bias: bool = True,
    random_shuffle: bool = True,
):
    """
    Process a list of json data, removing bias and shuffling the data.
    """
    _path = Path(file_path)
    data = read_json(file_path=str(_path))

    if not isinstance(data, list):
        raise TypeError("Data file must contain a json list.")

    if remove_bias:
        data = remove_bad_records(data=data)

    if random_shuffle:
        random.shuffle(data)

    save_json(
        data=data,
        file_name=_path.stem,
        directory=str(_path.parent),
    )
