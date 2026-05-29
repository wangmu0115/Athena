from typing import Self

from pydantic import Field, field_serializer

from athena_matplotlib.adapters import to_mpl_legend_loc
from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.types import LegendLocation


class LegendOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示图例")

    location: LegendLocation = Field("auto", description="图例位置", alias="loc")
    ncols: int = Field(1, gt=0, description="图例列数")
    bbox_to_anchor: tuple[float, float] | None = Field(None, description="图例锚点坐标")

    @field_serializer("location")
    def serialize_location(self, value: LegendLocation) -> str:
        return to_mpl_legend_loc(value)

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        location: LegendLocation = "auto",
        ncols: int = 1,
        bbox_to_anchor: tuple[float, float] | None = None,
    ) -> Self:
        return cls(
            visible=True,
            location=location,
            ncols=ncols,
            bbox_to_anchor=bbox_to_anchor,
        )
