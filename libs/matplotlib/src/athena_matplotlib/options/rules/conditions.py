from dataclasses import dataclass
from typing import Self

from athena_matplotlib.options.rules.data_context import DataField


@dataclass(slots=True)
class DataPredicate:
    """单个数据条件谓词，用于描述针对某个数据字段的一组比较条件。

    所有比较值都应与目标字段的数据类型兼容，例如：
        - 时间字段可以和日期时间字符串、date、datetime 比较
        - 数值字段可以和 int、float 比较
        - 分类字段通常适合使用 eq/neq 判断
    """

    field_: DataField = "y"
    gt_: object | None = None
    gte_: object | None = None
    lt_: object | None = None
    lte_: object | None = None
    eq_: object | None = None
    neq_: object | None = None

    @classmethod
    def field(cls, f: DataField) -> Self:
        return cls(field_=f)

    def gt(self, v: object) -> Self:
        self.gt_ = v
        return self

    def gte(self, v: object) -> Self:
        self.gte_ = v
        return self

    def lt(self, v: object) -> Self:
        self.lt_ = v
        return self

    def lte(self, v: object) -> Self:
        self.lte_ = v
        return self

    def eq(self, v: object) -> Self:
        self.eq_ = v
        return self

    def neq(self, v: object) -> Self:
        self.neq_ = v
        return self


@dataclass(slots=True)
class DataCondition:
    """数据条件表达式，支持单条件与复合条件。"""

    all_: list[DataPredicate] | None = None
    """所有条件都满足时生效"""
    any_: list[DataPredicate] | None = None
    """任意条件满足时生效"""

    @classmethod
    def when(cls, predicate: DataPredicate) -> Self:
        return cls(all_=[predicate])

    @classmethod
    def any(cls, *pds: DataPredicate) -> Self:
        return cls(any_=list(pds))

    @classmethod
    def all(cls, *pds: DataPredicate) -> Self:
        return cls(all_=list(pds))
