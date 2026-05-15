from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.charts.chart import ChartSpec
    from athena_charts.charts.labels import ChartLabels
    from athena_charts.charts.legend import ChartLegend
    from athena_charts.charts.options import ChartOptions


__all__ = (
    "ChartSpec",
    "ChartLabels",
    "ChartLegend",
    "ChartOptions",
)


_dynamic_imports = {
    "ChartSpec": "chart",
    "ChartLabels": "labels",
    "ChartLegend": "legend",
    "ChartOptions": "options",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
