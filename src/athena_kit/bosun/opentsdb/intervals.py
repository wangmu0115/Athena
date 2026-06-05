import re


def calc_interval_seconds(interval: str) -> float:
    """计算 OpenTSDB 时间间隔字符串对应的秒数。

    支持由多个 `数字 + 单位` 片段连续组成的 interval，例如 `1m`、`1d12h30m`、`1s500ms`。
    年份和月份使用固定近似值计算：`y` 按 365 天计算，`n` 按 30 天计算，`ms` 会转换为小数秒。

    输入格式非法时抛出 `ValueError`。
    """
    # Time unit: y=years, n=months, w=weeks, d=days, h=hours, m=minutes, s=seconds, ms=milliseconds
    if not re.fullmatch(r"(\d+(?:ms|[smhdwny]))+", interval):
        raise ValueError(f"Illegal interval format: `{interval}`.")

    duration_and_units = [du for du in re.split(r"(ms|y|n|w|d|h|m|s)", interval) if du != ""]
    if len(duration_and_units) % 2 != 0:
        raise ValueError(f"Illegal interval format: `{interval}`, duration and unit must appear in pairs.")

    seconds = 0
    for index, duration_str in enumerate(duration_and_units):
        if index % 2 == 0:
            duration = int(duration_str)
            unit = duration_and_units[index + 1]
            match unit:
                case "y":
                    base = 365 * 24 * 3600
                case "n":
                    base = 30 * 24 * 3600
                case "w":
                    base = 7 * 24 * 3600
                case "d":
                    base = 1 * 24 * 3600
                case "h":
                    base = 1 * 3600
                case "m":
                    base = 60
                case "s":
                    base = 1
                case "ms":
                    base = 0.001
                case _:
                    raise NotImplementedError(f"Unsupported time unit: {unit}.")
            seconds += duration * base
    return seconds
