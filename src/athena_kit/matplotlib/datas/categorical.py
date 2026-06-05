from dataclasses import dataclass, field
from typing import Literal, Self


@dataclass
class CategoricalDatum:
    """分类数据项，用于表示一组分类数据中的单个数据点，由分类名称 `category` 和值 `value` 组成。

    Attributes:
        category: 分类名称。
        value: 对应的数值，当值不存在或缺失时可为`None`。
    """

    category: str
    value: float | None

    @classmethod
    def datum(cls, *, category: str, value: float | None) -> Self:
        return cls(category=category, value=value)


@dataclass
class CategoricalSeriesData:
    """分类序列数据，用于表示基于分类轴的数据集合。

    Attributes:
        kind: 数据类型标识，固定值 `categorical`。
        datums: 分类数据项列表。
    """

    kind: Literal["categorical"] = "categorical"
    datums: list[CategoricalDatum] = field(default_factory=list)

    def __post_init__(self):
        if not self.datums:
            raise ValueError("CategoricalSeriesData cannot be empty.")

    @classmethod
    def from_tuples(cls, *category_values: tuple[str, float | None]):
        datums: list[CategoricalDatum] = []
        for category, value in category_values:
            datums.append(CategoricalDatum.datum(category=category, value=value))

        return cls(datums=datums)

    @classmethod
    def of(cls, datums: list[CategoricalDatum]):
        return cls(datums=datums)

    @property
    def categories(self) -> list[str]:
        return [datum.category for datum in self.datums]

    @property
    def values(self) -> list[float | None]:
        return [datum.value for datum in self.datums]
