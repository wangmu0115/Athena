def col_to_index(col: str) -> int:
    col = col.upper()
    index = 0
    for i, char in enumerate(reversed(col)):
        index += (ord(char) - ord("A") + 1) * (26**i)
    return index


def index_to_col(index: int) -> str:
    col = ""
    while index > 0:
        index -= 1
        col = chr((index % 26) + ord("A")) + col
        index //= 26
    return col


def calculate_range(
    sheet_id: str,
    n_rows: int,
    n_cols: int,
    start_row: int = 1,
    start_col: int = 1,
) -> str:
    end_col = index_to_col(start_col + n_cols - 1)
    end_row = start_row + n_rows - 1
    return f"{sheet_id}!{index_to_col(start_col)}{start_row}:{end_col}{end_row}"
