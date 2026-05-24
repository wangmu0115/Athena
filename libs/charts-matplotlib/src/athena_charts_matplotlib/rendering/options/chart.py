from typing import Self

from pydantic import Field

from athena_charts_matplotlib.adapters import to_mpl_line_style
from athena_charts_matplotlib.rendering.options.base import _BaseOptions
from athena_charts_matplotlib.rendering.options.coord import AxesOptions, GridOptions
from athena_charts_matplotlib.rendering.options.types import HorizontalAlignment
from athena_charts_matplotlib.styles import FontWeight


class ChartTitleOptions(_BaseOptions):
    titlesize: int | None = Field(None, gt=0, description="标题字号", alias="fontsize")
    titleweight: FontWeight | None = Field(None, description="标题字体粗细", alias="fontweight")
    titlecolor: str | None = Field(None, description="标题字体颜色", alias="color")
    location: HorizontalAlignment | None = Field(None, description="标题位置", alias="loc")

    @classmethod
    def of(
        cls,
        titlesize: int | None = None,
        titleweight: FontWeight | None = None,
        titlecolor: str | None = None,
        location: HorizontalAlignment | None = None,
    ) -> Self:
        return cls(
            titlesize=titlesize,
            titleweight=titleweight,
            titlecolor=titlecolor,
            location=location,
        )


class ChartOptions(_BaseOptions):
    facecolor: str | None = Field(None, description="背景颜色")
    title: ChartTitleOptions | None = Field(None, description="图表标题配置项")

    grid: GridOptions | None = Field(None, description="坐标系-网格配置项")
    axes: AxesOptions | None = Field(None, description="坐标系-坐标轴")

    # axis_line_visible: AxisLineVisible | None = Field(None, description="坐标轴线显示配置")

    def build_title_params(self) -> dict[str, object]:
        if self.title is None:
            return {}
        return self.title.model_dump(exclude_none=True, by_alias=True)

    def build_grid_params(self) -> dict[str, object]:
        if self.grid is None:
            return {}
        params = self.grid.model_dump(exclude_none=True, by_alias=True, exclude=["linestyle"])
        if self.grid.linestyle:
            params["linestyle"] = to_mpl_line_style(self.grid.linestyle)
        return params
