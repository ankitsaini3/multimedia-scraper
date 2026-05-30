from __future__ import annotations


class RuntimeCancellationError(Exception):
    """
    Cooperative structured runtime cancellation.
    """


class CancellationScopeClosedError(RuntimeError):
    """
    Raised when attempting to create children
    from a closed cancellation scope.
    """


class SupervisorClosedError(RuntimeError):
    """
    Raised when spawning tasks into a closed supervisor.
    """


class DuplicateRuntimeRegistrationError(
    RuntimeError,
):
    """
    Raised when runtime registration already exists.
    """
