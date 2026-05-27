from __future__ import annotations

from multimedia_scraper.core.config.dto.secrets import (
    SecretStr,
)
from multimedia_scraper.core.config.exceptions import (
    ConfigurationValidationError,
)


def test_secret_repr_is_redacted() -> None:

    secret = SecretStr("super-secret")

    assert "super-secret" not in repr(secret)
    assert "super-secret" not in str(secret)

    assert "********" in repr(secret)


def test_secret_not_leaked_in_exception() -> None:

    secret = SecretStr("super-secret")

    try:
        raise ConfigurationValidationError(
            "validation failed",
        )
    except ConfigurationValidationError as exc:
        rendered = str(exc)

    assert "super-secret" not in rendered

    assert secret.reveal() == "super-secret"
