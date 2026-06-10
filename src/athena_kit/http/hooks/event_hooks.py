from athena_kit.http.hooks.logging import (
    LoggingOptions,
    create_async_logging_hooks,
    create_logging_hooks,
)
from athena_kit.http.hooks.request_id import (
    RequestIDOptions,
    create_async_request_id_hook,
    create_request_id_hook,
)
from athena_kit.http.hooks.response_status import (
    ResponseStatusOptions,
    create_async_response_status_hook,
    create_response_status_hook,
)
from athena_kit.http.hooks.types import (
    AsyncEventHooks,
    AsyncRequestHook,
    AsyncResponseHook,
    EventHooks,
    RequestHook,
    ResponseHook,
)


def build_event_hooks(
    event_hooks: EventHooks | None = None,
    *,
    request_id: bool | RequestIDOptions = False,
    logging: bool | LoggingOptions = False,
    response_status: bool | ResponseStatusOptions = False,
) -> dict[str, list[RequestHook | ResponseHook]]:
    """构建同步 HTTPX event hooks。

    Args:
        event_hooks: 调用方提供的 HTTPX event hooks，会保留原有顺序并作为结果的起点。
        request_id: 是否启用请求 ID hook。传入 `True` 时使用 `RequestIDOptions` 默认配置，传入
            `RequestIDOptions` 时使用自定义配置，传入 `False` 时不启用。
        logging: 是否启用日志 hook。传入 `True` 时使用 `LoggingOptions` 默认配置，传入 `LoggingOptions`
            时使用自定义配置，传入 `False` 时不启用。
        response_status: 是否启用响应状态 hook。传入 `True` 时使用 `ResponseStatusOptions` 默认配置，传入
            `ResponseStatusOptions` 时使用自定义配置，传入 `False` 时不启用。
    """
    request_hooks = list((event_hooks or {}).get("request", []))
    response_hooks = list((event_hooks or {}).get("response", []))

    if request_id:
        options = request_id if isinstance(request_id, RequestIDOptions) else None
        request_hooks.append(create_request_id_hook(options))

    if logging:
        options = logging if isinstance(logging, LoggingOptions) else None
        log_request, log_response = create_logging_hooks(options)
        request_hooks.append(log_request)
        response_hooks.append(log_response)

    if response_status:
        options = response_status if isinstance(response_status, ResponseStatusOptions) else None
        response_hooks.append(create_response_status_hook(options))

    return {
        "request": request_hooks,
        "response": response_hooks,
    }


def build_async_event_hooks(
    event_hooks: AsyncEventHooks | None = None,
    *,
    request_id: bool | RequestIDOptions = False,
    logging: bool | LoggingOptions = False,
    response_status: bool | ResponseStatusOptions = False,
) -> dict[str, list[AsyncRequestHook | AsyncResponseHook]]:
    """构建异步 HTTPX event hooks。

    Args:
        event_hooks: 调用方提供的 HTTPX event hooks，会保留原有顺序并作为结果的起点。
        request_id: 是否启用请求 ID hook。传入 `True` 时使用 `RequestIDOptions` 默认配置，传入
            `RequestIDOptions` 时使用自定义配置，传入 `False` 时不启用。
        logging: 是否启用日志 hook。传入 `True` 时使用 `LoggingOptions` 默认配置，传入 `LoggingOptions`
            时使用自定义配置，传入 `False` 时不启用。
        response_status: 是否启用响应状态 hook。传入 `True` 时使用 `ResponseStatusOptions` 默认配置，传入
            `ResponseStatusOptions` 时使用自定义配置，传入 `False` 时不启用。
    """
    request_hooks = list((event_hooks or {}).get("request", []))
    response_hooks = list((event_hooks or {}).get("response", []))

    if request_id:
        options = request_id if isinstance(request_id, RequestIDOptions) else None
        request_hooks.append(create_async_request_id_hook(options))

    if logging:
        options = logging if isinstance(logging, LoggingOptions) else None
        log_request, log_response = create_async_logging_hooks(options)
        request_hooks.append(log_request)
        response_hooks.append(log_response)

    if response_status:
        options = response_status if isinstance(response_status, ResponseStatusOptions) else None
        response_hooks.append(create_async_response_status_hook(options))

    return {
        "request": request_hooks,
        "response": response_hooks,
    }
