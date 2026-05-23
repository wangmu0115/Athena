from pydantic import BaseModel, ConfigDict


class _BaseOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # 禁止未知字段
        arbitrary_types_allowed=True,  # 允许自定义对象
        validate_assignment=True,  # 修改字段重新校验
        str_strip_whitespace=True,  # 自动 trim
    )


class ColorCycle:
    def __init__(self, colors: list[str] | None = None):
        self._colors = colors or []
        self._n_colors = len(colors) if colors else 0
        self._index = 0

    def next(self) -> str | None:
        color = self.pick(self._index)
        if color is not None:
            self._index += 1
        return color

    def pick(self, index: int = 0) -> str | None:
        if self._n_colors == 0:
            return None
        color = self._colors[index % self._n_colors]
        return color
