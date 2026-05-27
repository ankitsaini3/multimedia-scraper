# src/multimedia_scraper/core/observability/failures/exception_chain.py

from __future__ import annotations

from collections.abc import Iterator


def iter_exception_chain(
    exception: BaseException,
) -> Iterator[BaseException]:
    """
    Deterministically iterate causal exception chain.
    """

    current: BaseException | None = exception

    while current is not None:
        yield current

        if current.__cause__ is not None:
            current = current.__cause__

            continue

        current = current.__context__
