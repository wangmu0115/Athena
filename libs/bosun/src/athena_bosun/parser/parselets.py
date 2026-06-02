from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum
from typing import TYPE_CHECKING

from athena_bosun.ast.ast import (
    BinaryOperatorExpression,
    CallExpression,
    Expression,
    FloatLiteralExpression,
    IntLiteralExpression,
    LiteralExpression,
    NameExpression,
    StrLiteralExpression,
    UnaryOperatorExpression,
)
from athena_bosun.parser.exceptions import ParserError
from athena_bosun.parser.tokens import Token, TokenType

if TYPE_CHECKING:
    from athena_bosun.parser.parser import Parser


class Precedence(IntEnum):  # 运算优先级
    DEFAULT = -1
    ASSIGN_BELOW = 0  # assign is right-associative
    ASSIGN = 1  # =, +=, -=, *=, /=, |=, &=
    CONDITIONAL = 2  # ? :
    LOGICAL = 3  # &, |
    EQUALS = 4  # ==, !=
    LEGE = 5  # <, <=, >, >=
    ADDSUB = 6  # +, -
    MULDIVMOD = 7  # *, /
    PREFIX = 8  # !, +, -
    CALL = 9  # callable(x)


class PrefixParselet(ABC):
    """Prefix parselet interface used by the Pratt parser."""

    @abstractmethod
    def parse(self, parser: Parser, token: Token) -> Expression: ...


class InfixParselet(ABC):
    @abstractmethod
    def parse(self, parser: Parser, left: Expression, token: Token) -> Expression: ...

    @property
    @abstractmethod
    def precedence(self) -> Precedence: ...


def standard_prefix_parselets() -> dict[TokenType, PrefixParselet]:
    return {
        TokenType.BUILT_IN_FUNC: NameParselet(),
        TokenType.NUMBER: LiteralParselet(),
        TokenType.STRING: LiteralParselet(),
        TokenType.ADD: UnaryOperatorParselet(),
        TokenType.SUB: UnaryOperatorParselet(),
        TokenType.NOT: UnaryOperatorParselet(),
        TokenType.LPAREN: GroupParselet(),
    }


def standard_infix_parselets() -> dict[TokenType, InfixParselet]:
    return {
        # call
        TokenType.LPAREN: CallParselet(),
        # binary operators
        TokenType.ADD: BinaryOperatorParselet(Precedence.ADDSUB),
        TokenType.SUB: BinaryOperatorParselet(Precedence.ADDSUB),
        TokenType.MUL: BinaryOperatorParselet(Precedence.MULDIVMOD),
        TokenType.DIV: BinaryOperatorParselet(Precedence.MULDIVMOD),
        TokenType.MOD: BinaryOperatorParselet(Precedence.MULDIVMOD),
        TokenType.LT: BinaryOperatorParselet(Precedence.LEGE),
        TokenType.LE: BinaryOperatorParselet(Precedence.LEGE),
        TokenType.GT: BinaryOperatorParselet(Precedence.LEGE),
        TokenType.GE: BinaryOperatorParselet(Precedence.LEGE),
        TokenType.EQ: BinaryOperatorParselet(Precedence.EQUALS),
        TokenType.NEQ: BinaryOperatorParselet(Precedence.EQUALS),
        TokenType.AND: BinaryOperatorParselet(Precedence.LOGICAL),
        TokenType.OR: BinaryOperatorParselet(Precedence.LOGICAL),
    }


class NameParselet(PrefixParselet):
    """Simple parselet for function name like: "q", "sum", ...."""

    def parse(self, parser: Parser, token: Token) -> NameExpression:
        return NameExpression(token.text)


class LiteralParselet(PrefixParselet):
    """Simple parselet for int/float/str literal."""

    def parse(self, parser: Parser, token: Token) -> LiteralExpression:
        match token.type:
            case TokenType.STRING:
                return StrLiteralExpression(token.text)
            case TokenType.NUMBER:
                number_txt = token.text
                if "." in number_txt or "e" in number_txt or "E" in number_txt:
                    return FloatLiteralExpression(float(number_txt))
                elif number_txt.startswith("0x") or number_txt.startswith("0X"):
                    return IntLiteralExpression(int(number_txt, 16))
                else:
                    return IntLiteralExpression(int(number_txt, 10))
            case _:
                raise NotImplementedError()


class GroupParselet(PrefixParselet):
    """Prase parentheses used to group an expression. like "5 * (2 + 3)"."""

    def parse(self, parser: Parser, token: Token) -> Expression:
        parser.consume_next()  # move to the beginning of expression in parentheses.
        expr = parser.parse_expression(Precedence.DEFAULT)  # ( {} )
        parser.consume_next()  # move to right parenthese
        if parser.curr_token.type != TokenType.RPAREN:
            raise ParserError("The grouped expression must end with a right parenthese.")
        return expr


class UnaryOperatorParselet(PrefixParselet):
    """Generic prefix parselet for a unary arithmetic operator.
    Unary operators: +, -, !
    """

    def parse(self, parser: Parser, token: Token) -> UnaryOperatorExpression:
        parser.consume_next()  # move to the beginning of right operand
        right = parser.parse_expression(Precedence.PREFIX)
        return UnaryOperatorExpression(token, right)


class BinaryOperatorParselet(InfixParselet):
    """Generic infix parselet for a binary arithmetic operator.
    Binary operators: +, -, *, /, %, >, >=, <, <=, ==, !=, &&, ||
    """

    def __init__(self, precedence: Precedence):
        self.__precedence = precedence

    def parse(self, parser: Parser, left: Expression, token: Token) -> BinaryOperatorExpression:
        parser.consume_next()  # move to the beginning of right operand
        right = parser.parse_expression(self.precedence)
        return BinaryOperatorExpression(left, token, right)

    @property
    def precedence(self) -> Precedence:
        return self.__precedence


class CallParselet(InfixParselet):
    def parse(self, parser: Parser, left: Expression, token: Token) -> CallExpression:
        if not isinstance(left, NameExpression):
            raise ParserError(f"The function of call expression must be a simple name, but get: {left!r}")
        args: list[Expression] = []
        while parser.peek_token is not None and parser.peek_token.type != TokenType.EOF:
            parser.consume_next()  # move to the argument expression
            if parser.curr_token.type == TokenType.RPAREN:
                break
            args.append(parser.parse_expression(Precedence.DEFAULT))
            if parser.peek_token.type == TokenType.COMMA:  # more arguments...
                parser.consume_next()
        if parser.curr_token.type != TokenType.RPAREN:
            raise ParserError("The arguments of call expression must be enclosed in parentheses.")
        return CallExpression(left.name, args)

    @property
    def precedence(self) -> Precedence:
        return Precedence.CALL
