from pydantic import Field

from athena_core.models import BaseAthenaModel


class ChartLabels(BaseAthenaModel):
    title: str = Field("", description="图表标题")
    subtitle: str = Field("", description="图表副标题")
