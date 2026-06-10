from typing import Any, Self

from pydantic import BaseModel, Field, model_validator

from athena_kit.core.tabular import encode_field_value


class SheetWritePayload(BaseModel):
    headers: list[str] | None = Field(default=None, description="Optional header values")
    rows_values: list[list[Any]] = Field(..., description="Rows to write", min_length=1)

    @classmethod
    def from_rows_values(cls, headers: list[str] | None, rows_values: list[list[Any]]) -> Self:
        if not rows_values:
            raise ValueError("Rows cannot be empty.")

        normalized_rows_values = [[encode_field_value(value) for value in row_values] for row_values in rows_values]
        return cls(headers=headers, rows_values=normalized_rows_values)

    @model_validator(mode="after")
    def validate_rows(self):
        if not self.headers:
            return self

        expected_n_columns = len(self.headers)
        for idx, row in enumerate(self.rows_values, start=1):
            if len(row) > expected_n_columns:
                raise ValueError(
                    f"Row {idx} has {len(row)} columns, but expected {expected_n_columns} based on headers."
                )
        return self

    def shape(self, include_headers: bool = True) -> tuple[int, int]:
        n_rows = len(self.rows_values)
        if include_headers and self.headers:
            n_rows += 1

        n_cols = len(self.headers) if self.headers else max(len(row) for row in self.rows_values)
        return n_rows, n_cols

    def to_table_2dvalues(self, include_headers: bool = True) -> list[list[Any]]:
        if include_headers and self.headers:
            return [self.headers, *self.rows_values]
        return self.rows_values
