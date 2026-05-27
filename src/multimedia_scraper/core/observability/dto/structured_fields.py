# src/multimedia_scraper/core/observability/dto/structured_fields.py

from __future__ import annotations

from collections.abc import Mapping
from typing import TypeAlias

StructuredPrimitive: TypeAlias = str | int | float | bool | None

StructuredValue: TypeAlias = (
    StructuredPrimitive
    | tuple["StructuredValue", ...]
    | Mapping[str, "StructuredValue"]
)

StructuredFields: TypeAlias = Mapping[str, StructuredValue]
