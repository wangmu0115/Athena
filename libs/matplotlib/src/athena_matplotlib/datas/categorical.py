from typing import Literal, Self

from pydantic import Field, model_validator

from athena_charts.specs._base import _BaseSpec


class CategoricalDatum(_BaseSpec):
    """分类数据项"""

    category: str = Field(..., description="分类名称")
    value: float | None = Field(None, description="分类数值")


class CategoricalSeriesData(_BaseSpec):
    kind: Literal["categorical"] = "categorical"
    datums: list[CategoricalDatum] = Field(..., description="分类项列表")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if not self.datums:
            raise ValueError("CategoricalSeriesData cannot be empty.")
        return self

    @property
    def categories(self) -> list[str]:
        return [datum.category for datum in self.datums]

    @property
    def values(self) -> list[float | None]:
        return [datum.value for datum in self.datums]
