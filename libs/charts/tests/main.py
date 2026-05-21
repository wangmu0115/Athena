def _format_number(
    value: object,
    *,
    precision: int | None = None,
    thousands_separator: bool = False,
    scale: float = 1.0,
) -> str:
    number = float(value) * scale
    if precision is None:
        return f"{number:g}"
    return f"{number:{',' if thousands_separator else ''}.{precision}f}"


print(_format_number(1894456.32, precision=0, thousands_separator=True))
