from typing import Literal

# 日期边界策略：
# - start: 当天开始时间 `time.min`
# - end: 当天结束时间 `time.max`
# - noon: 当天中午时间 `time(hour=12, minute=0, second=0)`
type DateBoundaryPolicy = Literal["start", "end", "noon"]

# 时间输出格式：
# - native: 返回 `datetime.time` 原生对象
# - iso: 返回 `time.isoformat()` 生成的 ISO 格式字符串
# - formatted: 返回按 `format_pattern` 格式化后的字符串
type TimeOutputFormat = Literal["native", "iso", "formatted"]
