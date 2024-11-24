from collections import defaultdict
from typing import DefaultDict

import plotly.express as px
import plotly.graph_objects as go
from plotly_utils import default_figure

from src.output import read_json


DEFAULT_BAR_COLOURS = px.colors.qualitative.Bold


def plot_bar_results(
    data: dict[str, dict[str, int | float]],
    title: str,
    x_title: str | None = None,
    y_title: str | None = None,
    descending: bool | None = True,
) -> go.Figure:
    """
    Plot the given result data onto a scatter plot with lines.

    Returns
    -------
    The created figure.
    """
    all_keys = set()
    for results in data.values():
        all_keys.update(set(results.keys()))

    charts = []
    for i, (model, results) in enumerate(data.items()):
        for _key in all_keys:
            if _key not in results:
                results[_key] = 0

        data_pairs = list(results.items())

        if descending is not None:
            data_pairs = sorted(data_pairs, key=lambda x: x[1], reverse=descending)

        bars = [d[0] for d in data_pairs]
        values = [d[1] for d in data_pairs]

        charts.append(
            go.Bar(
                name=model,
                x=bars,
                y=values,
                text=[round(v, 2) for v in values],
                marker_color=DEFAULT_BAR_COLOURS[i],
            )
        )

    figure = default_figure(
        title=title,
        data=charts,
        x_title=x_title,
        y_title=y_title,
    )
    return figure


def plot_bar_languages(
    results: str,
    dataset: str,
    descending: bool | None = True,
    percentage: bool = False,
    title: str | None = None,
) -> go.Figure:
    raw = read_json(file_path=results)
    if not isinstance(raw, dict):
        raise TypeError("Results file must contain a json dictionary.")

    data = {}
    for model, _data in raw["results"].items():
        if percentage:
            total = sum(_data["counts"].values())
            data[model] = {k: v * 100 / total for k, v in _data["counts"].items()}
        else:
            data[model] = _data["counts"]

    figure = plot_bar_results(
        data=data,
        title=title
        or f"Languages used when solving problems in the <b>{dataset}</b> dataset",
        x_title=None,
        y_title=f"Solutions where language was used (<b>{'%' if percentage else '#'}</b>)",
        descending=descending,
    )
    return figure


def plot_bar_libraries(
    results: str,
    domain: str,
    descending: bool | None = True,
    percentage: bool = False,
    title: str | None = None,
) -> go.Figure:
    raw = read_json(file_path=results)
    if not isinstance(raw, dict):
        raise TypeError("Results file must contain a json dictionary.")

    data = {}
    for model, _data in raw["results"].items():
        counts: DefaultDict[str, int] = defaultdict(int)
        total = 0
        for _, problem_data in _data.items():
            for imports, count in problem_data["counts"].items():
                total += count
                for _import in imports.split(","):
                    counts[_import] += count

        if percentage:
            data[model] = {k: v * 100 / total for k, v in counts.items()}
        else:
            data[model] = dict(counts)

    figure = plot_bar_results(
        data=data,
        title=title or f"Libraries used when solving <b>{domain}</b> problems",
        x_title=None,
        y_title=f"Solutions where library was imported (<b>{'%' if percentage else '#'}</b>)",
        descending=descending,
    )
    return figure
