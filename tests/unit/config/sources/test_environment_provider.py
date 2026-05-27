from multimedia_scraper.core.config.sources.env import (
    EnvironmentConfigSourceProvider,
)


def test_environment_provider_reads_explicit_keys_only(
    monkeypatch,
) -> None:

    monkeypatch.setenv(
        "MULTIMEDIA_SCRAPER_LOG_LEVEL",
        "DEBUG",
    )

    monkeypatch.setenv(
        "UNRELATED_SECRET",
        "SHOULD_NOT_APPEAR",
    )

    provider = EnvironmentConfigSourceProvider()

    source = provider.load()

    assert source.payload["logging.level"] == "DEBUG"

    assert "UNRELATED_SECRET" not in source.payload
