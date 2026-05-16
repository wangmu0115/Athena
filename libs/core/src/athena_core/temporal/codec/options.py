from pydantic import Field

from athena_core.models.base import BaseAthenaModel
from athena_core.temporal.codec.types import DateBoundaryPolicy, NaiveDateTimePolicy


class DatetimeCodecOptions(BaseAthenaModel):
    naive_policy: NaiveDateTimePolicy = Field("assume_local", description="无时区 datetime 的处理方式")
    date_boundary_policy: DateBoundaryPolicy = Field("start", description="date 转换为 datetime 时，映射到一天的时间点")
