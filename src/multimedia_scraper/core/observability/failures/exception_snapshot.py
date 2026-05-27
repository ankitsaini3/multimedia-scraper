# src/multimedia_scraper/core/observability/failures/exception_snapshot.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExceptionSnapshot:
    """
    Immutable structured exception snapshot.

    MUST remain:
    - serialization-safe
    - replay-safe
    - secret-safe
    """

    exception_type: str

    message: str

    module: str

    qualified_name: str

    is_retryable: bool

    causal_chain_depth: int
