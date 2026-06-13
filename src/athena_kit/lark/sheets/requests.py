from typing import Any, Self

from pydantic import BaseModel, Field

from athena_kit.core.tabular import serialize_cell_value


class SheetUpdateRequest(BaseModel):
    addSheet: dict[str, Any] | None = Field(None, description="Add sheet")
    copySheet: dict[str, Any] | None = Field(None, description="Copy sheet")
    deleteSheet: dict[str, Any] | None = Field(None, description="Delete sheet")

    @classmethod
    def add_sheet(cls, title: str, index: int) -> Self:
        return cls(addSheet={"properties": {"title": title, "index": index}})

    @classmethod
    def copy_sheet(cls, source_sheet_id: str, target_sheet_title: str) -> Self:
        return cls(copySheet={"source": {"sheetId": source_sheet_id}, "destination": {"title": target_sheet_title}})

    @classmethod
    def delete_sheet(cls, sheet_id: str) -> Self:
        return cls(deleteSheet={"sheetId": sheet_id})


class SheetsBatchUpdateRequest(BaseModel):
    requests: list[SheetUpdateRequest] = Field(..., description="Sheet batch update requests", min_length=1)


class SheetWritePayload(BaseModel):
    headers: list[str] | None = Field(default=None, description="Optional header values")
    rows_values: list[list[object]] = Field(default_factory=list, description="Rows to write")

    @classmethod
    def from_rows_values(cls, headers: list[str] | None, rows_values: list[list[object]]) -> Self:
        if not rows_values and not headers:
            raise ValueError("Headers and rows cannot be all empty.")

        normalized_rows_values = [[serialize_cell_value(value) for value in row_values] for row_values in rows_values]
        return cls(headers=headers, rows_values=normalized_rows_values)

    def shape(self, include_headers: bool = True) -> tuple[int, int]:
        n_rows = len(self.rows_values)
        if include_headers and self.headers:
            n_rows += 1

        n_header_cols = len(self.headers or [])
        n_row_cols = max((len(row) for row in self.rows_values), default=0)
        n_cols = max(n_header_cols, n_row_cols)
        return n_rows, n_cols

    def to_table_2dvalues(self, include_headers: bool = True) -> list[list[Any]]:
        if include_headers and self.headers:
            return [self.headers, *self.rows_values]
        return self.rows_values


class SheetWriteRequest(BaseModel):
    valueRange: dict[str, Any] = Field(..., description="Range and values to write")

    @classmethod
    def build(cls, range: str, values: list[list[Any]]) -> Self:
        return cls(valueRange={"range": range, "values": values})
