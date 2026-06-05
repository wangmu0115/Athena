from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.bosun.opentsdb.enums import Aggregator, FilterType, MultiFunction
    from athena_kit.bosun.opentsdb.exceptions import OpenTSDBParseError
    from athena_kit.bosun.opentsdb.intervals import calc_interval_seconds
    from athena_kit.bosun.opentsdb.models import (
        Downsampling,
        MultiField,
        Query,
        Rate,
        TagKv,
        TopK,
    )
    from athena_kit.bosun.opentsdb.parser import (
        parse_downsampling,
        parse_multifield,
        parse_query,
        parse_rate,
        parse_tagkv,
        parse_topk,
    )
    from athena_kit.bosun.opentsdb.serializer import (
        serialize_downsampling,
        serialize_multifield,
        serialize_query,
        serialize_rate,
        serialize_tagkv,
        serialize_topk,
    )

__all__ = (
    "Aggregator",
    "FilterType",
    "MultiFunction",
    "OpenTSDBParseError",
    "calc_interval_seconds",
    "Downsampling",
    "MultiField",
    "Query",
    "Rate",
    "TagKv",
    "TopK",
    "parse_downsampling",
    "parse_multifield",
    "parse_query",
    "parse_rate",
    "parse_tagkv",
    "parse_topk",
    "serialize_downsampling",
    "serialize_multifield",
    "serialize_query",
    "serialize_rate",
    "serialize_tagkv",
    "serialize_topk",
)

_dynamic_imports = {
    "Aggregator": "enums",
    "FilterType": "enums",
    "MultiFunction": "enums",
    "OpenTSDBParseError": "exceptions",
    "calc_interval_seconds": "intervals",
    "Downsampling": "models",
    "MultiField": "models",
    "Query": "models",
    "Rate": "models",
    "TagKv": "models",
    "TopK": "models",
    "parse_downsampling": "parser",
    "parse_multifield": "parser",
    "parse_query": "parser",
    "parse_rate": "parser",
    "parse_tagkv": "parser",
    "parse_topk": "parser",
    "serialize_downsampling": "serializer",
    "serialize_multifield": "serializer",
    "serialize_query": "serializer",
    "serialize_rate": "serializer",
    "serialize_tagkv": "serializer",
    "serialize_topk": "serializer",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
