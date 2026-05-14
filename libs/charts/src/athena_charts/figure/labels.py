from pydantic import Field

from athena_core.models import BaseAthenaModel


class FigureLabels(BaseAthenaModel):
    title: str = Field("", description="画布标题")
    subtitle: str = Field("", description="画布副标题")
