from pydantic import Field

from athena_core.models import BaseAthenaModel


class ChartOptions(BaseAthenaModel):
    clip: bool = Field(True, description="绘图元素是否裁剪到坐标区域内")
