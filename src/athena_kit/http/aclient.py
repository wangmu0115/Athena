from typing import Any

import httpx
from athena_kit.http.hooks import (
    AsyncEventHooks,
    LoggingOptions,
    RequestIDOptions,
    ResponseStatusOptions,
    build_async_event_hooks,
)


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
        request_id: bool | RequestIDOptions = False,
        logging: bool | LoggingOptions = False,
        response_status: bool | ResponseStatusOptions = False,
        retries: int = 0,
        event_hooks: AsyncEventHooks | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        **kwargs: Any,
    ):
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
            event_hooks=build_async_event_hooks(
                event_hooks,
                request_id=request_id,
                logging=logging,
                response_status=response_status,
            ),
            transport=transport,
            **kwargs,
        )
