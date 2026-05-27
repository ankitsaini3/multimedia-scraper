from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .models import ConfigSource


def merge_sources(
    sources: Iterable[ConfigSource],
) -> dict[str, Any]:

    merged: dict[str, Any] = {}

    ordered = sorted(
        sources,
        key=lambda s: (
            s.precedence,
            s.source_name,
        ),
    )

    for source in ordered:
        for key in sorted(source.payload):
            merged[key] = source.payload[key]

    return merged
