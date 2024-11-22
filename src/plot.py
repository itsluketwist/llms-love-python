import math
from collections import defaultdict
from typing import DefaultDict

import plotly.express as px
import plotly.graph_objects as go
from plotly_utils import default_figure

from src.output import read_json


DEFAULT_COLOR_SCHEME = px.colors.qualitative.Bold * 3


def _format_results(
    _list: list,
    _num: int = 5,
    _log: bool = True,
) -> list:
    """
    Correctly format a list of results, ready to be plotted.
    """
    _list.sort(reverse=True)

    if _log:
        _list = [math.log(_i) for _i in _list]

    while True:
        if len(_list) >= _num:
            return _list[:_num]
        else:
            _list += [-1 if _log else 0]


def plot_line_results(
    data: dict[str, list[int]],
    title: str,
    x_title: str | None = None,
    y_title: str | None = None,
    x_len: int = 5,
    y_log: bool = True,
) -> go.Figure:
    """
    Plot the given result data onto a scatter plot with lines.

    Returns
    -------
    The created figure.
    """
    x_ticks = ["Most common<br>suggestion", "2nd most<br>common", "3rd"]
    while len(x_ticks) < x_len:
        x_ticks.append(f"{len(x_ticks) + 1}th")

    lines = []
    for idx, (key, value) in enumerate(data.items()):
        lines.append(
            go.Scatter(
                x=x_ticks,
                y=_format_results(
                    _list=list(value),
                    _num=x_len,
                    _log=y_log,
                ),
                name=key,
                mode="lines+markers",
                marker_color=DEFAULT_COLOR_SCHEME[idx],
                line_color=DEFAULT_COLOR_SCHEME[idx],
            )
        )

    figure = default_figure(
        title=title,
        data=lines,
        x_title=x_title,
        y_title=y_title,
    )

    if y_log:
        tens = [1, 10, 100, 1000, 10000]
        figure.update_layout(
            yaxis=dict(
                tickmode="array",
                tickvals=[-1] + [math.log(t) for t in tens],
                ticktext=["0"] + [str(t) for t in tens],
            )
        )

    return figure


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
                marker_color=DEFAULT_COLOR_SCHEME[i],
            )
        )

    figure = default_figure(
        title=title,
        data=charts,
        x_title=x_title,
        y_title=y_title,
    )
    return figure


def plot_languages(
    results: str,
    dataset: str,
    descending: bool | None = True,
    percentage: bool = False,
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
        title=f"Languages used when solving problems in the <b>{dataset}</b> dataset",
        x_title=None,
        y_title=f"Problems solved (<b>{'%' if percentage else '#'}</b>)",
        descending=descending,
    )
    return figure


def plot_libraries(
    results: str,
    domain: str,
    descending: bool | None = True,
    percentage: bool = False,
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
        title=f"Libraries used when solving <b>{domain}</b> problems",
        x_title=None,
        y_title=f"Problems where library was imported (<b>{'%' if percentage else '#'}</b>)",
        descending=descending,
    )
    return figure
