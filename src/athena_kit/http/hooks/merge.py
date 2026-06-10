from athena_kit.http.hooks.logging import LoggingOptions, create_async_logging_hooks, create_logging_hooks
from athena_kit.http.hooks.raise_for_status import (
    RaiseForStatusOptions,
    create_async_raise_for_status_hook,
    create_raise_for_status_hook,
)
from athena_kit.http.hooks.request_id import RequestIDOptions, create_async_request_id_hook, create_request_id_hook
from athena_kit.http.hooks.types import (
    AsyncEventHooks,
    AsyncRequestHook,
    AsyncResponseHook,
    EventHooks,
    RequestHook,
    ResponseHook,
)


def merge_event_hooks(
    event_hooks: EventHooks | None = None,
    *,
    request_id: RequestIDOptions | None = None,
    logging_options: LoggingOptions | None = None,
    raise_for_status: bool | RaiseForStatusOptions = False,
) -> dict[str, list[RequestHook | ResponseHook]]:
    """Merge Athena's optional sync hooks with caller-provided HTTPX hooks."""
    request_hooks = list((event_hooks or {}).get("request", []))
    response_hooks = list((event_hooks or {}).get("response", []))

    if request_id is not None:
        request_hooks.append(create_request_id_hook(request_id))

    if logging_options is not None:
        log_request, log_response = create_logging_hooks(logging_options)
        request_hooks.append(log_request)
        response_hooks.append(log_response)

    if raise_for_status:
        options = raise_for_status if isinstance(raise_for_status, RaiseForStatusOptions) else None
        response_hooks.append(create_raise_for_status_hook(options))

    return {
        "request": request_hooks,
        "response": response_hooks,
    }


def merge_async_event_hooks(
    event_hooks: AsyncEventHooks | None = None,
    *,
    request_id: RequestIDOptions | None = None,
    logging_options: LoggingOptions | None = None,
    raise_for_status: bool | RaiseForStatusOptions = False,
) -> dict[str, list[AsyncRequestHook | AsyncResponseHook]]:
    """Merge Athena's optional async hooks with caller-provided HTTPX hooks."""
    request_hooks = list((event_hooks or {}).get("request", []))
    response_hooks = list((event_hooks or {}).get("response", []))

    if request_id is not None:
        request_hooks.append(create_async_request_id_hook(request_id))

    if logging_options is not None:
        log_request, log_response = create_async_logging_hooks(logging_options)
        request_hooks.append(log_request)
        response_hooks.append(log_response)

    if raise_for_status:
        options = raise_for_status if isinstance(raise_for_status, RaiseForStatusOptions) else None
        response_hooks.append(create_async_raise_for_status_hook(options))

    return {
        "request": request_hooks,
        "response": response_hooks,
    }
