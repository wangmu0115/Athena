from dataclasses import dataclass
from enum import StrEnum
from string import ascii_letters


class TokenType(StrEnum):
    """Bosun 表达式中的 Token 类型，Token 是词法分析阶段产生的最小语法单元，用于后续 Parser 构建 AST。

    - 特殊标记: EOF、ILLEGAL
    - 字面量: NUMBER、STRING
    - 算术运算符: +、-、*、/、%
    - 逻辑运算符: !、&&、||
    - 比较运算符: <、<=、>、>=、==、!=
    - 分隔符: 逗号、括号
    - 内置函数: q、shift、sum 等 Bosun 内置函数
    """

    ILLEGAL = "____ILLEGAL____"  # unsupported token
    EOF = "____EOF____"  # End Of File

    NUMBER = "____NUMBER____"
    STRING = "____STRING____"

    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"

    NOT = "!"
    AND = "&&"
    OR = "||"

    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    EQ = "=="
    NEQ = "!="

    COMMA = ","

    LPAREN = "("
    RPAREN = ")"

    BUILT_IN_FUNC = "built-in func"


@dataclass(frozen=True)
class Token:
    """词法分析阶段产生的 Token，一个 Token 表示 Bosun 表达式中的一个最小语法单元。

    Attributes:
        type: Token 类型。
        text: Token 对应的原始文本内容。例如：
            - NUMBER -> "123"
            - STRING -> "cpu.usage"
            - ADD -> "+"
            - BUILT_IN_FUNC -> "q"
        start: Token 在原始表达式中的起始位置（包含）。
        end: Token 在原始表达式中的结束位置（不包含）。

    Examples:
        >>> Token(TokenType.NUMBER, "123", 0, 3)
        NUMBER('123')

        >>> Token(TokenType.BUILT_IN_FUNC, "q", 10, 11)
        BUILT_IN_FUNC('q')
    """

    type: TokenType
    text: str | None = None
    start: int | None = None
    end: int | None = None

    def __post_init__(self):
        if self.text is None:
            object.__setattr__(self, "text", self.type.value)

    def __repr__(self):
        return f"Token(type={self.type.name}, text={self.text!r}, start={self.start}, end={self.end})"

    def __str__(self):
        return f"{self.type.name}({self.text!r})"


#: Bosun 内置函数名称集合。
BUILTIN_FUNCS: set[str] = {
    "q",
    "shift",
    "sum",
    "avg",
    "max",
    "min",
    "fv",
    "nv",
    "nanas",
}


#: 运算符文本到 TokenType 的映射表。
BUILTIN_SYMBOLS: dict[str, TokenType] = {
    tt.value: tt
    for tt in TokenType
    if tt.value 
    and tt.value[0] not in ascii_letters 
    and not tt.value.startswith("____")
}  # fmt: off
