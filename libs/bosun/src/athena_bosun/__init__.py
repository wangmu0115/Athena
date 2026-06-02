from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_bosun.parser import Lexer, Parser
    from athena_bosun.parser.preprocess import preprocess

__all__ = (
    "Lexer",
    "Parser",
    "preprocess",
)

_dynamic_imports = {
    "Lexer": "parser",
    "Parser": "parser",
    "preprocess": "parser.preprocess",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {attr_name!r}")
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
