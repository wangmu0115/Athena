import asyncio
from dataclasses import dataclass
from datetime import date
from typing import Any

from athena_kit.core.tabular import AsyncTableRepository, TableCell, TableRepository, TableRow


class UserRow(TableRow):
    name: str = TableCell(title="姓名", order=1)
    birthday: date = TableCell(title="生日", order=2)
    tags: list[str] = TableCell(title="标签", order=3, default_factory=list)


class AliasRow(TableRow):
    name: str = TableCell(alias="姓名")


def test_table_row_headers_and_round_trip():
    row = UserRow(name=" Ada ", birthday=date(2026, 5, 19), tags=["core", " tabular "])

    assert UserRow.table_headers() == ["姓名", "生日", "标签"]
    assert row.to_table_row() == ["Ada", "2026-05-19", "core, tabular"]
    assert UserRow.from_table_row(UserRow.table_headers(), row.to_table_row()) == UserRow(
        name="Ada",
        birthday=date(2026, 5, 19),
        tags=["core", "tabular"],
    )


def test_table_row_uses_alias_as_header_when_title_is_missing():
    assert AliasRow.table_headers() == ["姓名"]
    assert AliasRow.from_table_row(["姓名"], ["Ada"]) == AliasRow(name="Ada")


@dataclass(slots=True)
class MemoryLocator:
    key: str


class MemoryBackend:
    def __init__(self):
        self.headers: list[str] | None = None
        self.rows_values: list[list[Any]] = []
        self.version = 0

    def write_table(
        self,
        locator: MemoryLocator,
        headers: list[str] | None,
        rows_values: list[list[Any]],
        *,
        start_row: int = 1,
    ) -> tuple[int, int, int]:
        self.version += 1
        self.headers = headers or self.headers
        self.rows_values = rows_values
        return self.version, len(rows_values), len(rows_values[0]) if rows_values else 0

    def read_table(
        self,
        locator: MemoryLocator,
        *,
        start_row: int = 2,
        end_row: int | None = None,
        start_col: int = 1,
        end_col: int | None = None,
        has_headers: bool = True,
        return_headers: bool = True,
    ) -> tuple[list[str], list[list[Any]]]:
        headers = self.headers or []
        if not has_headers or not return_headers:
            headers = []
        return headers, self.rows_values


class AsyncMemoryBackend:
    def __init__(self):
        self.headers: list[str] | None = None
        self.rows_values: list[list[Any]] = []
        self.version = 0

    async def write_table(
        self,
        locator: MemoryLocator,
        headers: list[str] | None,
        rows_values: list[list[Any]],
        *,
        start_row: int = 1,
    ) -> tuple[int, int, int]:
        self.version += 1
        self.headers = headers or self.headers
        self.rows_values = rows_values
        return self.version, len(rows_values), len(rows_values[0]) if rows_values else 0

    async def read_table(
        self,
        locator: MemoryLocator,
        *,
        start_row: int = 2,
        end_row: int | None = None,
        start_col: int = 1,
        end_col: int | None = None,
        has_headers: bool = True,
        return_headers: bool = True,
    ) -> tuple[list[str], list[list[Any]]]:
        headers = self.headers or []
        if not has_headers or not return_headers:
            headers = []
        return headers, self.rows_values


def test_table_repository_replace_and_list_all():
    backend = MemoryBackend()
    repository = TableRepository(backend, MemoryLocator("users"), UserRow)
    rows = [UserRow(name="Ada", birthday=date(2026, 5, 19), tags=["core"])]

    assert repository.replace_all(rows) == (1, 1, 3)
    assert repository.list_all() == rows


def test_table_repository_list_all_without_headers():
    backend = MemoryBackend()
    backend.rows_values = [["Ada", "2026-05-19", "core"]]
    repository = TableRepository(backend, MemoryLocator("users"), UserRow)

    assert repository.list_all(has_headers=False) == [
        UserRow(name="Ada", birthday=date(2026, 5, 19), tags=["core"]),
    ]


def test_table_backend_read_table_can_omit_headers():
    backend = MemoryBackend()
    backend.headers = ["姓名", "生日", "标签"]
    backend.rows_values = [["Ada", "2026-05-19", "core"]]

    assert backend.read_table(MemoryLocator("users"), return_headers=False) == (
        [],
        [["Ada", "2026-05-19", "core"]],
    )
    assert backend.read_table(MemoryLocator("users"), has_headers=False, start_row=1) == (
        [],
        [["Ada", "2026-05-19", "core"]],
    )


def test_async_table_repository_replace_and_list_all():
    async def run():
        backend = AsyncMemoryBackend()
        repository = AsyncTableRepository(backend, MemoryLocator("users"), UserRow)
        rows = [UserRow(name="Ada", birthday=date(2026, 5, 19), tags=["core"])]

        assert await repository.replace_all(rows) == (1, 1, 3)
        assert await repository.list_all() == rows

    asyncio.run(run())


def test_async_table_repository_list_all_without_headers():
    async def run():
        backend = AsyncMemoryBackend()
        backend.rows_values = [["Ada", "2026-05-19", "core"]]
        repository = AsyncTableRepository(backend, MemoryLocator("users"), UserRow)

        assert await repository.list_all(has_headers=False) == [
            UserRow(name="Ada", birthday=date(2026, 5, 19), tags=["core"]),
        ]

    asyncio.run(run())
