from typing import Self

import matplotlib as mpl
from pydantic import Field

from athena_charts_matplotlib.rendering.options.base import _BaseOptions
from athena_charts_matplotlib.styles import FontWeight


class FigureOptions(_BaseOptions):
    size: tuple[int, int] | None = Field(None, description="画布大小: (width, height)")
    dpi: int | None = Field(None, gt=0, description="分辨率，每英寸点数")

    titlesize: int | None = Field(None, gt=0, description="画布标题字号")
    titleweight: FontWeight | None = Field(None, description="画布标题字体粗细")
    titlecolor: str | None = Field(None, description="画布标题字体颜色")

    def build_create_params(self) -> dict[str, object]:
        if self.size is not None:
            dpi = self.dpi or mpl.rcParams["figure.dpi"]
            figsize = self.size / dpi
            return {"figsize": figsize, "dpi": dpi}
        return {}

    def build_title_params(self) -> dict[str, object]:
        params = {}
        if self.titlesize is not None:
            params["fontsize"] = self.titlesize
        if self.titleweight:
            params["fontweight"] = self.titleweight
        if self.titlecolor:
            params["color"] = self.titlecolor
        return params

    @classmethod
    def of(
        cls,
        size: tuple[int, int] | None = None,
        dpi: int | None = None,
        titlesize: int | None = None,
        titleweight: FontWeight | None = None,
        titlecolor: str | None = "#111111",
    ) -> Self:
        return cls(
            size=size,
            dpi=dpi,
            titlesize=titlesize,
            titleweight=titleweight,
            titlecolor=titlecolor,
        )
