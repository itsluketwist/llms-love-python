from collections import defaultdict
from typing import DefaultDict

import plotly.graph_objects as go
from plotly_utils import default_figure

from src.output import read_json
from src.plot.utils import (
    DEFAULT_BAR_COLOURS,
    IGNORE_LANGUAGES,
    MODEL_MAP,
    format_model,
)


def plot_bar_results(
    data: dict[str, dict[str, int | float]],
    title: str,
    x_title: str | None = None,
    y_title: str | None = None,
    order: str = "total descending",
) -> go.Figure:
    """
    Plot the given result data onto a scatter plot with lines.

    Returns
    -------
    The created figure.
    """
    items = []
    models = []
    values = []
    colors = []
    legend = []
    for i, (model, results) in enumerate(data.items()):
        pairs = [(k, v) for k, v in results.items() if k not in IGNORE_LANGUAGES]
        pairs.sort(key=lambda x: x[1], reverse=True)
        legend.append((format_model(model=model), DEFAULT_BAR_COLOURS[i]))
        for item, count in pairs:
            items.append(f"<b>{item}</b>")
            models.append(MODEL_MAP[model])
            values.append(count)
            colors.append(DEFAULT_BAR_COLOURS[i])

    figure = default_figure(
        title=title,
        data=go.Bar(
            x=[items, models],
            y=values,
            text=[round(v, 2) for v in values],
            marker_color=colors,
        ),
        x_title=x_title,
        y_title=y_title,
    )
    figure.update_layout(
        xaxis_categoryorder=order,
        bargap=0.1,
    )
    figure.add_traces(
        data=[
            go.Bar(
                name=m,
                x=[1],
                marker_color=c,
                showlegend=True,
            )
            for m, c in legend
        ]
    )
    return figure


def plot_bar_languages(
    results: str,
    percentage: bool = False,
    title: str | None = None,
    dataset: str | None = None,
    order: str = "total descending",
) -> go.Figure:
    if title is None and dataset is None:
        raise TypeError("One of title or dataset must not be None.")

    raw = read_json(file_path=results)
    if not isinstance(raw, dict):
        raise TypeError("Results file must contain a json dictionary.")

    data = {}
    for model, _data in raw["results"].items():
        if percentage:
            total = raw["metadata"]["total"]
            data[model] = {k: v * 100 / total for k, v in _data["counts"].items()}
        else:
            data[model] = _data["counts"]

    figure = plot_bar_results(
        data=data,
        title=title
        or f"Languages used when solving problems in the <b>{dataset}</b> dataset",
        x_title=None,
        y_title=f"Solutions where language was used (<b>{'%' if percentage else '#'}</b>)",
        order=order,
    )
    return figure


def plot_bar_libraries(
    results: str,
    domain: str,
    percentage: bool = False,
    title: str | None = None,
    order: str = "total descending",
) -> go.Figure:
    raw = read_json(file_path=results)
    if not isinstance(raw, dict):
        raise TypeError("Results file must contain a json dictionary.")

    data = {}
    for model, _data in raw["results"].items():
        counts: DefaultDict[str, int] = defaultdict(int)
        for _, problem_data in _data.items():
            for imports, count in problem_data["counts"].items():
                for _import in imports.split(","):
                    counts[_import] += count

        if percentage:
            total = raw["metadata"]["total"]
            data[model] = {k: v * 100 / total for k, v in counts.items()}
        else:
            data[model] = dict(counts)

    figure = plot_bar_results(
        data=data,
        title=title or f"Libraries used when solving <b>{domain}</b> problems",
        x_title=None,
        y_title=f"Solutions where library was imported (<b>{'%' if percentage else '#'}</b>)",
        order=order,
    )
    return figure
