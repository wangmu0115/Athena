from pydantic import Field

from athena_core.models.base import BaseAthenaModel


class AxisTheme(BaseAthenaModel):
    edge_color: str = Field("#333333", description="轴线默认颜色")
    label_font_size: int = Field(10, gt=0, description="标签字号")
    label_color: str = Field("#111111", description="标签文本颜色")
    tick_font_size: int = Field(8, gt=0, description="刻度标签字号")
    tick_color: str = Field("#333333", description="刻度线默认颜色")
