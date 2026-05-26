from __future__ import annotations

from multimedia_scraper.core.config.dto.secrets import (
    SecretStr,
)


def resolve_secret(
    value: str,
) -> SecretStr:
    return SecretStr(value)