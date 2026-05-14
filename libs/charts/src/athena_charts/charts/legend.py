from typing import Literal

from pydantic import Field

from athena_core.models import BaseAthenaModel


class ChartLegend(BaseAthenaModel):
    visible: bool = Field(True, description="是否显示图例")
    title: str = Field("", description="图例标题")
    position: Literal[
        "best",
        "top",
        "bottom",
        "left",
        "right",
        "top_left",
        "top_right",
        "bottom_left",
        "bottom_right",
    ] = Field("best", description="图例位置")
