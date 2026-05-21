from typing import Literal, Self

from pydantic import Field

from athena_charts.specs._base import _BaseSpec

type DataField = Literal["x", "y", "category", "value", "name", "index", "plot_name"]
"""数据字段定义，用于描述条件表达式或动态样式规则中所引用的数据来源字段。"""


class DataPredicate(_BaseSpec):
    """单个数据条件谓词，用于描述针对某个数据字段的一组比较条件。

    所有比较值都应与目标字段的数据类型兼容，例如：
        - 时间字段可以和日期时间字符串、date、datetime 比较
        - 数值字段可以和 int、float 比较
        - 分类字段通常适合使用 eq/neq 判断
    """

    field: DataField = Field("y", description="判断字段来源")

    gt: object | None = Field(None, description="大于")
    gte: object | None = Field(None, description="大于等于")
    lt: object | None = Field(None, description="小于")
    lte: object | None = Field(None, description="小于等于")
    eq: object | None = Field(None, description="等于")
    neq: object | None = Field(None, description="不等于")


class DataCondition(_BaseSpec):
    """数据条件表达式，支持单条件与复合条件。"""

    all: list[DataPredicate] | None = Field(None, description="所有条件都满足时生效")
    any: list[DataPredicate] | None = Field(None, description="任意条件满足时生效")

    @classmethod
    def when(cls, predicate: DataPredicate) -> Self:
        return cls(all=[predicate])
