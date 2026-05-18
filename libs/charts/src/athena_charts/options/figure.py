from pydantic import Field

from athena_charts.options.base import BaseOptions


class FigureOptions(BaseOptions):
    width: int | None = Field(None, gt=0, description="画布宽度，单位 px")
    height: int | None = Field(None, gt=0, description="画布高度，单位 px")
