import math

from matplotlib.axes import Axes

from athena_core.values.fallbacks import first_not_none
from athena_core.values.optional import optional_or, safe_getattr
from athena_matplotlib.options.data_label import DataLabelOptions, DataLabelStyle, DataLabelStyleRule
from athena_matplotlib.options.rules.data_context import DataContext
from athena_matplotlib.options.rules.matches import match_data_condition


class DataLabelLayerArtist:
    def draw(
        self,
        axes: Axes,
        x_positions: list[float],
        y_values: list[float | None],
        *,
        semantic_x_values: list[object] | None = None,
        plot_name: str = "",
        z_index: int = 999,
        options: DataLabelOptions | None = None,
        override: DataLabelOptions | None = None,
    ):
        if options is None and override is None:
            return

        semantic_x_values = semantic_x_values or x_positions

        # offset_x, offset_y, ha, va
        annotate_common_params = _resolve_datalabel_common_params(options, override)

        base_style = _resolve_datalabel_base_style(options, override)
        style_rules = [
            *(options.rules if options is not None else []),
            *(override.rules if override is not None else []),
        ]
        count = len(x_positions)
        for index, (x_pos, x_raw, y) in enumerate(zip(x_positions, semantic_x_values, y_values, strict=True)):
            if y is None:
                continue
            if isinstance(y, float) and not math.isfinite(y):
                continue

            data_context = DataContext.of(x=x_raw, y=y, index=index, count=count, name=plot_name)
            style = _resolve_datalabel_style(base_style, style_rules, data_context)
            if not style.visible:
                continue

            formatter = optional_or(style.formatter, default="{y:g}")
            text = formatter.format(x=x_raw, y=y, name=plot_name, index=index)

            text_params = style.model_dump(exclude_none=True, exclude=["visible", "formatter"], by_alias=True)
            text_params.update(annotate_common_params)

            axes.annotate(
                text,
                xy=(x_pos, y),
                zorder=z_index,
                **text_params,
            )


def _resolve_datalabel_base_style(
    options: DataLabelOptions | None,
    override: DataLabelOptions | None,
) -> DataLabelStyle:
    values: dict[str, object | None] = {}

    if options is not None:
        values.update(options.style_model_dump(by_alias=False))
    if override is not None:
        values.update(override.style_model_dump(by_alias=False))

    return DataLabelStyle(**values)


def _resolve_datalabel_style(
    base_style: DataLabelStyle,
    rules: list[DataLabelStyleRule],
    context: DataContext,
) -> DataLabelStyle:
    values = base_style.model_dump(exclude_none=True, by_alias=False)

    for rule in rules:
        if match_data_condition(rule.when, context=context):
            values.update(rule.style.model_dump(exclude_none=True, by_alias=False))

    return DataLabelStyle(**values)


def _resolve_datalabel_common_params(
    options: DataLabelOptions | None,
    override: DataLabelOptions | None,
) -> dict[str, object]:
    return {
        "xytext": (
            first_not_none(
                safe_getattr(options, "offset_x"),
                safe_getattr(override, "offset_x"),
                default=0,
            ),
            first_not_none(
                safe_getattr(options, "offset_y"),
                safe_getattr(override, "offset_y"),
                default=6,
            ),
        ),
        "textcoords": "offset points",
        "ha": first_not_none(
            safe_getattr(options, "ha"),
            safe_getattr(override, "ha"),
            default="center",
        ),
        "va": first_not_none(
            safe_getattr(options, "va"),
            safe_getattr(override, "va"),
            default="bottom",
        ),
    }
