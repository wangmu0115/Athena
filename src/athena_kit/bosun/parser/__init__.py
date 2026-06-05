from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from athena_kit.bosun.parser.exceptions import BosunPreprocessError, LexerError, ParserError
    from athena_kit.bosun.parser.lexer import Lexer
    from athena_kit.bosun.parser.parser import Parser
    from athena_kit.bosun.parser.tokens import Token, TokenType

__all__ = (
    "BosunPreprocessError",
    "Lexer",
    "LexerError",
    "Parser",
    "ParserError",
    "Token",
    "TokenType",
)

_DYNAMIC_IMPORTS = {
    "BosunPreprocessError": "exceptions",
    "Lexer": "lexer",
    "LexerError": "exceptions",
    "Parser": "parser",
    "ParserError": "exceptions",
    "Token": "tokens",
    "TokenType": "tokens",
}


def __getattr__(attr_name: str) -> object:
    module_name = _DYNAMIC_IMPORTS.get(attr_name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {attr_name!r}")

    module = import_module(f"{__name__}.{module_name}")
    result = getattr(module, attr_name)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
