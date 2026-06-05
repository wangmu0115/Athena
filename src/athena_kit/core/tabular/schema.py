from typing import Any, Self

from athena_kit.core.models import BaseAthenaModel
from athena_kit.core.tabular.codec import decode_cell_value, encode_field_value


class BaseTableRow(BaseAthenaModel):
    """Typed row schema for tabular persistence."""

    @classmethod
    def headers(cls) -> list[str]:
        headers = []

        for field_name in cls._ordered_field_names():
            field = cls.model_fields[field_name]
            extra = field.json_schema_extra or {}
            headers.append(extra.get("title") or field_name)

        return headers

    def to_row_values(self) -> list[Any]:
        cls = self.__class__
        return [
            encode_field_value(
                getattr(self, field_name),
                cls.model_fields[field_name].annotation,
            )
            for field_name in cls._ordered_field_names()
        ]

    @classmethod
    def from_row_values(cls, headers: list[str], row_values: list[Any]) -> Self:
        title_map = cls._title_to_field_name()

        payload = {}
        for index, header in enumerate(headers):
            field_name = title_map.get(header)
            if not field_name:
                continue
            raw_value = row_values[index] if index < len(row_values) else None
            payload[field_name] = decode_cell_value(
                raw_value,
                cls.model_fields[field_name].annotation,
            )

        return cls.model_validate(payload)

    @classmethod
    def from_rows_values(cls, headers: list[str], rows_values: list[list[Any]]) -> list[Self]:
        return [cls.from_row_values(headers, row_values) for row_values in rows_values]

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
    def _title_to_field_name(cls) -> dict[str, str]:
        mapping = {}

        for field_name, field in cls.model_fields.items():
            extra = field.json_schema_extra or {}
            mapping[extra.get("title") or field_name] = field_name

        return mapping
