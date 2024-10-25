import math

import plotly.graph_objects as go
from plotly_utils import default_figure


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


def plot_results(
    data: dict[str, list[int]],
    title: str,
    x_len: int = 5,
    y_log: bool = True,
) -> go.Figure:
    """
    Plot the given result data onto a scatter plot with lines.

    Returns
    -------
    The created figure.
    """
    x_ticks = ["1st", "2nd", "3rd"]
    while len(x_ticks) < x_len:
        x_ticks.append(f"{len(x_ticks) + 1}th")

    lines = []
    for key, value in data.items():
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
            )
        )

    figure = default_figure(
        title=title,
        data=lines,
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
