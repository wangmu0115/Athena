from __future__ import annotations

from athena_bosun.ast.nodes import Expression, Program
from athena_bosun.parser.exceptions import ParserError
from athena_bosun.parser.lexer import Lexer
from athena_bosun.parser.parselets import Precedence, standard_infix_parselets, standard_prefix_parselets
from athena_bosun.parser.tokens import Token, TokenType


class Parser:
    def __init__(self, lexer: Lexer):
        self.tokens = iter(lexer)
        self.curr_token: Token = next(self.tokens)
        self.peek_token: Token | None = next(self.tokens, None)
        self.prefix_parselets = standard_prefix_parselets()
        self.infix_parselets = standard_infix_parselets()

    def parse(self) -> Program:
        expr = self.parse_expression(Precedence.DEFAULT)
        if self.peek_token is not None and self.peek_token.type != TokenType.EOF:
            raise ParserError(f"Unexpected token after expression: {self.peek_token}.")
        return Program(expr)

    def parse_expression(self, precedence: Precedence = Precedence.DEFAULT) -> Expression:
        prefix = self.prefix_parselets.get(self.curr_token.type, None)
        if prefix is None:
            raise ParserError(f"Could not parse {self.curr_token}")
        left = prefix.parse(self, self.curr_token)

        infix = self._peek_infix_parselet()
        while infix is not None and precedence < infix.precedence:
            self.consume_next()  # move to the infix operator
            left = infix.parse(self, left, self.curr_token)
            infix = self._peek_infix_parselet()
        return left

    def consume_next(self) -> None:
        if self.peek_token is None:
            raise ParserError("Unexpected end of input.")
        self.curr_token = self.peek_token
        self.peek_token = next(self.tokens, None)

    def _peek_infix_parselet(self):
        if self.peek_token is None:
            return None
        return self.infix_parselets.get(self.peek_token.type, None)
