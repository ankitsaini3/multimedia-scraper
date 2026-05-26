# Event Semantics

Status:

```text id="ev7m2q"
STABLE CONTRACT DRAFT
```

Scope:

```text id="w1x9pa"
Phase 1 — Core Runtime Foundations
```

This specification defines:

* event delivery guarantees
* event ordering semantics
* event isolation guarantees
* event ownership rules
* event lifecycle behavior
* event concurrency semantics
* event failure handling
* event subscription rules
* event cancellation behavior
* runtime observability guarantees

This document is:

```text id="h4k0tz"
architecturally authoritative
```

All implementations must conform to these semantics.

---

# 1. Event System Philosophy

The event system exists for:

* runtime coordination
* observability
* lifecycle signaling
* supervision integration
* plugin-safe communication
* cross-cutting runtime concerns

The event system does NOT exist for:

* business workflow orchestration
* distributed messaging
* persistent queues
* RPC replacement
* arbitrary control flow

---

# 2. Foundational Event Rule

Events communicate:

```text id="j7s3mr"
something happened
```

NOT:

```text id="o1w4bn"
what another subsystem must do
```

Events describe facts.

They do NOT issue commands.

---

# 3. Event System Scope

The Phase 1 event system is:

```text id="r6y2el"
in-process only
```

No guarantees exist for:

* persistence
* durability
* replay
* cross-process delivery
* distributed coordination

---

# 4. Event Ownership Model

# EventBus Owns

* event publication coordination
* subscription registry
* dispatch lifecycle
* handler isolation
* delivery coordination

---

# Runtime Lifecycle Owns

* event system startup
* event system shutdown
* event dispatch lifetime

---

# Subscribers Own

* handler execution logic
* handler-local state
* handler cleanup

---

# Publishers Do NOT Own

* handler execution
* subscriber lifecycle
* delivery persistence

---

# 5. Event Contract Structure

Canonical event contract:

```python id="evt1"
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class Event:

    event_id: UUID
    occurred_at: datetime
    correlation_id: UUID | None
```

Events are immutable runtime facts.

---

# 6. Event Immutability Semantics

Events MUST be:

```text id="g0w5pd"
immutable after publication
```

Mutation after publish is forbidden.

---

# Allowed Event Data

Events MAY contain:

* identifiers
* metadata
* DTO references
* correlation IDs
* timestamps

---

# Forbidden Event Data

Events MUST NOT contain:

* mutable runtime state
* infrastructure handles
* live runtime objects
* unmanaged resources

---

# 7. Event Publication Semantics

Publishing an event means:

```text id="m9r1yk"
the publisher declares a runtime fact occurred
```

Publication does NOT imply:

* successful processing
* handler completion
* guaranteed observation

---

# 8. Delivery Guarantees

Phase 1 delivery semantics are:

```text id="d7k8qa"
at-most-once delivery
```

Meaning:

* an event MAY be delivered once
* an event MAY be dropped
* retries are NOT guaranteed
* duplicate suppression is NOT guaranteed

---

# 9. No Persistence Guarantee

The event system provides:

```text id="x3u6zn"
NO persistence guarantee
```

Events are transient runtime coordination signals.

---

# 10. No Replay Guarantee

The system provides:

```text id="f5l2wc"
NO replay guarantee
```

Late subscribers do not receive historical events.

---

# 11. No Delivery Confirmation Guarantee

Publishers are NOT guaranteed:

* subscriber receipt
* handler completion
* downstream success

Publishing indicates ONLY:

```text id="p8j4ds"
dispatch attempt accepted
```

---

# 12. Event Ordering Semantics

Global ordering is:

```text id="q2n7eb"
NOT guaranteed
```

Consumers MUST NOT depend on:

* global ordering
* subscription ordering
* task scheduling ordering

---

# 13. Per-Type Ordering

Per-event-type ordering is also:

```text id="t9k5vf"
NOT guaranteed
```

Future implementations MAY preserve ordering internally.

The contract does NOT guarantee it.

---

# 14. Subscriber Ordering

Subscriber invocation order is:

```text id="u4x1lm"
undefined
```

Subscribers MUST remain order-independent.

---

# 15. Event Isolation Semantics

The event system guarantees:

```text id="z7y3wr"
subscriber isolation
```

Meaning:

* one failing handler MUST NOT crash publishers
* one failing handler MUST NOT corrupt dispatch state
* one failing handler MUST NOT stop unrelated handlers

---

# 16. Handler Failure Semantics

Handler failures MUST:

* remain isolated
* preserve root causes
* emit structured logs
* remain observable

Handler failures MUST NOT:

* silently disappear
* terminate runtime unexpectedly

---

# 17. Publisher Isolation Guarantees

Publishers are isolated from:

* handler failures
* handler cancellation
* subscriber lifecycle

Publishers declare facts only.

---

# 18. Event Dispatch Semantics

Dispatch MAY occur:

* sequentially
* concurrently
* through queues
* through workers

The implementation strategy is internal.

The stable contract guarantees ONLY:

* isolation
* lifecycle ownership
* bounded behavior
* observability

---

# 19. Concurrency Semantics

Event dispatch is:

```text id="e6w9pk"
async-aware
```

Handlers MAY execute concurrently.

Consumers MUST assume concurrency.

---

# 20. Handler Concurrency Rules

Handlers MUST:

* be cancellation-safe
* avoid blocking runtime
* avoid shared mutable state
* remain idempotency-tolerant where practical

Handlers MUST NOT:

* mutate runtime lifecycle
* bypass supervision
* spawn detached tasks

---

# 21. EventBus Lifecycle Semantics

The event system lifecycle is:

```text id="n1r4qy"
runtime-scoped
```

The event bus exists ONLY during active runtime lifecycle.

---

# Startup Guarantees

Before RUNNING:

* subscriptions operational
* dispatch operational
* observability hooks active

---

# Shutdown Guarantees

During SHUTTING_DOWN:

* new event publication MAY be rejected
* dispatch MAY drain
* handler failures MUST remain observable

---

# 22. Event Cancellation Semantics

Event handlers participate in runtime cancellation.

Handlers MUST:

* support cooperative cancellation
* preserve cleanup execution
* avoid cancellation suppression

---

# 23. Backpressure Semantics

The event system MUST support:

```text id="s8p6dx"
bounded runtime behavior
```

Unbounded memory growth is forbidden.

---

# Allowed Backpressure Policies

Implementations MAY:

* throttle publishers
* bound queues
* drop events
* reject publication

Policies MUST remain observable.

---

# 24. Event Type Semantics

Events are:

```text id="v2j8gh"
typed runtime contracts
```

Subscribers subscribe to event types.

---

# Event Type Inheritance Rules

Implementations MAY support:

* polymorphic subscription
* inheritance-based dispatch

The stable contract does NOT require it.

---

# 25. Event Naming Semantics

Event names represent:

```text id="w6m3rt"
completed runtime facts
```

Examples:

Good:

```text id="x1n7yb"
TaskStartedEvent
PluginActivatedEvent
RuntimeShutdownInitiatedEvent
```

Bad:

```text id="y9r4ku"
StartTaskEvent
ActivatePluginEvent
```

Commands are forbidden.

---

# 26. Event Payload Rules

Payloads MUST remain:

* serializable-friendly
* immutable
* bounded
* infrastructure-agnostic

Payloads SHOULD remain lightweight.

---

# 27. Correlation Semantics

Events MAY include:

```text id="z5t8qp"
correlation identifiers
```

Correlation IDs support:

* tracing
* observability
* lifecycle diagnostics

Correlation semantics are runtime-scoped.

---

# 28. Runtime Observability Semantics

The event system MUST emit observable signals for:

* handler failure
* dispatch rejection
* queue overflow
* shutdown draining
* cancellation propagation

Silent failure is forbidden.

---

# 29. Subscription Semantics

Subscriptions are:

```text id="a2m9vs"
runtime-scoped resources
```

Subscriptions belong to the EventBus lifecycle.

---

# Subscription Guarantees

Subscriptions MUST:

* unregister cleanly
* participate in shutdown
* avoid leaking handlers

---

# Subscription Ownership Rules

Subscriptions are owned by:

```text id="b4r7qe"
EventBus
```

Subscribers do NOT directly manage dispatch internals.

---

# 30. Illegal Event Behaviors

Forbidden behaviors include:

---

## Mutable Events

Forbidden:

```python id="evt2"
event.payload[\"state\"] = ...
```

after publish.

---

## Command-Oriented Events

Forbidden:

```text id="c6n2wk"
DoSomethingEvent
```

---

## Runtime Lifecycle Mutation From Handlers

Forbidden:

```python id="evt3"
runtime.shutdown()
```

inside arbitrary handler logic.

---

## Detached Handler Tasks

Forbidden:

```python id="evt4"
asyncio.create_task(...)
```

outside supervision ownership.

---

## Blocking Event Handlers

Forbidden:

```python id="evt5"
time.sleep(...)
```

inside handler execution.

---

# 31. Event Testing Semantics

Tests MUST verify:

* handler isolation
* delivery semantics
* cancellation propagation
* bounded behavior
* observability guarantees
* shutdown draining
* handler failure containment

---

# 32. Event Stability Policy

The following are considered:

```text id="d8v5ly"
FOUNDATIONAL STABLE EVENT SEMANTICS
```

* delivery guarantees
* ordering guarantees
* isolation guarantees
* lifecycle ownership
* cancellation participation
* event immutability
* subscription semantics

Breaking changes require:

* ADR review
* concurrency analysis
* lifecycle compatibility review
* operational impact review

---

# 33. Final Event Principle

```text id="e1x7pr"
Events describe facts.
The runtime coordinates consequences.
```

The event system exists to provide:

* decoupled runtime coordination
* observability
* lifecycle signaling
* plugin-safe communication

within strict lifecycle and concurrency boundaries.
