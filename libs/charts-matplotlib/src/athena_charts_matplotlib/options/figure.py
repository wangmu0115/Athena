from pydantic import Field

from athena_charts.themes.base import FontWeight
from athena_charts_matplotlib.options.base import BaseOptions


class MatplotlibFigureOptions(BaseOptions):
    width: int | None = Field(None, gt=0, description="画布宽度，单位 px")
    height: int | None = Field(None, gt=0, description="画布高度，单位 px")
    dpi: int | None = Field(None, gt=0, description="分辨率，每英寸点数")
    facecolor: str | None = Field(None, description="画布背景颜色")
    edgecolor: str | None = Field(None, description="画布边框颜色")
    titlesize: int | None = Field(None, gt=0, description="画布标题字号")
    titleweight: FontWeight | None = Field(None, description="画布标题字体粗细")
