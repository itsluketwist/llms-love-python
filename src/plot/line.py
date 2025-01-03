import math
from datetime import datetime

import plotly.graph_objects as go
from plotly_utils import default_figure

from src.constants import DATETIME_FORMAT
from src.output import read_json
from src.plot.utils import DEFAULT_COLOURS, LIBRARY_COLOURS


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
                marker_color=DEFAULT_COLOURS[idx],
                line_color=DEFAULT_COLOURS[idx],
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


def plot_line_library_stars(
    libraries: list[str],
    title: str | None = None,
    x_title: str = "Years since repository creation",
    y_title: str = "Total GitHub stars",
    data_path: str = "data/library/library_stats.json",
    width: int = 700,
) -> go.Figure:
    """
    Plot the given result data onto a scatter plot with lines.

    Returns
    -------
    The created figure.
    """
    raw = read_json(file_path=data_path)
    if not isinstance(raw, dict):
        raise TypeError("Results file must contain a json dictionary.")

    queried = datetime.strptime(raw["queried"], DATETIME_FORMAT)
    title = (
        title or "GitHub repository stars growth"
    )  # + " vs ".join([f"<b>{lib}</b>" for lib in libraries])

    figure = default_figure(
        title=title,
        x_title=x_title,
        y_title=y_title,
    )

    for i, library in enumerate(libraries):
        library_data = raw["data"][library]
        created = datetime.strptime(library_data["created"], DATETIME_FORMAT)
        age = (queried - created).days / 365

        figure.add_trace(
            go.Scatter(
                x=[0, age],
                y=[0, library_data["stars"]],
                name=library,
                mode="lines+markers",
                marker_color=LIBRARY_COLOURS[i],
                line_color=LIBRARY_COLOURS[i],
                line_width=5,
                marker_size=8,
            )
        )
        figure.add_annotation(
            x=age,
            y=library_data["stars"],
            text=f"<b>{library}</b>",
            showarrow=False,
            xshift=-5,
            xanchor="right",
            yshift=5,
            yanchor="bottom",
        )

    figure.update_layout(
        width=width,
        showlegend=False,
        margin=dict(b=200, t=160),
    )

    return figure
