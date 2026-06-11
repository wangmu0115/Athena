from typing import Any, Self

from pydantic import BaseModel, ConfigDict

from athena_kit.core.tabular.serialization import deserialize_cell_value, serialize_cell_value


class TableRow(BaseModel):
    """可与二维表格行互相转换的 Pydantic 模型基类"""

    model_config = ConfigDict(
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    @classmethod
    def table_headers(cls) -> list[str]:
        """按列顺序返回写入表格时使用的标题行"""

        return [cls._field_header(field_name) for field_name in cls._ordered_field_names()]

    def to_table_row(self) -> list[Any]:
        """将当前模型实例序列化为一行表格单元格值。"""
        cls = self.__class__
        return [
            serialize_cell_value(
                getattr(self, field_name),
                cls.model_fields[field_name].annotation,
            )
            for field_name in cls._ordered_field_names()
        ]

    @classmethod
    def from_table_row(cls, headers: list[str], row_values: list[Any]) -> Self:
        """根据标题行和一行单元格值反序列化为模型实例。"""
        header_map = cls._header_to_field_name()
        return cls._from_table_row(headers, row_values, header_map)

    @classmethod
    def from_table_rows(cls, headers: list[str], rows_values: list[list[Any]]) -> list[Self]:
        """根据标题行和多行单元格值反序列化为模型实例列表。"""
        header_map = cls._header_to_field_name()
        return [cls._from_table_row(headers, row_values, header_map) for row_values in rows_values]

    @classmethod
    def _from_table_row(cls, headers: list[str], row_values: list[Any], header_map: dict[str, str]) -> Self:
        payload = {}
        for index, header in enumerate(headers):
            field_name = header_map.get(header)
            if not field_name:
                continue
            raw_value = row_values[index] if index < len(row_values) else None
            payload[field_name] = deserialize_cell_value(
                raw_value,
                cls.model_fields[field_name].annotation,
            )

        return cls.model_validate(payload)

    @classmethod
    def _ordered_field_names(cls) -> list[str]:
        return sorted(
            cls.model_fields.keys(),
            key=lambda name: (
                (cls.model_fields[name].json_schema_extra or {}).get("order", 0),
                name,
            ),
        )

    @classmethod
    def _field_header(cls, field_name: str) -> str:
        field = cls.model_fields[field_name]
        extra = field.json_schema_extra or {}
        return extra.get("title") or field.alias or field_name

    @classmethod
    def _header_to_field_name(cls) -> dict[str, str]:
        mapping = {}

        for field_name, field in cls.model_fields.items():
            extra = field.json_schema_extra or {}
            title = extra.get("title")
            if title:
                mapping[title] = field_name
            if field.alias:
                mapping[field.alias] = field_name
            mapping[field_name] = field_name

        return mapping
