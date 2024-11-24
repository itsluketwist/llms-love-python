import math

import plotly.express as px
import plotly.graph_objects as go
from plotly_utils import default_figure


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
