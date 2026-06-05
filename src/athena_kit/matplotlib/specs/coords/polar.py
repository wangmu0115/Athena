from typing import Literal

from pydantic import Field

from athena_kit.matplotlib.specs.coords.base import AxisSpec, Coord


class PolarAxisSpec(AxisSpec):
    pass
    # role: PolarAxisRole = Field(..., description="极坐标轴角色")

    # @classmethod
    # def theta(
    #     cls,
    #     *,
    #     label: str = "",
    #     data_type: AxisDataType = "category",
    # ) -> Self:
    #     return cls(
    #         role="theta",
    #         label=label,
    #         data_type=data_type,
    #     )

    # @classmethod
    # def radius(cls, *, label: str = "") -> Self:
    #     return cls(
    #         role="radius",
    #         label=label,
    #         data_type="number",
    #     )

    # @model_validator(mode="after")
    # def validate(self) -> Self:
    #     if self.role == "radius" and self.data_type != "number":
    #         raise ValueError("Polar radius axis must use number data type.")
    #     return self


class PolarCoord(Coord):
    """极坐标系规范，用于描述极坐标图表中的角度轴与半径轴。

    注意：
        - 饼图和环形图通常不需要显式配置 `angle_axis` 和 `radius_axis`，因为其角度和半径通常由 plot 数据与图形配置决定。
        - 雷达图、极坐标柱状图等更依赖显式轴配置。
    """

    kind: Literal["polar"] = Field("polar", description="极坐标系")
    # angle_axis: PolarAxisSpec | None = Field(None, description="角度轴")
    # radius_axis: PolarAxisSpec | None = Field(None, description="半径轴")

    # @classmethod
    # def pie(cls) -> Self:
    #     return cls(angle_axis=None, radius_axis=None)

    # @model_validator(mode="after")
    # def validate(self) -> Self:
    #     if self.angle_axis is not None and self.angle_axis.role != "theta":
    #         raise ValueError("Polar angle_axis must use theta role.")
    #     if self.radius_axis is not None and self.radius_axis.role != "radius":
    #         raise ValueError("Polar radius_axis must use radius role.")
    #     return self
