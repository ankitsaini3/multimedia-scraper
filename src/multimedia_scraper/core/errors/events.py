# src/multimedia_scraper/core/errors/events.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    RuntimeSystemError,
)


class EventSystemError(
    RuntimeSystemError,
):
    """
    Base event system failure.
    """


class EventDispatchError(
    EventSystemError,
):
    """
    Event dispatch coordination failure.
    """


class EventHandlerError(
    EventSystemError,
):
    """
    Event handler execution failure.
    """


class EventSubscriptionError(
    EventSystemError,
):
    """
    Invalid event subscription state.
    """


class EventOrderingError(
    EventSystemError,
):
    """
    Event ordering guarantee violation.
    """


class EventBackpressureError(
    EventSystemError,
):
    """
    Event system backpressure failure.
    """
