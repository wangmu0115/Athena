from dataclasses import asdict, dataclass
from typing import Literal, Self

type DataField = Literal["x", "y", "category", "value", "name", "plotname", "index", "first", "last"]
"""数据字段定义，用于描述条件表达式或动态样式规则中所引用的数据来源字段。"""


@dataclass
class DataContext:
    x: object
    y: float | None
    category: object
    value: float | None
    name: str
    plotname: str
    index: int
    first: bool
    last: bool

    @classmethod
    def of(
        cls,
        *,
        x: object,
        y: float | None,
        index: int,
        count: int,
        name: str | None = "",
    ) -> Self:
        return cls(
            x=x,
            y=y,
            category=x,
            value=y,
            name=name,
            plotname=name,
            index=index,
            first=index == 0,
            last=index == count - 1,
        )

    def get(self, field: DataField) -> object | None:
        return asdict(self)[field]
