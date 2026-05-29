from dataclasses import dataclass, field
from typing import Literal, Self


@dataclass
class XYPoint:
    """二维坐标点，用于表示笛卡尔坐标系中的一个数据点，由 X 轴值和 Y 轴值组成。

    Attributes:
        x: 原始 X 轴数据，类型取决于坐标轴类型，包括数值、字符串分类、日期或日期时间等。
        y: 对应的 Y 轴数值，为 `None` 时，表示该数据点缺失，渲染时通常会被跳过或产生断点。
    """

    x: object
    y: float | None

    @classmethod
    def point(cls, *, x: object, y: float | None):
        return cls(x=x, y=y)


@dataclass
class XYSeriesData:
    """二维序列数据，用于表示一组按照顺序排列的二维坐标数据。

    `x` 和 `y` 按位置一一对应，第 `i` 个二维坐标点由 `(x[i], y[i])` 构成。

    Attributes:
        kind: 数据类型标识，固定值 `xy`
        x: 类型取决于坐标轴的数据类型。
        y: 数值型数据，当 `y[i]` 为 `None` 时，表示该位置的数据缺失，渲染时通常会被跳过或形成断点。
    """

    kind: Literal["xy"] = "xy"
    x: list[object] = field(default_factory=list)
    y: list[float | None] = field(default_factory=list)

    def __post_init__(self):
        if not self.x or not self.y:
            raise ValueError("XYSeriesData cannot be empty.")
        if len(self.x) != len(self.y):
            raise ValueError("XYSeriesData.x and XYSeriesData.y must have the same length.")

    @classmethod
    def from_points(cls, points: list[XYPoint]) -> Self:
        xs = []
        ys = []
        for point in points or []:
            xs.append(point.x)
            ys.append(point.y)
        return cls(x=xs, y=ys)

    @classmethod
    def broadcast_y(cls, *, xs: list[object], y: float | None) -> Self:
        return cls.of(x=xs, y=[y] * len(xs))

    @classmethod
    def broadcast_x(cls, *, x: object, ys: list[float | None]) -> Self:
        return cls.of(xs=[x] * len(ys), ys=ys)

    @classmethod
    def of(cls, *, xs: list[object], ys: list[float | None]) -> Self:
        return cls(x=xs, y=ys)
