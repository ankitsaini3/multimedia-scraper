# Lifecycle Semantics

Status:

```text id="x4m2ke"
STABLE CONTRACT DRAFT
```

Scope:

```text id="0uyrxt"
Phase 1 — Core Runtime Foundations
```

This document defines:

* runtime lifecycle semantics
* startup/shutdown guarantees
* state transition rules
* ownership semantics
* initialization ordering
* cancellation semantics
* resource lifetime rules
* plugin lifecycle semantics
* supervision lifecycle semantics

This specification is:

```text id="1qf3zv"
architecturally authoritative
```

All implementations must conform to these semantics.

---

# 1. Lifecycle Philosophy

The runtime lifecycle exists to guarantee:

* deterministic startup
* deterministic shutdown
* bounded resource lifetime
* cancellation safety
* fault containment
* runtime observability
* plugin isolation
* async coordination correctness

The lifecycle system is the:

```text id="fdz7az"
authoritative owner of runtime existence
```

No subsystem may bypass it.

---

# 2. Foundational Lifecycle Rule

The runtime lifecycle is:

```text id="nnjlwm"
single-owner coordinated
```

This means:

* one authoritative startup sequence
* one authoritative shutdown sequence
* one authoritative cancellation root
* one authoritative runtime state machine

---

# 3. Runtime Lifecycle Ownership

The runtime lifecycle owns:

* startup coordination
* shutdown coordination
* service activation
* service deactivation
* cancellation propagation
* runtime state transitions
* resource release ordering
* plugin activation/deactivation
* supervised task lifetime

The lifecycle system does NOT own:

* business workflows
* media operations
* provider logic
* playback orchestration

---

# 4. Runtime State Machine

Canonical runtime state machine:

```text id="v4jlwm"
INITIALIZED
    -> STARTING
    -> RUNNING
    -> SHUTTING_DOWN
    -> STOPPED
```

This state machine is stable architecture.

---

# 5. Runtime State Definitions

# INITIALIZED

Meaning:

```text id="u4yjlwm"
runtime object constructed
```

Guarantees:

* configuration not yet activated
* services not operational
* no supervised tasks running
* plugins inactive

Allowed operations:

* dependency registration
* configuration loading
* service wiring

Forbidden operations:

* event publishing
* task spawning
* plugin activation

---

# STARTING

Meaning:

```text id="jlwmf7"
runtime startup sequence in progress
```

Guarantees:

* startup ordering enforced
* services partially available
* cancellation root established

Forbidden:

* concurrent startup
* plugin execution before activation
* runtime mutation outside startup owner

---

# RUNNING

Meaning:

```text id="3jlwm6"
runtime operational
```

Guarantees:

* all required services active
* event bus operational
* supervision operational
* plugins activated
* runtime context stable
* dependency container frozen

Allowed:

* supervised task spawning
* event publishing
* plugin interaction
* runtime coordination

---

# SHUTTING_DOWN

Meaning:

```text id="2jlwm5"
runtime teardown initiated
```

Guarantees:

* cancellation propagation active
* no new long-lived tasks accepted
* shutdown ordering enforced

Forbidden:

* plugin activation
* runtime service registration
* container mutation

---

# STOPPED

Meaning:

```text id="1jlwm4"
runtime fully terminated
```

Guarantees:

* all supervised tasks terminated
* plugins deactivated
* resources released
* logging flushed

Forbidden:

* task spawning
* event publishing
* runtime mutation

---

# 6. Legal State Transitions

Allowed transitions ONLY:

```text id="zjlwm1"
INITIALIZED -> STARTING
STARTING -> RUNNING
STARTING -> SHUTTING_DOWN
RUNNING -> SHUTTING_DOWN
SHUTTING_DOWN -> STOPPED
```

All other transitions are invalid.

---

# 7. Startup Semantics

Startup is:

```text id="qjlwm2"
deterministic and ordered
```

Startup ordering is part of stable architecture.

---

# 8. Canonical Startup Sequence

Frozen startup order:

```text id="wjlwm8"
configuration
    -> logging
    -> dependency container
    -> event bus
    -> supervision
    -> plugin registry
    -> plugin activation
    -> runtime RUNNING state
```

This ordering MUST remain stable.

---

# 9. Startup Ownership Rules

Startup is owned exclusively by:

```text id="ejlwm9"
RuntimeContext.startup()
```

No subsystem may independently initiate runtime activation.

---

# 10. Startup Concurrency Rules

Rules:

* startup() MUST NOT execute concurrently
* startup() MUST be idempotent-safe
* startup() MUST be cancellation-safe
* startup() MUST serialize state transitions

Concurrent startup attempts are forbidden.

---

# 11. Startup Failure Semantics

Startup failures are:

```text id="7jlwm3"
fatal runtime failures
```

If startup fails:

* runtime MUST NOT enter RUNNING
* partial initialization MUST rollback
* initialized resources MUST cleanup
* failures MUST preserve root causes
* failures MUST emit structured logs

---

# 12. Partial Startup Rollback

If startup fails mid-sequence:

```text id="5jlwm7"
already-started services MUST shutdown in reverse order
```

Example:

```text id="9jlwm5"
logging initialized
event bus initialized
supervision initialization fails
```

Required rollback:

```text id="0jlwm2"
shutdown event bus
flush logging
transition to STOPPED
```

---

# 13. Shutdown Semantics

Shutdown is:

```text id="ljlwm6"
graceful by default
```

The runtime MUST attempt orderly teardown before forced termination.

---

# 14. Canonical Shutdown Sequence

Frozen shutdown ordering:

```text id="mjlwm5"
stop accepting work
    -> propagate cancellation
    -> stop supervised tasks
    -> deactivate plugins
    -> drain event system
    -> flush logging
    -> release runtime resources
    -> STOPPED
```

This ordering is stable architecture.

---

# 15. Shutdown Ownership

Shutdown is owned exclusively by:

```text id="jjlwm8"
RuntimeContext.shutdown()
```

Subsystems MUST NOT independently terminate runtime.

---

# 16. Shutdown Guarantees

Shutdown MUST:

* propagate cancellation globally
* stop supervised tasks
* deactivate plugins
* flush structured logs
* release runtime-owned resources

Shutdown MUST NOT:

* abandon supervised tasks
* leak runtime resources
* silently suppress failures

---

# 17. Shutdown Idempotency

shutdown() MUST be:

```text id="kjlwm4"
idempotent
```

Multiple shutdown calls MUST NOT:

* corrupt runtime state
* double-release resources
* restart shutdown sequencing

---

# 18. Forced Shutdown Semantics

Forced shutdown MAY occur if:

* graceful shutdown timeout exceeded
* runtime corruption detected
* fatal supervision failure occurs

Forced shutdown MUST:

* emit structured critical logs
* preserve diagnostics where possible

---

# 19. Cancellation Semantics

Cancellation is:

```text id="njlwm1"
hierarchical and downward-propagating
```

The runtime owns the global cancellation root.

---

# 20. Cancellation Ownership

Only runtime lifecycle and supervision may own:

* cancellation propagation
* task cancellation coordination
* shutdown cancellation boundaries

---

# 21. Cancellation Guarantees

Cancellation MUST:

* propagate downward
* preserve cleanup execution
* remain observable
* remain structured

Cancellation MUST NOT:

* silently disappear
* bypass supervision
* orphan tasks

---

# 22. Long-Lived Task Semantics

All long-lived tasks MUST be:

```text id="pjlwm3"
runtime-supervised
```

Detached runtime tasks are forbidden.

---

# 23. Task Lifetime Rules

Tasks:

* MUST NOT outlive runtime
* MUST participate in cancellation
* MUST support graceful cleanup

Task ownership belongs to:

```text id="tjlwm0"
Supervisor
```

---

# 24. Event System Lifecycle Semantics

The event system lifecycle is runtime-scoped.

The event bus exists ONLY while runtime is operational.

---

# Event Bus Startup Guarantees

Before RUNNING:

* subscriptions operational
* dispatch operational
* runtime event hooks active

---

# Event Bus Shutdown Guarantees

During shutdown:

* new events MAY be rejected
* pending handlers MAY drain
* handler failures MUST log
* event dispatch MUST terminate cleanly

---

# 25. Plugin Lifecycle Semantics

Plugins are:

```text id="ujlwm7"
runtime-managed components
```

Plugins MUST NOT own runtime lifecycle.

---

# 26. Plugin Lifecycle State Machine

Canonical plugin lifecycle:

```text id="vjlwm9"
DISCOVERED
    -> VALIDATED
    -> REGISTERED
    -> INITIALIZED
    -> ACTIVE
    -> DEACTIVATED
    -> UNLOADED
```

---

# 27. Plugin Activation Semantics

Plugin activation occurs ONLY after:

* runtime services active
* event bus active
* supervision active
* runtime context stable

---

# 28. Plugin Failure Semantics

Plugin failures MUST:

* preserve root causes
* emit structured logs
* remain isolated
* avoid corrupting runtime lifecycle

Plugin initialization failure MUST NOT crash unrelated plugins.

---

# 29. Dependency Container Lifecycle

The dependency container lifecycle is runtime-scoped.

---

# Container Startup Rules

Before RUNNING:

* services registered
* dependencies resolved
* container frozen

---

# Container Freeze Rule

After RUNNING:

```text id="wjlwm3"
runtime dependency graph becomes immutable
```

Dynamic mutation is forbidden.

---

# 30. RuntimeContext Lifecycle Guarantees

RuntimeContext guarantees:

---

## After startup()

Guaranteed operational:

* config
* logger
* event bus
* supervisor
* plugin registry
* dependency container

---

## After shutdown()

Guaranteed terminated:

* supervised tasks
* plugin activity
* runtime event dispatch
* runtime-owned resources

---

# 31. Resource Ownership Semantics

Every runtime resource MUST have:

```text id="xjlwm4"
exactly one lifecycle owner
```

Examples:

| Resource            | Owner          |
| ------------------- | -------------- |
| runtime tasks       | Supervisor     |
| event subscriptions | EventBus       |
| plugins             | PluginRegistry |
| config state        | RuntimeContext |
| logging pipeline    | RuntimeLogger  |

Shared ownership is forbidden.

---

# 32. Resource Release Rules

Resource release MUST occur:

```text id="yjlwm8"
in reverse initialization order
```

This prevents dependency invalidation during teardown.

---

# 33. Runtime Observability Semantics

Lifecycle transitions MUST emit structured observability signals.

Required observable events:

* runtime starting
* runtime running
* runtime shutting down
* runtime stopped
* task failures
* plugin failures
* cancellation propagation

---

# 34. Lifecycle Failure Classification

Lifecycle failures are classified as:

| Type                      | Severity |
| ------------------------- | -------- |
| startup failure           | fatal    |
| shutdown cleanup failure  | degraded |
| plugin activation failure | isolated |
| supervision failure       | critical |
| event dispatch failure    | degraded |

---

# 35. Illegal Lifecycle Behavior

Forbidden behaviors include:

---

## Runtime Mutation During Shutdown

Forbidden:

```python id="zjlwm0"
container.register(...)
```

during SHUTTING_DOWN.

---

## Detached Tasks

Forbidden:

```python id="1jlwm9"
asyncio.create_task(...)
```

outside supervision ownership.

---

## Plugin-Owned Lifecycle

Forbidden:

```python id="2jlwm1"
plugin.shutdown_runtime()
```

---

## Concurrent Startup

Forbidden:

```python id="3jlwm8"
await asyncio.gather(
    runtime.startup(),
    runtime.startup(),
)
```

---

# 36. Testing Lifecycle Semantics

Tests MUST verify:

* legal state transitions
* cancellation propagation
* shutdown ordering
* startup rollback behavior
* task cleanup guarantees
* plugin isolation
* container freeze guarantees

---

# 37. Lifecycle Stability Policy

The following are considered:

```text id="4jlwm6"
FOUNDATIONAL STABLE RUNTIME SEMANTICS
```

* runtime state machine
* startup ordering
* shutdown ordering
* cancellation ownership
* plugin lifecycle
* supervision ownership
* container freeze semantics

Breaking changes require:

* ADR review
* migration analysis
* concurrency analysis
* operational impact review

---

# 38. Final Lifecycle Principle

```text id="5jlwm2"
The runtime lifecycle is the authoritative owner
of runtime existence, coordination, and termination.
```

All subsystems operate within lifecycle boundaries defined here.
