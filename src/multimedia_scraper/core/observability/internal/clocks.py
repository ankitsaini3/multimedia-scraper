from __future__ import annotations

import time
from datetime import datetime, timezone


def utc_now() -> datetime:
    """
    Canonical UTC wall-clock timestamp.

    Must remain timezone-aware.
    """

    return datetime.now(tz=timezone.utc)


def monotonic_time_ns() -> int:
    """
    Canonical monotonic runtime clock.

    Used for:
    - duration calculations
    - deterministic ordering
    - timeout semantics
    """

    return time.monotonic_ns()
