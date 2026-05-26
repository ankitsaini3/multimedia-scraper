# Concurrency Semantics

Status:

```text id="c1m7ae"
STABLE CONTRACT DRAFT
```

Scope:

```text id="n4y1pd"
Phase 1 — Core Runtime Foundations
```

This specification defines:

* concurrency ownership
* async coordination rules
* task lifetime semantics
* supervision guarantees
* cancellation propagation
* runtime concurrency boundaries
* isolation guarantees
* scheduling assumptions
* event concurrency semantics
* plugin concurrency constraints

This document is:

```text id="2k7vxo"
architecturally authoritative
```

All implementations must conform to these semantics.

---

# 1. Concurrency Philosophy

Concurrency exists to support:

* runtime responsiveness
* isolation
* coordination
* cancellation
* observability
* fault containment

Concurrency is NOT:

* unrestricted parallel execution
* detached task spawning
* uncontrolled background work

The runtime must remain:

```text id="w0v3jo"
deterministic under concurrent execution
```

---

# 2. Foundational Concurrency Rule

All runtime concurrency MUST be:

```text id="8zzjlwm"
runtime-owned and supervised
```

No long-lived concurrent execution may exist outside runtime supervision.

---

# 3. Concurrency Ownership Model

# Runtime Lifecycle Owns

* global cancellation root
* runtime startup synchronization
* runtime shutdown synchronization
* runtime state transitions

---

# Supervisor Owns

* task tracking
* task lifetime
* task cancellation
* failure isolation
* graceful task shutdown

---

# EventBus Owns

* handler dispatch coordination
* subscription concurrency isolation
* event fanout coordination

---

# Plugins Do NOT Own

* global task hierarchies
* runtime cancellation roots
* detached runtime execution

---

# 4. Canonical Concurrency Boundary

The authoritative concurrency boundary is:

```text id="tjlwm9"
Supervisor
```

All long-lived runtime tasks MUST pass through supervision.

---

# 5. Task Classification

Runtime tasks are classified into:

| Type           | Lifetime         |
| -------------- | ---------------- |
| startup tasks  | startup-scoped   |
| runtime tasks  | runtime-scoped   |
| request tasks  | operation-scoped |
| shutdown tasks | shutdown-scoped  |

---

# 6. Startup Task Semantics

Startup tasks:

* exist only during STARTING
* are runtime-owned
* must complete before RUNNING

Startup tasks MUST NOT:

* outlive startup phase
* detach from startup lifecycle

---

# 7. Runtime Task Semantics

Runtime tasks:

* are long-lived
* exist during RUNNING
* are supervised
* participate in cancellation propagation

Examples:

* event dispatch workers
* plugin background workers
* runtime coordination loops

---

# 8. Request Task Semantics

Request tasks are:

```text id="6jlwm8"
operation-scoped
```

Examples:

* metadata extraction
* search request
* validation pipeline

Request tasks MAY:

* complete independently
* spawn child tasks through supervision

Request tasks MUST NOT:

* escape cancellation boundaries
* become detached runtime tasks

---

# 9. Shutdown Task Semantics

Shutdown tasks exist ONLY during:

```text id="7jlwm0"
SHUTTING_DOWN
```

Examples:

* cleanup
* draining
* flushing
* graceful teardown

Shutdown tasks MUST:

* remain bounded
* support cancellation
* avoid spawning runtime work

---

# 10. Supervision Model

The supervision model is:

```text id="9jlwm1"
hierarchical ownership supervision
```

Every long-lived task has exactly one supervisor owner.

---

# 11. Forbidden Concurrency Patterns

Forbidden:

---

## Detached Tasks

Forbidden:

```python id="1jlwm5"
asyncio.create_task(...)
```

without supervision ownership.

---

## Fire-and-Forget Runtime Work

Forbidden:

```python id="2jlwm8"
loop.create_task(...)
```

without lifecycle ownership.

---

## Unbounded Background Loops

Forbidden:

```python id="3jlwm0"
while True:
    ...
```

without cancellation participation.

---

## Plugin-Owned Runtime Loops

Forbidden:

```python id="4jlwm7"
plugin creates unmanaged runtime worker
```

---

# 12. Task Ownership Rule

Every runtime task MUST have:

```text id="5jlwm6"
exactly one lifecycle owner
```

Shared ownership is forbidden.

---

# 13. Task Lifetime Rules

Tasks MUST NOT:

* outlive runtime
* outlive parent supervision scope
* bypass cancellation propagation

Tasks MUST:

* support graceful shutdown
* support cleanup execution
* remain observable

---

# 14. Cancellation Semantics

Cancellation is:

```text id="6jlwm1"
hierarchical and downward-propagating
```

The runtime lifecycle owns the cancellation root.

---

# 15. Cancellation Propagation Rules

Cancellation propagates:

```text id="7jlwm4"
runtime
    -> supervisor
        -> task group
            -> child tasks
```

Propagation MUST remain deterministic.

---

# 16. Cancellation Guarantees

Cancellation MUST:

* preserve cleanup execution
* preserve finally blocks
* preserve observability
* remain structured

Cancellation MUST NOT:

* silently disappear
* terminate unrelated ownership scopes
* orphan child tasks

---

# 17. Graceful Cancellation Rules

Tasks MUST support:

```text id="8jlwm9"
cooperative cancellation
```

Tasks MUST:

* yield periodically
* avoid infinite blocking
* handle cancellation safely

---

# 18. Forced Cancellation

Forced cancellation MAY occur if:

* graceful shutdown timeout exceeded
* runtime corruption detected
* supervision failure occurs

Forced cancellation MUST remain observable.

---

# 19. Concurrency Isolation Guarantees

Task failures MUST remain isolated.

A failing task MUST NOT:

* corrupt unrelated tasks
* terminate runtime unexpectedly
* corrupt supervision state

---

# 20. Failure Containment Semantics

Failures propagate ONLY through:

* supervision
* lifecycle coordination
* structured runtime events

Failures MUST NOT propagate arbitrarily through concurrency boundaries.

---

# 21. EventBus Concurrency Semantics

The event bus is:

```text id="9jlwm3"
async-aware and fanout-capable
```

---

# Event Dispatch Guarantees

Event publishing MUST:

* remain non-blocking where possible
* isolate handler failures
* preserve runtime stability

---

# Event Handler Isolation

A failing handler MUST NOT:

* crash publisher
* corrupt dispatch state
* block unrelated handlers

---

# Event Concurrency Model

The event bus MAY dispatch handlers:

* sequentially
* concurrently
* through worker queues

The dispatch strategy is implementation-defined.

The contract guarantees ONLY:

```text id="0jlwm5"
handler isolation
```

NOT ordering guarantees.

---

# 22. Event Ordering Semantics

Global event ordering is NOT guaranteed.

Per-event ordering is also NOT guaranteed unless explicitly documented later.

Consumers MUST NOT rely on ordering.

---

# 23. Event Backpressure Semantics

The event system MUST support bounded runtime behavior.

Unbounded event growth is forbidden.

The implementation MAY:

* drop events
* throttle publishers
* apply bounded queues

The policy must remain observable.

---

# 24. Plugin Concurrency Semantics

Plugins operate within runtime concurrency boundaries.

Plugins MUST:

* use supervised tasks
* participate in cancellation
* avoid detached execution

Plugins MUST NOT:

* own global event loops
* create unmanaged worker pools
* bypass runtime supervision

---

# 25. RuntimeContext Concurrency Semantics

RuntimeContext startup/shutdown are serialized operations.

Forbidden:

```python id="1jlwm2"
concurrent startup/shutdown execution
```

---

# RuntimeContext Guarantees

startup():

* atomic state transition
* single execution owner
* rollback-safe

shutdown():

* idempotent
* cancellation-safe
* cleanup-safe

---

# 26. Dependency Container Concurrency Semantics

The dependency container becomes immutable after RUNNING.

Container mutation during concurrent runtime execution is forbidden.

---

# 27. Shared State Semantics

Shared mutable state is:

```text id="2jlwm6"
heavily restricted
```

---

# Allowed Shared Mutable State

Allowed ONLY inside:

* supervision internals
* event subscription registry
* lifecycle coordination internals

---

# Forbidden Shared State

Forbidden:

* cross-module mutable globals
* unsynchronized runtime mutation
* plugin-owned global state

---

# 28. Synchronization Policy

Synchronization primitives MAY exist ONLY where ownership is explicit.

Allowed:

* asyncio.Lock
* asyncio.Event
* asyncio.Queue

Forbidden:

* hidden synchronization coupling
* implicit cross-module synchronization

---

# 29. Blocking Operation Rules

Blocking operations inside runtime concurrency are forbidden.

Forbidden:

* blocking I/O in event handlers
* blocking sleeps
* synchronous network waits

Blocking work MUST be isolated.

---

# 30. Async Boundary Rules

Async boundaries MUST remain explicit.

Forbidden:

```python id="3jlwm9"
implicitly starting event loops
```

Runtime owns async coordination.

---

# 31. Threading Policy

Phase 1 runtime is:

```text id="4jlwm2"
async-first
```

NOT thread-first.

Threads MAY be introduced later ONLY behind runtime-owned boundaries.

Thread ownership MUST remain explicit.

---

# 32. Process Ownership Policy

Runtime-owned subprocesses MUST eventually become supervised resources.

No unmanaged subprocess ownership allowed.

This becomes critical in later phases:

* playback
* browser automation
* download orchestration

---

# 33. Timeout Semantics

Long-running runtime operations SHOULD support timeouts.

Timeouts MUST:

* remain observable
* preserve cancellation semantics
* preserve cleanup guarantees

---

# 34. Observability Semantics

Concurrency events MUST remain observable.

Required observable signals:

* task spawned
* task completed
* task cancelled
* task failed
* supervision escalation
* forced cancellation
* event dispatch failure

---

# 35. Concurrency Testing Rules

Tests MUST verify:

* cancellation propagation
* task cleanup
* supervision ownership
* task isolation
* graceful shutdown behavior
* timeout handling
* event handler isolation

---

# 36. Illegal Concurrency Behavior

Forbidden behaviors include:

---

## Detached Runtime Tasks

Forbidden:

```python id="5jlwm5"
asyncio.create_task(...)
```

outside supervision.

---

## Infinite Uncancelable Loops

Forbidden:

```python id="6jlwm3"
while True:
    pass
```

---

## Blocking Runtime Coordination

Forbidden:

```python id="7jlwm2"
time.sleep(...)
```

inside async runtime.

---

## Plugin-Owned Global Concurrency

Forbidden:

```python id="8jlwm4"
plugin manages independent runtime scheduler
```

---

# 37. Concurrency Stability Policy

The following are considered:

```text id="9jlwm7"
FOUNDATIONAL STABLE CONCURRENCY SEMANTICS
```

* supervision ownership
* cancellation hierarchy
* task ownership
* runtime concurrency boundaries
* plugin concurrency restrictions
* event isolation guarantees

Breaking changes require:

* ADR review
* concurrency analysis
* lifecycle compatibility review
* operational impact evaluation

---

# 38. Final Concurrency Principle

```text id="0jlwm8"
Concurrency without ownership is forbidden.
```

All concurrent execution must remain:

* supervised
* observable
* cancellable
* isolated
* lifecycle-scoped
* runtime-owned
