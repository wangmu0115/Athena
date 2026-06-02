from string import ascii_letters

from athena_bosun.parser.exceptions import LexerError
from athena_bosun.parser.preprocess import preprocess
from athena_bosun.parser.tokens import BUILTIN_FUNCS, BUILTIN_SYMBOLS, Token, TokenType


class Lexer:
    """Bosun 表达式词法分析器。

    Lexer 会先调用预处理逻辑，将 Bosun 源文本中的变量定义、告警入口等内容转换为
    单个表达式，然后按字符流依次产出 Token。

    支持的 Token 包括：
        - 数字字面量，例如 `1`, `0.1`, `1e-8`, `0xff`
        - 字符串字面量，例如 `"metric.name"`
        - Bosun 内置函数，例如 `q`, `avg`, `nv`
        - 算术、比较、逻辑运算符
        - 逗号和括号
    """

    def __init__(self, source: str):
        """初始化 Lexer。

        Args:
            source: Bosun 源文本，可以是预处理前的完整文本，也可以是单个表达式。
        """
        self.query_string = convert_bosun_query(source)

    def __iter__(self):
        """逐个产出 Token，最后总是产出 EOF Token。

        Raises:
            LexerError: 遇到无法识别的字符、非法标识符或非法运算符时抛出。
        """
        position = 0
        while position < len(self.query_string):
            ch = self.query_string[position]
            token_start = position
            match ch:
                case " " | "\r" | "\t" | "\n":  # skip whitespace
                    ...
                case "+" | "-" | "*" | "/" | "%":
                    yield Token(BUILTIN_SYMBOLS[ch], ch, token_start, token_start + 1)
                case ">" | "<" | "=" | "!":
                    comp_op = _read_operator(self.query_string, position, "=")
                    if comp_op not in BUILTIN_SYMBOLS:
                        raise LexerError(f"Unknown illegal operator: {comp_op}")
                    position += len(comp_op) - 1
                    yield Token(BUILTIN_SYMBOLS[comp_op], comp_op, token_start, token_start + len(comp_op))
                case "&" | "|" as logic_op:
                    logic_op = _read_operator(self.query_string, position, logic_op)
                    if logic_op not in BUILTIN_SYMBOLS:
                        raise LexerError(f"Unknown illegal operator: {logic_op}")
                    position += len(logic_op) - 1
                    yield Token(BUILTIN_SYMBOLS[logic_op], logic_op, token_start, token_start + len(logic_op))
                case "," | "(" | ")":
                    yield Token(BUILTIN_SYMBOLS[ch], ch, token_start, token_start + 1)
                case '"':
                    literal = _read_string(self.query_string, position)
                    position += len(literal) + 1
                    yield Token(TokenType.STRING, literal, token_start, position + 1)
                case _:
                    if _is_letter(ch):
                        iden = _read_iden(self.query_string, position)
                        if iden in BUILTIN_FUNCS:
                            position += len(iden) - 1
                            yield Token(TokenType.BUILT_IN_FUNC, iden, token_start, token_start + len(iden))
                        else:
                            raise LexerError(f"Unknown illegal identifier: {iden}")
                    elif _is_digit(ch):  # numbers
                        number = _read_number(self.query_string, position)
                        position += len(number) - 1
                        yield Token(TokenType.NUMBER, number, token_start, token_start + len(number))
                    else:
                        raise LexerError(f"Unknown illegal characters: {ch}")
            position += 1
        yield Token(TokenType.EOF, start=position, end=position)


def convert_bosun_query(source: str) -> str:
    """将 Bosun 源文本转换为 Lexer 可直接读取的表达式。

    Args:
        source: Bosun 源文本。

    Returns:
        经过预处理后的单个表达式字符串。
    """
    return preprocess(source)


def _read_iden(seq: str, start_position: int) -> str:  # 标识符: _abc, abc, abc_1, abc123, ...
    """从指定位置读取标识符。

    标识符由字母、数字和下划线组成，首字符由调用方保证已经是合法字母或下划线。

    Args:
        seq: 待读取的表达式字符串。
        start_position: 标识符起始位置。

    Returns:
        读取到的标识符文本。
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


def _read_string(seq: str, start_position: int) -> str:  # "<字符序列>"
    """从指定位置读取双引号字符串内容。

    当前 Lexer 不处理反斜杠转义，遇到下一个双引号即认为字符串结束。

    Args:
        seq: 待读取的表达式字符串。
        start_position: 起始双引号位置。

    Returns:
        不包含外层双引号的字符串内容。

    Raises:
        LexerError: 字符串没有闭合时抛出。
    """
    end_position = start_position + 1
    while end_position < len(seq) and seq[end_position] != '"':
        end_position += 1
    if end_position == len(seq):
        raise LexerError("The string must be enclosed in double quotes.")
    return seq[start_position + 1 : end_position]


def _read_number(seq: str, start_position: int) -> str:  # 整数: 42 ；浮点数: 0.1, 1e+7, 1e-7, 2.3e7
    """从指定位置读取数字字面量。

    支持整数、浮点数、科学计数法和十六进制整数。

    Args:
        seq: 待读取的表达式字符串。
        start_position: 数字起始位置。

    Returns:
        读取到的数字文本。

    Raises:
        LexerError: 数字格式非法时抛出。
    """
    is_hex = _is_hex(seq, start_position)  # 十六进制
    if is_hex:
        end_position = start_position + 2
        while end_position < len(seq) and seq[end_position] in "0123456789abcdefABCDEF":
            end_position += 1
        if end_position - start_position <= 2:
            raise LexerError(f"Invalid hex number: {seq[start_position:end_position]}")
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
            raise LexerError(f"Invalid scientific notation number: {number}")
        return number


def _read_operator(seq: str, position: int, allowed_postfix: str = "=") -> str:  # 运算符: >, >=, ...
    """从指定位置读取一元或二元运算符。

    对比较运算符，`allowed_postfix` 为 `=`，可读取 `>=`, `<=`, `==`, `!=`。
    对逻辑运算符，`allowed_postfix` 为当前字符，可读取 `&&`, `||`。

    Args:
        seq: 待读取的表达式字符串。
        position: 运算符起始位置。
        allowed_postfix: 允许跟在当前字符后的第二个字符。

    Returns:
        运算符文本。
    """
    if position >= len(seq) - 1:
        return seq[position]
    if seq[position + 1] == allowed_postfix:
        return seq[position : position + 2]
    else:
        return seq[position]


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
