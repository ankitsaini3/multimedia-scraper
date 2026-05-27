from multimedia_scraper.core.config.dto.secrets import (
    SecretStr,
)


def test_secret_repr_is_redacted() -> None:

    secret = SecretStr("super-secret")

    assert "super-secret" not in repr(secret)
    assert "super-secret" not in str(secret)

    assert "********" in repr(secret)
