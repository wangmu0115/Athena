from string import ascii_letters

from athena_kit.bosun.parser.exceptions import LexerError
from athena_kit.bosun.parser.preprocess import preprocess
from athena_kit.bosun.parser.tokens import BUILTIN_FUNCS, BUILTIN_SYMBOLS, Token, TokenType


class Lexer:
    """Bosun 表达式词法分析器。

    默认会先调用 `preprocess()`，将完整 Bosun 源文本转换为单个表达式。
    如果输入已经是预处理后的表达式，可以设置 `preprocessed=True` 跳过预处理。

    支持的 Token 包括：
        - 数字字面量，例如 `1`, `0.1`, `1e-8`, `0xff`
        - 字符串字面量，例如 `"metric.name"`
        - Bosun 内置函数，例如 `q`, `avg`, `nv`
        - 算术、比较、逻辑运算符
        - 逗号和括号

    注意：
        - `query_string` 保存的是实际被词法分析的表达式。
        - Token 的 `start` / `end` 位置基于 `query_string`，不一定基于原始 `source`。
    """

    def __init__(self, source: str, *, preprocessed: bool = False):
        """初始化 Lexer。

        Args:
            source: Bosun 源文本或已经预处理后的表达式。
            preprocessed:
                当为 `False` 时，先调用 `preprocess(source)`。
                当为 `True` 时，直接把 `source` 作为待词法分析表达式。
        """
        self._query_string = source if preprocessed else preprocess(source)

    @property
    def query_string(self):
        """实际被词法分析的表达式字符串。

        - 当 `preprocessed=False` 时，该值是 `preprocess(source)` 的结果。
        - 当 `preprocessed=True` 时，该值就是传入的 `source`。

        Token 的 `start` / `end` 位置均以该字符串为坐标基准。
        """
        return self._query_string

    def __iter__(self):
        """逐个产出 Token，最后总是产出 EOF Token。

        Raises:
            LexerError: 遇到无法识别的字符、非法标识符或非法运算符时抛出。
        """
        position = 0
        while position < len(self._query_string):
            ch = self._query_string[position]
            token_start = position
            match ch:
                case " " | "\r" | "\t" | "\n":  # skip whitespace
                    ...

                case "+" | "-" | "*" | "/" | "%":
                    yield Token(BUILTIN_SYMBOLS[ch], ch, token_start, token_start + 1)

                case ">" | "<" | "=" | "!":  # >, >=, <, <=, ==, !, !=
                    comp_op = _read_operator(self._query_string, position, "=")
                    position += len(comp_op) - 1
                    yield Token(BUILTIN_SYMBOLS[comp_op], comp_op, token_start, token_start + len(comp_op))

                case "&" | "|" as logic_op:  # &&, ||
                    logic_op = _read_operator(self._query_string, position, logic_op)
                    position += len(logic_op) - 1
                    yield Token(BUILTIN_SYMBOLS[logic_op], logic_op, token_start, token_start + len(logic_op))

                case "," | "(" | ")":
                    yield Token(BUILTIN_SYMBOLS[ch], ch, token_start, token_start + 1)

                case '"':
                    literal = _read_string(self._query_string, position)
                    position += len(literal) + 1
                    yield Token(TokenType.STRING, literal, token_start, position + 1)

                case _:
                    if _is_letter(ch):
                        iden = _read_iden(self._query_string, position)
                        if iden in BUILTIN_FUNCS:
                            position += len(iden) - 1
                            yield Token(TokenType.BUILT_IN_FUNC, iden, token_start, token_start + len(iden))
                        else:
                            raise LexerError(f"Unknown illegal identifier: {iden}.")
                    elif _is_digit(ch):
                        number = _read_number(self._query_string, position)
                        position += len(number) - 1
                        yield Token(TokenType.NUMBER, number, token_start, token_start + len(number))
                    else:
                        raise LexerError(f"Unknown illegal characters: {ch}.")
            position += 1

        yield Token(TokenType.EOF, start=position, end=position)


def _read_iden(seq: str, start_position: int) -> str:
    """从指定位置读取标识符。

    标识符由字母、数字和下划线组成，首字符由调用方保证已经是合法字母或下划线。
        _abc, abc, abc_1, abc123, ...
    """
    end_position = start_position + 1
    while end_position < len(seq):
        ch = seq[end_position]
        if _is_letter(ch) or _is_digit(ch):
            end_position += 1
        else:
            break
    iden = seq[start_position:end_position]
    return iden


def _read_string(seq: str, start_position: int) -> str:
    """从指定位置读取双引号字符串内容。

    当前 Lexer 不处理反斜杠转义，遇到下一个双引号即认为字符串结束。
    """
    end_position = start_position + 1
    while end_position < len(seq) and seq[end_position] != '"':
        end_position += 1
    if end_position == len(seq):
        raise LexerError("The string must be enclosed in double quotes.")
    return seq[start_position + 1 : end_position]


def _read_number(seq: str, start_position: int) -> str:
    """从指定位置读取数字字面量。

    支持整数、浮点数、科学计数法和十六进制整数。
        42, 0.1, 1e+7, 1e-7, 2.3e7, 0XABC
    """
    is_hex = _is_hex(seq, start_position)  # 十六进制
    if is_hex:
        end_position = start_position + 2
        while end_position < len(seq) and seq[end_position] in "0123456789abcdefABCDEF":
            end_position += 1
        if end_position - start_position <= 2:
            raise LexerError(f"Invalid hex number: {seq[start_position:end_position]}.")
        return seq[start_position:end_position]
    else:
        cnt_point = 0  # 小数点 <= 1
        cnt_e = 0  # 1e-8, 1e6
        end_position = start_position + 1
        while end_position < len(seq):
            ch = seq[end_position]
            match ch:
                case "." | "e" | "E":
                    cnt_point, cnt_e = _check_float(ch, cnt_point, cnt_e)
                    end_position += 1
                case "-" | "+":
                    if seq[end_position - 1] == "e" or seq[end_position - 1] == "E":
                        end_position += 1
                    else:
                        break
                case _:
                    if _is_digit(ch):
                        end_position += 1
                    else:
                        break

        number = seq[start_position:end_position]
        if number[-1] in {"e", "E"} or (number[-1] in {"+", "-"} and number[-2] in {"e", "E"}):
            raise LexerError(f"Invalid scientific notation number: {number}.")
        return number


def _read_operator(seq: str, position: int, allowed_postfix: str = "=") -> str:
    """从指定位置读取一元或二元运算符。

    - 比较运算符，`allowed_postfix` 为 `=`，可读取 `>=`, `<=`, `==`, `!=`。
    - 逻辑运算符，`allowed_postfix` 为当前字符，可读取 `&&`, `||`。

    Raises:
        LexerError: 当读取的运算符不在内置的运算符列表中时抛出。
    """

    if position >= len(seq) - 1:
        op = seq[position]
    elif seq[position + 1] == allowed_postfix:
        op = seq[position : position + 2]
    else:
        op = seq[position]

    if op in BUILTIN_SYMBOLS:
        return op
    raise LexerError(f"Unknown illegal operator: {op}.")


def _is_letter(ch: str) -> bool:
    """判断字符是否为 Bosun 标识符中的字母字符。"""
    return ch == "_" or ch in ascii_letters


def _is_digit(ch: str) -> bool:
    """判断字符是否为十进制数字。"""
    return ch in "0123456789"


def _is_hex(seq: str, position: int) -> bool:
    """判断指定位置是否是十六进制数字前缀 `0x` 或 `0X`。"""
    if position >= len(seq) - 1 or seq[position] != "0":
        return False
    return seq[position + 1] == "x" or seq[position + 1] == "X"


def _check_float(ch: str, cnt_point: int, cnt_e: int) -> tuple[int, int]:
    """检查浮点数字符读取状态。

    Args:
        ch: 当前读取到的字符，只处理 `.`, `e`, `E`。
        cnt_point: 当前已经读取到的小数点数量。
        cnt_e: 当前已经读取到的科学计数法标记数量。

    Returns:
        更新后的小数点数量和科学计数法标记数量。

    Raises:
        LexerError: 重复出现小数点、科学计数法标记，或 `e` 后出现小数点时抛出。
    """
    if ch == ".":
        if cnt_point >= 1:
            raise LexerError("The decimal point(`.`) can only appear once.")
        if cnt_e >= 1:
            raise LexerError("Scientific notation float (`e`), after `e` can not be floating-point.")
        return 1, cnt_e
    elif ch == "e" or ch == "E":
        if cnt_e >= 1:
            raise LexerError("The decimal point(`e`) can only appear once.")
        return cnt_point, 1
    else:
        return cnt_point, cnt_e
