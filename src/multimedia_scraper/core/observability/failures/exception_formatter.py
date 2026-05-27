# src/multimedia_scraper/core/observability/failures/exception_formatter.py

from __future__ import annotations

from multimedia_scraper.core.observability.failures.exception_chain import (
    iter_exception_chain,
)
from multimedia_scraper.core.observability.failures.exception_snapshot import (
    ExceptionSnapshot,
)
from multimedia_scraper.core.observability.security.secret_filter import (
    filter_secrets,
)


def format_exception(
    exception: BaseException,
) -> ExceptionSnapshot:
    """
    Produce deterministic structured exception snapshot.

    Guarantees:
    - secret-safe formatting
    - deterministic causal extraction
    - serialization-safe output
    """

    chain_depth = sum(
        1
        for _ in iter_exception_chain(
            exception,
        )
    )

    exception_type = type(
        exception,
    )

    message = filter_secrets(
        str(exception),
    )

    return ExceptionSnapshot(
        exception_type=(exception_type.__name__),
        message=message,
        module=(exception_type.__module__),
        qualified_name=(f"{exception_type.__module__}.{exception_type.__qualname__}"),
        is_retryable=False,
        causal_chain_depth=(chain_depth),
    )
