from __future__ import annotations

from multimedia_scraper.core.config.sources.env import (
    EnvironmentConfigSourceProvider,
)


def test_environment_provider_reads_only_explicit_keys(
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

    provider = (
        EnvironmentConfigSourceProvider()
    )

    source = provider.load()

    assert (
        source.payload["logging.level"]
        == "DEBUG"
    )

    assert (
        "UNRELATED_SECRET"
        not in source.payload
    )


def test_environment_provider_is_deterministic(
    monkeypatch,
) -> None:

    monkeypatch.setenv(
        "MULTIMEDIA_SCRAPER_LOG_LEVEL",
        "INFO",
    )

    provider = (
        EnvironmentConfigSourceProvider()
    )

    source_1 = provider.load()

    source_2 = provider.load()

    assert source_1 == source_2