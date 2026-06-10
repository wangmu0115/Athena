from collections.abc import Callable, Sequence

import httpx

type JSONScalar = str | int | float | bool
type JSONArray = list[JSONValue]
type JSONObject = dict[str, JSONValue]
type JSONValue = JSONScalar | None | JSONArray | JSONObject

type JSONPath = str | int | list[str | int]

type JSONObjectValidator = Callable[[JSONObject], None]


class _Missing:
    pass


_MISSING = _Missing()


class ResponseJSONError(Exception):
    """响应 JSON 处理异常的基类"""


class InvalidResponseJSONError(ResponseJSONError):
    """响应体不是合法 JSON 或 JSON 值不是预期形态"""


class ResponseJSONValidationError(ResponseJSONError):
    """响应 JSON 对象校验失败"""

    def __init__(self, message: str, *, payload: JSONObject | None = None):
        super().__init__(message)
        self.payload = payload


def parse_response_json(response: httpx.Response) -> JSONValue:
    """解析 HTTP 响应体中的 JSON，可能是对象、数组、字符串、数字、布尔值或 `None`。

    Raises:
        InvalidResponseJSONError: 响应体不是合法 JSON。
    """
    try:
        return response.json()
    except ValueError as exc:
        raise InvalidResponseJSONError("Response body is not valid JSON") from exc


def extract_response_json_value(
    response: httpx.Response,
    path: JSONPath | None = None,
    *,
    validator: JSONObjectValidator | None = None,
    default: JSONValue = None,
) -> JSONValue:
    """解析 HTTP 响应 JSON，并可选地按路径提取单个值。

    字符串路径支持便捷语法，例如 `"data.items[0].id"`。
    如果 JSON 字段名本身包含 `.` 或 `[index]` 形式的文本，请使用显式列表路径，例如 `["data.items[0]", "id"]`。

    Args:
        response: HTTP 响应对象。
        path: 要提取的路径。传入 `None` 时返回完整 JSON 值；传入 `str` 时读取对象字段；
            传入 `int` 时读取数组下标；传入列表时逐层读取。
        validator: JSON 对象校验函数，接收完整 JSON 对象，校验失败时应抛出异常；传入 `None` 时跳过校验。
        default: 路径不存在或类型不匹配时返回的默认值。
    """
    value = parse_response_json(response)
    if validator is not None:
        validator(_ensure_json_object(value))

    if path is None:
        return value

    return _get_json_value(value, path, default=default)


def extract_response_json_values(
    response: httpx.Response,
    paths: list[JSONPath],
    *,
    validator: JSONObjectValidator | None = None,
) -> tuple[JSONValue, ...]:
    """解析 HTTP 响应 JSON，并按多个路径提取值。

    Args:
        response: HTTP 响应对象。
        paths: 要提取的路径列表，不能为空。每个路径都可以是便捷字符串路径、数组下标或显式列表路径。
            某个路径不存在或类型不匹配时，该路径对应的结果为 `None`。
        validator: JSON 对象校验函数，接收完整 JSON 对象，校验失败时应抛出异常；传入 `None` 时跳过校验。
    """
    if not paths:
        raise ValueError("paths should not be an empty list.")

    value = parse_response_json(response)
    if validator is not None:
        validator(_ensure_json_object(value))

    return tuple(_get_json_value(value, path) for path in paths)


def create_biz_code_validator(
    *,
    code_key: str = "code",
    success_codes: Sequence[int | str] = (0,),
    message_key: str = "message",
) -> JSONObjectValidator:
    """创建基于业务状态码的 JSON 对象验证函数。

    Args:
        code_key: 业务状态码字段名。
        success_codes: 表示成功的业务状态码集合。
        message_key: 业务错误消息字段名。
    """

    def _validate_object(payload: JSONObject) -> None:
        code = payload.get(code_key)
        if code is None:
            raise ResponseJSONValidationError(f"Missing biz status field: {code_key}", payload=payload)

        if code not in success_codes:
            message = payload.get(message_key, f"Missing error message field: {message_key}")
            raise ResponseJSONValidationError(f"Request failed: code={code}, message={message}", payload=payload)

    return _validate_object


def _get_json_value(value: JSONValue, path: JSONPath, *, default: JSONValue = None) -> JSONValue:
    parts = _parse_json_path(path)
    current: JSONValue = value

    for part in parts:
        child = _get_json_child(current, part)
        if child is _MISSING:
            return default
        current = child

    return current


def _get_json_child(value: JSONValue, part: str | int) -> JSONValue | _Missing:
    if isinstance(value, dict) and isinstance(part, str):
        return value.get(part, _MISSING)

    if isinstance(value, list) and isinstance(part, int) and -len(value) <= part < len(value):
        return value[part]

    return _MISSING


def _parse_json_path(path: JSONPath) -> list[str | int]:
    """把公开的 JSON path 表达解析成最小路径片段。

    Args:
        path: JSON path。`int` 表示根数组下标；`list[str | int]` 表示显式路径；
            `str` 表示便捷路径，会按 `.` 拆分 segment，并在每个 segment 内解析 `[index]`。

    Returns:
        由字符串字段名和数组下标组成的路径片段列表。

    Raises:
        ValueError: `path` 为空字符串、空列表、包含空路径片段，或便捷路径 segment 不合法。
    """
    if isinstance(path, int):
        return [path]

    if isinstance(path, list):
        if not path:
            raise ValueError("`path` should not be an empty list.")
        if all(isinstance(part, (str, int)) and part != "" for part in path):
            return path
        raise ValueError("`path` should contain non-empty strings or integers only.")

    if not path:
        raise ValueError("`path` should not be an empty string.")

    parts: list[str | int] = []
    for segment in path.split("."):
        if not segment:
            raise ValueError("`path` should not contain empty segments.")
        _parse_json_path_segment(segment, parts)
    return parts


def _parse_json_path_segment(segment: str, parts: list[str | int]) -> None:
    """解析便捷字符串路径中的一个 segment。

    合法 segment 必须以字段名开始，可以在字段名后附加一个数组下标：
    - `"abc"` 会解析为 `["abc"]`
    - `"abc[0]"` 会解析为 `["abc", 0]`
    - `"abc[12]"` 会解析为 `["abc", 12]`

    非法 segment 包括：
    - `"[0]"`，数组下标不能作为字符串 segment 的开头；根数组下标应使用 `path=0` 或 `path=[0]`
    - `"abc0]"`，右方括号必须与左方括号成对出现
    - `"abc[0"`，数组下标必须用右方括号闭合
    - `"abc[]"`，数组下标不能为空
    - `"abc[x]"`，数组下标必须是整数
    - `"abc[0][1]"`、`"abc[0, 1]"`，单个 segment 只能包含一个数组下标

    Args:
        segment: 已经按 `.` 拆分后的路径片段。
        parts: 解析结果会追加到该列表中。

    Raises:
        ValueError: segment 不符合便捷路径语法。
    """
    if segment.startswith("[") or ("]" in segment and "[" not in segment):
        raise ValueError("`path` segment should start with a field name.")

    field_chars: list[str] = []
    index = 0

    while index < len(segment):
        char = segment[index]
        if char == "]":
            raise ValueError("`path` array index should start with '['.")

        if char != "[":
            field_chars.append(char)
            index += 1
            continue

        if not field_chars:
            raise ValueError("`path` array index should follow a field name.")

        parts.append("".join(field_chars))  # 完成字段名解析
        field_chars = []

        close_index = segment.find("]", index + 1)
        if close_index == -1:
            raise ValueError("`path` array index should be closed with ']'.")

        raw_index = segment[index + 1 : close_index]
        if not raw_index:
            raise ValueError("`path` array index should not be empty.")
        try:
            parts.append(int(raw_index))
        except ValueError as exc:
            raise ValueError("`path` array index should be an integer.") from exc

        index = close_index + 1
        if index < len(segment):
            raise ValueError("`path` segment should contain at most one array index.")

    # 当 segment 类似于 "abc" 时，会走到这里
    if field_chars:
        parts.append("".join(field_chars))


def _ensure_json_object(value: JSONValue) -> JSONObject:
    """确保 JSON 类型是 dict，否则抛出异常 `InvalidResponseJSONError`。"""
    if isinstance(value, dict):
        return value

    raise InvalidResponseJSONError(f"JSON value should be object, get {type(value).__name__}.")
