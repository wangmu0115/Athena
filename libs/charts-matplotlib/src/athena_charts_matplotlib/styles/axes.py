from pydantic import Field

from athena_charts.themes import FontWeight
from athena_charts_matplotlib.styles._base import _BaseStyle
from athena_charts_matplotlib.styles.types import HorizontalAlignment, VerticalAlignment


class MatplotlibAxesStyle(_BaseStyle):
    facecolor: str | None = Field(None, description="背景颜色")
    edgecolor: str | None = Field(None, description="边框颜色")
    edge_linewidth: float | None = Field(None, description="边框粗细")

    titlesize: int | None = Field(None, gt=0, description="标题字号")
    titleweight: FontWeight | None = Field(None, description="标题字体粗细")
    titlecolor: str | None = Field(None, description="标题字体颜色")
    titlelocation: HorizontalAlignment | None = Field(None, description="标题水平对齐方式")

    labelsize: int | None = Field(None, gt=0, description="坐标轴标题字号")
    labelweight: FontWeight | None = Field(None, description="坐标轴标题粗细")
    labelcolor: str | None = Field(None, description="坐标轴标题颜色")
    x_axis_labellocation: HorizontalAlignment | None = Field(None, description="X 轴标题水平对齐方式")
    y_axis_labellocation: VerticalAlignment | None = Field(None, description="Y 轴标题垂直对齐方式")
