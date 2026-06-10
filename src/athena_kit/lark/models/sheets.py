from typing import Any, Self

from pydantic import BaseModel, Field


class CreateSpreadsheetRequest(BaseModel):
    folder_token: str = Field(..., description="Lark folder token", min_length=1)
    title: str = Field(..., description="Spreadsheet title", min_length=1)


class SheetUpdateRequest(BaseModel):
    addSheet: dict[str, Any] | None = Field(None, description="Add sheet request")
    copySheet: dict[str, Any] | None = Field(None, description="Copy sheet request")
    deleteSheet: dict[str, Any] | None = Field(None, description="Delete sheet request")

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


class SheetWriteRequest(BaseModel):
    valueRange: dict[str, Any] = Field(..., description="Range and values to write")

    @classmethod
    def build(cls, range: str, values: list[list[Any]]) -> Self:
        return cls(valueRange={"range": range, "values": values})
