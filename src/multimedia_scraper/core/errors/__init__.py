# src/multimedia_scraper/core/errors/__init__.py

from multimedia_scraper.core.errors.base import (
    ConfigurationError as ConfigurationError,
    DomainError as DomainError,
    InfrastructureError as InfrastructureError,
    IntegrationError as IntegrationError,
    MultimediaScraperError as MultimediaScraperError,
    RuntimeSystemError as RuntimeSystemError,
    UserInputError as UserInputError,
)
from multimedia_scraper.core.errors.concurrency import (
    AsyncBoundaryViolationError as AsyncBoundaryViolationError,
    ConcurrencyError as ConcurrencyError,
    ConcurrencyLimitExceededError as ConcurrencyLimitExceededError,
    DeadlockRiskError as DeadlockRiskError,
    EventLoopBlockedError as EventLoopBlockedError,
    QueueOverflowError as QueueOverflowError,
    TaskOwnershipError as TaskOwnershipError,
)
from multimedia_scraper.core.errors.configuration import (
    ConfigurationOverrideError as ConfigurationOverrideError,
    ConfigurationResolutionError as ConfigurationResolutionError,
    ConfigurationValidationError as ConfigurationValidationError,
    FrozenConfigurationMutationError as FrozenConfigurationMutationError,
    MissingConfigurationError as MissingConfigurationError,
)
from multimedia_scraper.core.errors.events import (
    EventBackpressureError as EventBackpressureError,
    EventDispatchError as EventDispatchError,
    EventHandlerError as EventHandlerError,
    EventOrderingError as EventOrderingError,
    EventSubscriptionError as EventSubscriptionError,
    EventSystemError as EventSystemError,
)
from multimedia_scraper.core.errors.network import (
    ConnectionFailureError as ConnectionFailureError,
    NetworkError as NetworkError,
    RequestTimeoutError as RequestTimeoutError,
    ResponseValidationError as ResponseValidationError,
    SSRFProtectionError as SSRFProtectionError,
)
from multimedia_scraper.core.errors.observability import (
    CorrelationPropagationError as CorrelationPropagationError,
    ObservabilityError as ObservabilityError,
    RedactionFailureError as RedactionFailureError,
    TelemetryBackpressureError as TelemetryBackpressureError,
    TelemetryFlushError as TelemetryFlushError,
    TelemetrySerializationError as TelemetrySerializationError,
    TelemetryValidationError as TelemetryValidationError,
)
from multimedia_scraper.core.errors.plugins import (
    PluginCapabilityError as PluginCapabilityError,
    PluginCompatibilityError as PluginCompatibilityError,
    PluginContractViolationError as PluginContractViolationError,
    PluginError as PluginError,
    PluginExecutionError as PluginExecutionError,
    PluginInitializationError as PluginInitializationError,
)
from multimedia_scraper.core.errors.resources import (
    ResourceCleanupError as ResourceCleanupError,
    ResourceError as ResourceError,
    ResourceExhaustedError as ResourceExhaustedError,
    ResourceInitializationError as ResourceInitializationError,
    ResourceLeakError as ResourceLeakError,
    ResourceOwnershipError as ResourceOwnershipError,
)
from multimedia_scraper.core.errors.runtime import (
    RuntimeBootstrapError as RuntimeBootstrapError,
    RuntimeCancellationError as RuntimeCancellationError,
    RuntimeHealthError as RuntimeHealthError,
    RuntimeInvariantViolationError as RuntimeInvariantViolationError,
    RuntimeShutdownError as RuntimeShutdownError,
    RuntimeStateError as RuntimeStateError,
)
from multimedia_scraper.core.errors.security import (
    CapabilityDeniedError as CapabilityDeniedError,
    PathTraversalError as PathTraversalError,
    PluginIsolationError as PluginIsolationError,
    SandboxViolationError as SandboxViolationError,
    SecretExposureError as SecretExposureError,
    SecurityBoundaryError as SecurityBoundaryError,
    UnsafeSubprocessError as UnsafeSubprocessError,
)
from multimedia_scraper.core.errors.serialization import (
    CanonicalEncodingError as CanonicalEncodingError,
    DeserializationError as DeserializationError,
    DTOCompatibilityError as DTOCompatibilityError,
    DTOValidationError as DTOValidationError,
    SchemaMigrationError as SchemaMigrationError,
    SerializationError as SerializationError,
)
from multimedia_scraper.core.errors.subprocess import (
    SubprocessError as SubprocessError,
    SubprocessLaunchError as SubprocessLaunchError,
    SubprocessTerminationError as SubprocessTerminationError,
    SubprocessTimeoutError as SubprocessTimeoutError,
    UnsupportedExecutableError as UnsupportedExecutableError,
)
from multimedia_scraper.core.errors.supervision import (
    ChildTaskEscapeError as ChildTaskEscapeError,
    OrphanTaskError as OrphanTaskError,
    RestartPolicyViolationError as RestartPolicyViolationError,
    SupervisionError as SupervisionError,
    SupervisorCorruptionError as SupervisorCorruptionError,
    TaskSupervisionError as TaskSupervisionError,
)
