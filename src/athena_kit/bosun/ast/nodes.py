from __future__ import annotations

from dataclasses import dataclass

from athena_kit.bosun.parser.tokens import Token

type LiteralValue = int | float | str


@dataclass(frozen=True, slots=True)
class Program:
    """Bosun 表达式 AST 根节点。

    不承载 query 提取、公式生成等业务逻辑，需要分析 AST 时，请使用 `athena_kit.bosun.ast.queries` 中的函数。
    """

    expression: Expression


class Expression:
    """Bosun 表达式 AST 节点基类。

    该基类用于统一表达式节点类型，方便 parser 和后续分析函数做类型标注与模式匹配。
    它不定义行为，具体语义由子类表达。
    """


@dataclass(frozen=True, slots=True)
class NameExpression(Expression):
    """名称表达式。

    当前主要用于表示函数调用左侧的函数名，例如 `q`、`avg`、`nv`。
    """

    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True, slots=True)
class LiteralExpression(Expression):
    """字面量表达式基类。

    保存 parser 从 token 中解析出的 Python 字面量值，具体子类用于区分整数、浮点数和字符串。
    """

    literal: LiteralValue

    def __str__(self) -> str:
        return str(self.literal)


class IntLiteralExpression(LiteralExpression): ...


class FloatLiteralExpression(LiteralExpression): ...


class StrLiteralExpression(LiteralExpression):
    """字符串字面量表达式。

    `literal` 保存去掉外层双引号后的字符串内容，`__str__` 会重新补回双引号，用于表达式调试输出。
    """

    literal: str

    def __str__(self) -> str:
        return f'"{self.literal}"'


@dataclass(frozen=True, slots=True)
class UnaryOperatorExpression(Expression):
    """一元运算表达式，表示 `+x`、`-x`、`!x` 这类前缀运算。

    - `operator` 保留原始运算符 token。
    - `right` 保存一元运算的右操作数。
    """

    operator: Token
    right: Expression

    def __str__(self) -> str:
        return f"({self.operator.text}{self.right})"


@dataclass(frozen=True, slots=True)
class BinaryOperatorExpression(Expression):
    """二元运算表达式，表示算术、比较和逻辑二元运算。

    - `operator` 保留原始运算符 token。
    - `left` 与 `right` 保存左右操作数。
    """

    left: Expression
    operator: Token
    right: Expression

    def __str__(self) -> str:
        return f"({self.left} {self.operator.text} {self.right})"


@dataclass(frozen=True, slots=True)
class CallExpression(Expression):
    """函数调用表达式，表示 `func(arg1, arg2, ...)`。

    - `function` 保存函数名。
    - `args` 保存按原始顺序解析出的参数表达式列表。
    """

    function: str
    args: list[Expression]

    def __str__(self) -> str:
        return f"{self.function}({','.join(str(arg) for arg in self.args)})"
