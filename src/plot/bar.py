from collections import defaultdict
from typing import DefaultDict

import plotly.graph_objects as go
from plotly_utils import default_figure

from src.output import read_json
from src.plot.utils import (
    IGNORE_FILETYPES,
    LANGUAGE_COLOURS,
    LIBRARY_COLOURS,
    SCRIPTING_LANGUAGES,
    format_model,
)


def plot_bar_results(
    categories: tuple[list[str], list[str]],
    values: list[int | float],
    colors: list[str],
    title: str | None,
    x_title: str | None = None,
    y_title: str | None = None,
    width: int | None = None,
    annotation: str | None = None,
) -> go.Figure:
    """
    Plot the given result data onto a scatter plot with lines.

    Returns
    -------
    The created figure.
    """
    figure = default_figure(
        title=title,
        data=go.Bar(
            x=categories,
            y=values,
            text=[round(v, 1) for v in values],
            marker_color=colors,
            textposition="outside",
        ),
        x_title=x_title,
        y_title=y_title,
    )
    figure.update_layout(
        bargap=0.1,
        margin=dict(b=200, t=160),
        showlegend=False,
        xaxis_tickfont_size=14,
        yaxis_tickfont_size=14,
    )

    if width:
        figure.update_layout(width=width)

    if annotation:
        figure.add_annotation(
            text=f"<i><b>{annotation}</b></i>",
            xref="paper",
            yref="paper",
            x=0.995,
            y=0.995,
            showarrow=False,
        )

    return figure


def plot_bar_languages(
    results: str,
    percentage: bool = True,
    title: str | None = None,
    domain: str | None = None,
    width: int | None = None,
    ignore_bash: bool = True,
    temperature: bool = False,
) -> go.Figure:
    raw = read_json(file_path=results)
    if not isinstance(raw, dict):
        raise TypeError("Results file must contain a json dictionary.")

    if title or domain:
        title = title or f"Languages used for <b>{domain}</b>"

    ignore = IGNORE_FILETYPES
    if ignore_bash:
        ignore += SCRIPTING_LANGUAGES

    plot_mod = []
    plot_lang = []
    plot_val = []
    total = raw["metadata"]["total"]
    for model, _data in raw["results"].items():
        counts: dict[str, int | float] = _data["counts"]
        if percentage:
            counts = {k: v * 100 / total for k, v in counts.items()}
            counts = {k: int(v) if v > 10 else v for k, v in counts.items()}
        pairs = [(k, v) for k, v in counts.items() if k not in ignore]
        pairs.sort(key=lambda x: x[1], reverse=True)

        for language, count in pairs:
            plot_lang.append(language)
            plot_mod.append(format_model(model=model))
            plot_val.append(count)

    if temperature:
        model = raw["metadata"]["model"]
        annotation = f"model: {model}"
    else:
        annotation = None

    figure = plot_bar_results(
        categories=(plot_mod, plot_lang),
        values=plot_val,
        colors=[LANGUAGE_COLOURS.get(lang, "LightSlateGray") for lang in plot_lang],
        title=title,
        x_title=f"Languages used per <b>{'temperature' if temperature else 'model'}</b>",
        y_title=f"<b>{'%' if percentage else '#'}</b> responses with language used",
        width=width,
        annotation=annotation,
    )

    return figure


def plot_bar_libraries(
    results: str,
    libraries: list[str],
    percentage: bool = True,
    extra_libraries: list[str] | None = None,
    width: int = 1200,
    title: str | None = None,
    temperature: bool = False,
) -> go.Figure:
    raw = read_json(file_path=results)
    if not isinstance(raw, dict):
        raise TypeError("Results file must contain a json dictionary.")

    if title is None:
        library_string = " vs ".join(
            [
                f"<b style='color:{col};'>{lib}</b>"
                for lib, col in zip(libraries, LIBRARY_COLOURS)
            ]
        )
        title = f"Library usage of {library_string} across models"

    plot_mod = []
    plot_lib = []
    plot_val = []
    plot_clr = []
    extra_libraries = extra_libraries or []
    total = raw["metadata"]["total"]
    for model, _data in raw["results"].items():
        counts: DefaultDict[str, int] = defaultdict(int)
        for _, problem_data in _data.items():
            for import_str, count in problem_data["counts"].items():
                import_list = import_str.split(",")
                for _import in import_list:
                    if _import in libraries or _import == "none":
                        counts[_import] += count

                if [i for i in import_list if i != "none" and i not in libraries]:
                    counts["other"] += 1

        if percentage:
            _counts = {k: v * 100 / total for k, v in counts.items()}
            _counts = {k: int(v) if v > 10 else v for k, v in _counts.items()}
        else:
            _counts = dict(counts)

        for i, library in enumerate(libraries):
            plot_lib.append(library)
            plot_mod.append(format_model(model=model))
            plot_val.append(_counts.get(library, 0))
            plot_clr.append(LIBRARY_COLOURS[i])

        for extra in ["other", "none"]:
            if extra in _counts:
                plot_lib.append(extra)
                plot_mod.append(format_model(model=model))
                plot_val.append(_counts.get(extra, 0))
                plot_clr.append("DarkSlateBlue")

    if temperature:
        model = raw["metadata"]["model"]
        annotation = f"model: {model}"
    else:
        annotation = None

    figure = plot_bar_results(
        categories=(plot_mod, plot_lib),
        values=plot_val,
        colors=plot_clr,
        title=title,
        x_title=f"Libraries imported per <b>{'temperature' if temperature else 'model'}</b>",
        y_title=f"<b>{'%' if percentage else '#'}</b> responses with library imported",
        width=width,
        annotation=annotation,
    )

    return figure
