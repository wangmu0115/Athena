from typing import Any

import httpx
from athena_kit.http.hooks import AsyncEventHooks, LoggingOptions, RequestIDOptions, merge_async_event_hooks


class AsyncHttpClient(httpx.AsyncClient):
    """Thin `httpx.AsyncClient` subclass with optional Athena hooks.

    Change note:
        The old custom middleware pipeline has been removed. This class now
        relies on HTTPX's native client configuration, event hooks, auth,
        transports, timeouts, limits, and exception model.

    References:
        HTTPX Clients: https://www.python-httpx.org/advanced/clients/
        HTTPX Event Hooks: https://www.python-httpx.org/advanced/event-hooks/
        HTTPX Transports: https://www.python-httpx.org/advanced/transports/
    """

    def __init__(
        self,
        *args: Any,
        request_id: RequestIDOptions | bool = False,
        logging_options: LoggingOptions | bool = False,
        raise_for_status: bool = False,
        retries: int = 0,
        event_hooks: AsyncEventHooks | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        **kwargs: Any,
    ):
        resolved_request_id = RequestIDOptions() if request_id is True else request_id or None
        resolved_logging = LoggingOptions() if logging_options is True else logging_options or None

        if transport is None and retries > 0:
            # HTTPX's built-in retries are transport-level connection retries.
            # For status-code/backoff policies, prefer a dedicated package such
            # as tenacity at the integration layer.
            #
            # Reference:
            #   HTTPX Transports: https://www.python-httpx.org/advanced/transports/
            transport = httpx.AsyncHTTPTransport(retries=retries)

        super().__init__(
            *args,
            event_hooks=merge_async_event_hooks(
                event_hooks,
                request_id=resolved_request_id,
                logging_options=resolved_logging,
                raise_for_status=raise_for_status,
            ),
            transport=transport,
            **kwargs,
        )
