# Failure Semantics

Status:

```text id="fail7m2"
STABLE CONTRACT DRAFT
```

Scope:

```text id="fail1x9"
Phase 1 — Core Runtime Foundations
```

This specification defines:

* typed exception hierarchy
* failure ownership boundaries
* infrastructure translation rules
* failure propagation semantics
* runtime failure classification
* observability guarantees
* cancellation failure behavior
* plugin failure semantics
* supervision failure semantics
* public exception contracts

This document is:

```text id="fail4k0"
architecturally authoritative
```

All implementations must conform to these semantics.

---

# 1. Failure Philosophy

The system must:

```text id="fail0w5"
fail predictably
```

Failures are considered:

* normal runtime realities
* observable runtime signals
* typed architectural boundaries

The system MUST avoid:

* silent corruption
* hidden failure propagation
* infrastructure leakage
* ambiguous runtime state

---

# 2. Foundational Failure Rule

All failures crossing architectural boundaries MUST be:

```text id="fail9r1"
typed and translated
```

Raw infrastructure exceptions MUST NOT leak across public runtime contracts.

---

# 3. Failure Ownership Model

# Runtime Lifecycle Owns

* startup failure coordination
* shutdown failure coordination
* fatal runtime state transitions

---

# Supervisor Owns

* task failure observation
* task failure isolation
* cancellation propagation failures

---

# EventBus Owns

* handler failure isolation
* dispatch failure observability

---

# Plugins Own

* plugin-local failure handling
* provider-specific infrastructure translation

---

# Providers Own

* infrastructure translation at provider boundaries

---

# 4. Exception Hierarchy

Canonical runtime hierarchy:

```text id="faild7k8"
MultimediaScraperError
├── RuntimeSystemError
├── InfrastructureError
├── IntegrationError
├── DomainError
├── UserInputError
└── ConfigurationError
```

This hierarchy is stable architecture.

---

# 5. Root Exception Contract

Canonical root contract:

```python id="fail_evt1"
class MultimediaScraperError(Exception):
    \"\"\"Root runtime exception.\"\"\"
```

All public runtime exceptions MUST derive from this root.

---

# 6. RuntimeSystemError Semantics

Purpose:

```text id="failx3u6"
runtime coordination failure
```

Examples:

* supervision corruption
* lifecycle corruption
* runtime invariant violation
* event system corruption

---

# Canonical Contract

```python id="fail_evt2"
class RuntimeSystemError(
    MultimediaScraperError,
):
    ...
```

---

# 7. InfrastructureError Semantics

Purpose:

```text id="failf5l2"
infrastructure interaction failure
```

Examples:

* network failure
* filesystem failure
* subprocess failure
* serialization failure

Infrastructure errors are:

```text id="failp8j4"
boundary translation targets
```

---

# Canonical Contract

```python id="fail_evt3"
class InfrastructureError(
    MultimediaScraperError,
):
    ...
```

---

# 8. IntegrationError Semantics

Purpose:

```text id="failq2n7"
external integration incompatibility
```

Examples:

* incompatible plugin
* unsupported provider contract
* API mismatch
* capability mismatch

---

# Canonical Contract

```python id="fail_evt4"
class IntegrationError(
    MultimediaScraperError,
):
    ...
```

---

# 9. DomainError Semantics

Purpose:

```text id="failt9k5"
domain-level semantic failure
```

Examples:

* invalid metadata
* unsupported media structure
* invalid extraction result
* malformed DTO state

---

# Canonical Contract

```python id="fail_evt5"
class DomainError(
    MultimediaScraperError,
):
    ...
```

---

# 10. UserInputError Semantics

Purpose:

```text id="failu4x1"
invalid user-provided input
```

Examples:

* invalid CLI arguments
* malformed URLs
* invalid configuration overrides

---

# Canonical Contract

```python id="fail_evt6"
class UserInputError(
    MultimediaScraperError,
):
    ...
```

---

# 11. ConfigurationError Semantics

Purpose:

```text id="failz7y3"
configuration validation failure
```

Examples:

* invalid config schema
* invalid override precedence
* unsupported runtime configuration

---

# Canonical Contract

```python id="fail_evt7"
class ConfigurationError(
    MultimediaScraperError,
):
    ...
```

---

# 12. Boundary Translation Rule

Infrastructure exceptions MUST NOT cross public contracts.

Mandatory translation:

```text id="faile6w9"
infrastructure exception
    -> typed runtime exception
```

---

# Canonical Translation Example

Forbidden:

```python id="fail_evt8"
raise aiohttp.ClientError(...)
```

across provider boundary.

Required:

```python id="fail_evt9"
try:
    ...
except aiohttp.ClientError as exc:
    raise InfrastructureError(
        \"network request failed\",
    ) from exc
```

---

# 13. Root Cause Preservation

Translation MUST preserve root causes.

Mandatory:

```python id="fail_evt10"
raise DomainError(...) from exc
```

Forbidden:

```python id="fail_evt11"
raise DomainError(...)
```

without cause chaining.

---

# 14. Failure Classification Semantics

Failures are classified into:

| Category              | Severity |
| --------------------- | -------- |
| configuration         | fatal    |
| lifecycle corruption  | critical |
| plugin initialization | isolated |
| handler failure       | degraded |
| cancellation timeout  | degraded |
| task corruption       | critical |

---

# 15. Fatal Failure Semantics

Fatal failures mean:

```text id="failn1r4"
runtime cannot safely continue
```

Fatal failures MUST:

* terminate startup
* initiate shutdown
* emit critical observability signals

---

# 16. Isolated Failure Semantics

Isolated failures MUST remain:

```text id="fails8p6"
contained within ownership boundary
```

Example:

* one plugin failure MUST NOT corrupt unrelated plugins

---

# 17. Degraded Failure Semantics

Degraded failures mean:

```text id="failv2j8"
runtime continues with reduced guarantees
```

Examples:

* logging sink failure
* event handler failure
* optional plugin failure

Degraded operation MUST remain observable.

---

# 18. Critical Failure Semantics

Critical failures indicate:

```text id="failw6m3"
runtime invariants may be compromised
```

Examples:

* supervision corruption
* lifecycle corruption
* cancellation corruption

Critical failures MAY force shutdown.

---

# 19. Runtime Invariant Semantics

Invariant violations are:

```text id="failx1n7"
RuntimeSystemError
```

Examples:

* illegal lifecycle transition
* orphan runtime task
* corrupted supervision ownership

Invariant violations are considered architecture failures.

---

# 20. Failure Observability Semantics

All failures MUST remain observable.

Silent failure is forbidden.

Required observability:

* structured logs
* correlation identifiers
* failure classification
* root-cause preservation

---

# 21. Structured Failure Logging

Failure logs MUST include:

* exception type
* ownership boundary
* correlation ID where available
* runtime state
* causal chain

---

# 22. Failure Propagation Rules

Failures propagate ONLY through:

* runtime lifecycle
* supervision boundaries
* typed event boundaries
* explicit API contracts

Arbitrary propagation is forbidden.

---

# 23. Cancellation Failure Semantics

Cancellation is NOT considered an error condition.

Cancellation MUST NOT:

* be logged as fatal
* corrupt runtime state
* bypass cleanup guarantees

---

# Cleanup Failure Semantics

Cleanup failures during cancellation:

* MUST remain observable
* MUST preserve root causes
* MUST NOT stop remaining cleanup

---

# 24. Supervision Failure Semantics

The supervisor owns:

* task failure observation
* task isolation
* escalation policy

Task failures MUST:

* remain observable
* remain isolated
* preserve runtime stability where possible

---

# Forbidden Supervision Behavior

Forbidden:

```text id="faily9r4"
silent task failure disappearance
```

---

# 25. Event Handler Failure Semantics

Handler failures MUST:

* remain isolated
* preserve root causes
* emit structured logs

Handler failure MUST NOT:

* crash publisher
* corrupt dispatch state
* stop unrelated handlers

---

# 26. Plugin Failure Semantics

Plugin failures are:

```text id="failz5t8"
plugin-scoped by default
```

Plugin failures MUST NOT:

* mutate runtime lifecycle
* corrupt unrelated plugins
* bypass runtime ownership

---

# Plugin Initialization Failure Rules

Initialization failure:

* prevents activation
* preserves runtime stability
* emits structured observability signals

---

# 27. Provider Failure Semantics

Providers MUST translate:

* network failures
* extraction library failures
* parsing failures
* serialization failures

before crossing provider boundaries.

---

# Forbidden Provider Leakage

Forbidden:

```python id="fail_evt12"
raise YtDlpError(...)
```

across provider contract.

Required:

```python id="fail_evt13"
raise StreamExtractionError(...) from exc
```

---

# 28. Configuration Failure Semantics

Invalid configuration MUST:

* fail immediately
* prevent runtime startup
* remain observable
* preserve validation context

Partial configuration startup is forbidden.

---

# 29. Lifecycle Failure Semantics

Startup failure:

```text id="faila2m9"
runtime unusable
```

Required behavior:

* rollback initialized services
* transition to STOPPED
* preserve diagnostics

---

# Shutdown Failure Semantics

Shutdown failures:

* MUST continue cleanup
* MUST preserve observability
* MUST avoid deadlock

---

# 30. Async Failure Semantics

Async task failures MUST NEVER disappear silently.

All supervised task failures MUST become observable through:

* supervision
* events
* structured logging

---

# Forbidden Async Failure Behavior

Forbidden:

```python id="fail_evt14"
asyncio.create_task(...)
```

without supervision ownership.

---

# 31. Retry Semantics

Retries are:

```text id="failb4r7"
explicit policy decisions
```

Retries MUST NOT occur implicitly across architectural boundaries.

---

# Allowed Retry Ownership

Retries MAY be owned by:

* supervision policies
* provider coordination layers
* application services

Retries MUST remain observable.

---

# 32. Timeout Failure Semantics

Timeouts are classified as:

```text id="failc6n2"
InfrastructureError
```

unless they violate runtime invariants.

Timeouts MUST:

* preserve cancellation semantics
* preserve cleanup guarantees
* remain observable

---

# 33. Failure Isolation Guarantees

Failure isolation is guaranteed across:

* plugins
* event handlers
* supervised tasks
* provider boundaries

Isolation prevents cascading corruption.

---

# 34. Illegal Failure Behaviors

Forbidden behaviors include:

---

## Silent Exception Suppression

Forbidden:

```python id="fail_evt15"
except Exception:
    pass
```

---

## Infrastructure Leakage

Forbidden:

```python id="fail_evt16"
raise aiohttp.ClientError(...)
```

across public boundaries.

---

## Root Cause Destruction

Forbidden:

```python id="fail_evt17"
raise RuntimeSystemError(...)
```

without `from exc`.

---

## Hidden Runtime Corruption

Forbidden:

```python id="fail_evt18"
ignore supervision corruption
```

---

## Fatal Cancellation Logging

Forbidden:

```python id="fail_evt19"
logger.critical(\"task cancelled\")
```

for cooperative cancellation.

---

# 35. Failure Testing Semantics

Tests MUST verify:

* boundary translation
* root-cause preservation
* failure isolation
* cancellation behavior
* lifecycle rollback
* supervision observability
* plugin isolation
* structured logging guarantees

---

# 36. Failure Stability Policy

The following are considered:

```text id="faild8v5"
FOUNDATIONAL STABLE FAILURE SEMANTICS
```

* exception hierarchy
* translation rules
* isolation guarantees
* propagation semantics
* lifecycle failure behavior
* cancellation semantics
* supervision failure ownership

Breaking changes require:

* ADR review
* migration analysis
* operational impact review
* compatibility evaluation

---

# 37. Final Failure Principle

```text id="faile1x7"
Failures are runtime facts,
not hidden implementation details.
```

The system must ensure failures remain:

* typed
* observable
* isolated
* structured
* cancellable
* lifecycle-compatible
* operationally diagnosable.
