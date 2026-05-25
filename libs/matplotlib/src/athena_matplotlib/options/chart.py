from typing import Self

from pydantic import Field

from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.types import FontWeight, HorizontalAlignment


class ChartOptions(_BaseOptions):
    facecolor: str | None = Field(None, description="背景颜色")
    titlesize: int | None = Field(None, gt=0, description="标题字号", alias="fontsize")
    titleweight: FontWeight | None = Field(None, description="标题字体粗细", alias="fontweight")
    titlecolor: str | None = Field(None, description="标题字体颜色", alias="color")
    location: HorizontalAlignment | None = Field(None, description="标题位置", alias="loc")

    def build_title_params(self) -> dict[str, object]:
        return self.model_dump(
            exclude_none=True,
            by_alias=True,
            exclude=["facecolor"],
        )

    @classmethod
    def of(
        cls,
        facecolor: str | None = None,
        titlesize: int | None = None,
        titleweight: FontWeight | None = None,
        titlecolor: str | None = None,
        location: HorizontalAlignment | None = None,
    ) -> Self:
        return cls(
            facecolor=facecolor,
            titlesize=titlesize,
            titleweight=titleweight,
            titlecolor=titlecolor,
            location=location,
        )
