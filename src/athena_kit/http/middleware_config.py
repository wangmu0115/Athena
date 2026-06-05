"""HTTP middleware configuration models.

This module defines the typed configuration models used by the HTTP middleware pipeline.

It contains three layers of configuration:
    1. Options: Middleware-specific configuration, e.g. `RetryOptions`, `LoggingOptions`, etc.
    2. Extensions: Per-request override configuration provided by the caller.
    3. RequestContext: The fully resolved runtime configuration created by merging
       client-level defaults with per-request extensions.

Typical flow:
    AsyncHttpClient default options
        + per-request Extensions
        ->
    RequestContext
        ->
    Middleware execution

Design principles:
    1. Declarative configuration: options describe "what" behavior is desired, not "how" it is executed.
    2. Layered override: request-level options override client defaults.
    3. Typed interface: callers use strongly typed configuration objects instead of raw dictionaries.
    4. Loose coupling: middlewares depend only on resolved options from RequestContext, not on raw input dictionaries.
    5. Extensibility: each middleware should define its own Options class.

Note:
    RequestContext should be treated as read-only after creation. It should contain runtime configuration only,
    not transient execution state such as responses, exceptions, or timing data.
"""

import logging
import uuid
from collections.abc import Callable
from dataclasses import dataclass, fields, replace
from typing import Self


@dataclass(slots=True)
class BaseOptions:
    def with_overrides(self, override: Self | None) -> Self:
        if override is None:
            return replace(self)

        return replace(
            self,
            **{
                f.name: getattr(override, f.name) 
                for f in fields(override)
                if getattr(override, f.name) is not None
            },
        )  # fmt: off


@dataclass(slots=True)
class RetryOptions(BaseOptions):
    """HTTP request retry options.

    Attributes:
        enabled: Whether retry is enabled.
        retries: Maximum retry attempts after the initial request.
        retry_backoff: Base exponential backoff delay in seconds.
        retry_jitter: Maximum random jitter added to the backoff delay in seconds.
        retry_methods: HTTP methods eligible for retry, such as `{"GET", "PUT"}`.
        retry_status_codes: HTTP status codes that trigger retry.
        respect_retry_after: Whether to respect the `Retry-After` response header.
    """

    enabled: bool = True
    retries: int | None = None
    retry_backoff: float | None = None
    retry_jitter: float | None = None
    retry_methods: set[str] | None = None
    retry_status_codes: set[int] | None = None
    respect_retry_after: bool | None = None

    @classmethod
    def default(cls) -> Self:
        return cls(
            enabled=True,
            retries=2,
            retry_backoff=0.2,
            retry_jitter=0.1,
            retry_methods={"GET", "HEAD", "PUT", "DELETE", "OPTIONS", "TRACE"},
            retry_status_codes={408, 429, 500, 502, 503, 504},
            respect_retry_after=True,
        )


@dataclass(slots=True)
class LoggingOptions(BaseOptions):
    """HTTP request logging options.

    Attributes:
        enabled: Whether request logging is enabled.
        level: Log level, such as `logging.INFO` or `logging.DEBUG`.
        logger: Custom `logging.Logger` instance for the request.
    """

    enabled: bool = True
    level: int | None = None
    logger: logging.Logger | None = None

    @classmethod
    def default(cls, logger: logging.Logger | None = None) -> Self:
        return cls(
            enabled=True,
            level=logging.INFO,
            logger=logger,
        )


@dataclass(slots=True)
class RequestIDOptions(BaseOptions):
    """HTTP request ID injection options.

    Attributes:
        enabled: Whether request ID injection is enabled.
        header_name: Header name used to carry the request ID.
        id_factory: Callable used to generate request IDs.
    """

    enabled: bool = True
    header_name: str | None = None
    id_factory: Callable[[], str] | None = None

    @classmethod
    def default(cls) -> Self:
        return cls(
            enabled=True,
            header_name="X-Request-ID",
            id_factory=lambda: str(uuid.uuid4()),
        )


@dataclass(slots=True)
class Extensions:
    """Per-request middleware option overrides."""

    retry: RetryOptions | None = None
    logging: LoggingOptions | None = None
    request_id: RequestIDOptions | None = None


@dataclass(slots=True)
class RequestContext:
    """Resolved runtime request context consumed by middlewares."""

    retry: RetryOptions
    logging: LoggingOptions
    request_id: RequestIDOptions
