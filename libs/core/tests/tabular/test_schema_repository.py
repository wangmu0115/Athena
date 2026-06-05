import asyncio
from dataclasses import dataclass
from datetime import date
from typing import Any

from athena_core.tabular import BaseTableRow, TableField, TableRepository


class UserRow(BaseTableRow):
    name: str = TableField(title="姓名", order=1)
    birthday: date = TableField(title="生日", order=2)
    tags: list[str] = TableField(title="标签", order=3, default_factory=list)


def test_table_row_headers_and_round_trip():
    row = UserRow(name=" Ada ", birthday=date(2026, 5, 19), tags=["core", " tabular "])

    assert UserRow.headers() == ["姓名", "生日", "标签"]
    assert row.to_row_values() == ["Ada", "2026-05-19", "core, tabular"]
    assert UserRow.from_row_values(UserRow.headers(), row.to_row_values()) == UserRow(
        name="Ada",
        birthday=date(2026, 5, 19),
        tags=["core", "tabular"],
    )


@dataclass(slots=True)
class MemoryLocator:
    key: str


class MemoryBackend:
    def __init__(self):
        self.headers: list[str] | None = None
        self.rows_values: list[list[Any]] = []

    async def write_table(
        self,
        locator: MemoryLocator,
        headers: list[str] | None,
        rows_values: list[list[Any]],
        *,
        start_row: int = 1,
    ) -> tuple[int, int, int]:
        self.headers = headers or self.headers
        self.rows_values = rows_values
        return 1, len(rows_values), len(rows_values[0]) if rows_values else 0

    async def read_table(
        self,
        locator: MemoryLocator,
        *,
        start_row: int = 2,
        end_row: int | None = None,
        start_col: int = 1,
        end_col: int | None = None,
    ) -> tuple[list[str], list[list[Any]]]:
        return self.headers or [], self.rows_values


def test_table_repository_replace_and_list_all():
    async def run():
        backend = MemoryBackend()
        repository = TableRepository(backend, MemoryLocator("users"), UserRow)
        rows = [UserRow(name="Ada", birthday=date(2026, 5, 19), tags=["core"])]

        assert await repository.replace_all(rows) == (1, 1, 3)
        assert await repository.list_all() == rows

    asyncio.run(run())
