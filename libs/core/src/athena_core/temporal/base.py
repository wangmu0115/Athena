from typing import Literal

# 日期边界策略：
# - start: 当天开始时间 `time.min`
# - end: 当天结束时间 `time.max`
# - noon: 当天中午时间 `time(hour=12, minute=0, second=0)`
type DateBoundaryPolicy = Literal["start", "end", "noon"]
