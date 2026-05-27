# src/multimedia_scraper/core/observability/bootstrap/bootstrap_diagnostics.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BootstrapPhaseDiagnostic:
    """
    Immutable startup phase diagnostic snapshot.
    """

    phase: str

    started_at_utc: datetime

    completed_at_utc: datetime | None

    success: bool

    failure_type: str | None

    failure_message: str | None
