from athena_core.models import BaseAthenaModel
from pydantic import Field


class FigureLabels(BaseAthenaModel):
    title: str = Field("", description="画布标题")
    subtitle: str = Field("", description="画布副标题")
