import asyncio
import logging
import random
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from typing import Any

import httpx

from athena_kit.http import RequestHandler, RetryOptions

logger = logging.getLogger(__name__)


class RetryMiddleware:
    """HTTP retry middleware.

    This middleware retries failed HTTP requests using an idempotency-aware strategy.
    By default, only safe or idempotent HTTP methods are retried.

    Note:
        This middleware must be installed closer to the transport layer than any exception-handling middleware
        to ensure retries are performed prior to error handling.
    """

    __middleware_name__ = "RetryMiddleware"

    def __init__(self):
        self._default_options = RetryOptions.default()

    def __call__(self, next_handler: RequestHandler) -> RequestHandler:
        async def wrapper(method: str, url: str, **kwargs: Any) -> httpx.Response:
            options: RetryOptions = kwargs["context"].retry

            retries = options.retries if options.retries is not None else self._default_options.retries
            if not options.enabled or retries <= 0:
                return await next_handler(method, url, **kwargs)

            retry_methods = options.retry_methods or self._default_options.retry_methods
            retry_status_codes = options.retry_status_codes or self._default_options.retry_status_codes
            method = method.upper()
            for attempt in range(retries + 1):
                try:
                    response = await next_handler(method, url, **kwargs)

                    should_retry = method in retry_methods \
                                    and response.status_code in retry_status_codes \
                                    and attempt < retries  # fmt: off
                    if not should_retry:
                        return response

                    delay = self._get_retry_delay(options, attempt, response)
                    logger.warning(
                        "HTTP retry scheduled: method=%s, url=%s, status_code=%d, attempt=%d, retries=%d, delay=%.6f",
                        method, url, response.status_code, 
                        attempt, retries, delay,
                    )  # fmt: off
                    await asyncio.sleep(delay if delay > 0.0 else 0.005)
                except (httpx.TimeoutException, httpx.RequestError) as exc:
                    if method not in retry_methods or attempt >= retries:
                        raise
                    delay = self._get_backoff_delay(attempt, options)
                    logger.warning(
                        "HTTP retry scheduled: method=%s, url=%s, attempt=%d, retries=%d, delay=%.6f, reason=%s",
                        method, url,
                        attempt, retries, delay, type(exc).__name__,
                    )  # fmt: off
                    await asyncio.sleep(delay if delay > 0.0 else 0.005)

        return wrapper

    def _get_retry_delay(self, options: RetryOptions, attempt: int, response: httpx.Response) -> float:
        respect_retry_after = options.respect_retry_after \
                                if options.respect_retry_after is not None \
                                else self._default_options.respect_retry_after  # fmt: off
        if respect_retry_after:
            retry_after = self._parse_retry_after(response.headers.get("Retry-After"))
            if retry_after is not None:
                return retry_after

        return self._get_backoff_delay(attempt, options)

    def _get_backoff_delay(self, attempt: int, options: RetryOptions) -> float:
        retry_backoff = options.retry_backoff or self._default_options.retry_backoff
        retry_jitter = options.retry_jitter or self._default_options.retry_jitter

        delay = retry_backoff * (2**attempt)
        if retry_jitter > 0:
            delay += random.uniform(0, retry_jitter)

        return delay

    @staticmethod
    def _parse_retry_after(value: str | None) -> float | None:
        if not value:
            return None

        if value.isdigit():
            return max(float(value), 0.0)

        try:
            retry_at = parsedate_to_datetime(value)

            if retry_at.tzinfo is None:
                retry_at = retry_at.replace(tzinfo=UTC)

            delay = (retry_at - datetime.now(UTC)).total_seconds()
            return max(0.0, delay)
        except (TypeError, ValueError):
            return None
