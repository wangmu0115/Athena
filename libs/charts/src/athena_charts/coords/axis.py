from typing import Literal

from pydantic import Field

from athena_core.models import BaseAthenaModel

type AxisScale = Literal["linear", "log"]
type AxisType = Literal["timestamp_ms", "timestamp_s", "datetime", "date", "time", "number", "category"]


class TickFormatter(BaseAthenaModel):
    kind: Literal["auto", "category"]


class Axis(BaseAthenaModel):
    label: str = Field("", description="坐标轴标题")
    type: AxisType
