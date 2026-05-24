from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from athena_charts.specs.coords import AxisSpec
from athena_charts.specs.coords.cartesian import CartesianCoord
from athena_charts.specs.plots.bar import BarPlot
from athena_charts.specs.plots.line import LinePlot
from athena_charts.specs.plots.unions import PlotSpec
from athena_charts.transforms.normalize import NormalizedXYSeries, normalize_axis_value, normalize_barplot_data, normalize_lineplot_data
from athena_core.temporal.codec import TemporalCodec


@dataclass
class AlignedXYSeries:
    x_values: list[Any]
    y_values_list: list[list[Any]]


def align_cartesian_plots_data(
    plots: list[PlotSpec],
    coord: CartesianCoord,
    *,
    missing_value: float | None = 0.0,
    category_order: list[object] | None = None,
    temporal_codec: TemporalCodec | None = None,
    skil_invalid: bool = True,
) -> AlignedXYSeries:
    normalized_xy_series: list[NormalizedXYSeries] = []
    for plot in plots:
        match plot:
            case LinePlot():
                normalized = normalize_lineplot_data(plot, coord, temporal_codec=temporal_codec, skip_invalid=skil_invalid)
            case BarPlot():
                normalized = normalize_barplot_data(plot, coord, temporal_codec=temporal_codec, skip_invalid=skil_invalid)
            case _:
                raise ValueError(f"Unsupported cartesian coord plot: {type(plot).__name__}.")
        normalized_xy_series.append(normalized)
    categories = resolve_x_categories(
        collect_x_categories(normalized_xy_series),
        x_axis=coord.get_x_axis(plots[0].x_axis_side),
        category_order=category_order,
        missing_value=missing_value,
    )
    return align_series_to_categories(normalized_xy_series, categories, missing_value=missing_value)


def align_series_to_categories(
    series: Iterable[NormalizedXYSeries],
    categories: list[Any],
    *,
    missing_value: float | None = 0.0,
) -> AlignedXYSeries:
    y_values_list: list[list[Any]] = []
    for item in series:
        by_category = dict(zip(item.x_values, item.y_values, strict=True))
        y_values_list.append([by_category.get(category, missing_value) for category in categories])

    return AlignedXYSeries(
        x_values=categories,
        y_values_list=y_values_list,
    )


def resolve_x_categories(
    categories: list[Any],
    *,
    x_axis: AxisSpec,
    category_order: list[object] | None = None,
    temporal_codec: TemporalCodec | None = None,
) -> list[Any]:
    if not categories:
        return []

    if category_order:
        ordered: list[Any] = []

        seen: set[Any] = set()
        category_set = set(categories)
        for raw_category in category_order:
            try:
                category = normalize_axis_value(raw_category, x_axis.data_type, temporal_codec=temporal_codec)
                if category in category_set and category not in seen:
                    seen.add(category)
                    ordered.append(category)
            except (TypeError, ValueError):
                continue

        return ordered + _sort_x_categories([c for c in category_set if c not in seen], x_axis=x_axis)

    return _sort_x_categories(categories, x_axis=x_axis)


def collect_x_categories(series: Iterable[NormalizedXYSeries]) -> list[Any]:
    categories: list[Any] = []
    seen: set[Any] = set()

    for item in series:
        for x_value in item.x_values:
            if x_value not in seen:
                seen.add(x_value)
                categories.append(x_value)

    return categories


def _sort_x_categories(categories: list[Any], *, x_axis: AxisSpec) -> list[Any]:
    if x_axis.data_type in {"timestamp_ms", "timestamp_s", "datetime", "date", "time", "number"}:
        return sorted(categories)

    return categories
