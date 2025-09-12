from datetime import date, time, datetime


def parse_str_date(d_str: str, d_format: str = "%Y-%m-%d") -> date:
    """将日期字符串解析为日期对象

    Args:
        d_str: 日期字符串
        d_format: 格式化字符串
            |||

    Returns:
        date: 日期对象 `datetime.date`
    """
    dt = datetime.strptime(d_str, d_format)
    return dt.date()

def parse_str_time(t_str: str, t_format: str = "") -> time:
    pass


def str_datetime(dt_str: str, dt_format: str = "%Y"):
    pass
