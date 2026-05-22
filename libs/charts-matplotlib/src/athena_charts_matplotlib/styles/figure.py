from pydantic import Field

from athena_charts.themes import FontWeight
from athena_charts_matplotlib.styles._base import _BaseStyle


class MatplotlibFigureStyle(_BaseStyle):
    width: int | None = Field(None, gt=0, description="画布宽度，单位 px")
    height: int | None = Field(None, gt=0, description="画布高度，单位 px")
    dpi: int | None = Field(None, gt=0, description="分辨率，每英寸点数")
    facecolor: str | None = Field(None, description="画布背景颜色")
    edgecolor: str | None = Field(None, description="画布边框颜色")
    frameon: bool | None = Field(None, description="是否绘制边框")
    titlesize: int | None = Field(None, gt=0, description="画布标题字号")
    titleweight: FontWeight | None = Field(None, description="画布标题字体粗细")
    titlecolor: str | None = Field(None, description="画布标题字体颜色")
