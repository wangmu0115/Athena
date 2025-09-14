from typing import Union
from urllib.parse import parse_qs, unquote, urlparse


def parse_url_querystring(url: str, drop_na: bool = True, na_str: str = "None") -> tuple[str, dict[str, Union[str, list[str]]]]:
    parsed_url = urlparse(url)  # urllib.parse.ParseResult
    query_params = {}
    if parsed_url.query and len(parsed_url.query) > 0:
        for key, values in parse_qs(parsed_url.query).items():
            decoded_values = [unquote(value) for value in values if not drop_na or unquote(value) != na_str]
            if decoded_values:  # only non-None value
                if len(decoded_values) == 1:
                    query_params[key] = decoded_values[0]
                else:
                    query_params[key] = decoded_values
    return parsed_url._replace(query="").geturl(), query_params
