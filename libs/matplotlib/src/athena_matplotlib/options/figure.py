from typing import Self

from pydantic import Field

from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.types import FontWeight


class FigureOptions(_BaseOptions):
    titlesize: int | None = Field(None, gt=0, description="画布标题字号", alias="fontsize")
    titleweight: FontWeight | None = Field(None, description="画布标题字体粗细", alias="fontweight")
    titlecolor: str | None = Field(None, description="画布标题字体颜色", alias="color")

    def build_title_params(self) -> dict[str, object]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def of(
        cls,
        titlesize: int | None = None,
        titleweight: FontWeight | None = None,
        titlecolor: str | None = None,
    ) -> Self:
        return cls(
            titlesize=titlesize,
            titleweight=titleweight,
            titlecolor=titlecolor,
        )
