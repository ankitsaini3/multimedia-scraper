# src/multimedia_scraper/core/observability/security/secret_patterns.py

from __future__ import annotations

import re
from typing import Final

SECRET_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(
        r"(?i)bearer\s+[a-z0-9\-._~+/]+=*",
    ),
    re.compile(
        r"(?i)api[_\-]?key\s*[:=]\s*\S+",
    ),
    re.compile(
        r"(?i)token\s*[:=]\s*\S+",
    ),
    re.compile(
        r"(?i)password\s*[:=]\s*\S+",
    ),
    re.compile(
        r"(?i)secret\s*[:=]\s*\S+",
    ),
    re.compile(
        r"(?i)authorization\s*[:=]\s*\S+",
    ),
)
