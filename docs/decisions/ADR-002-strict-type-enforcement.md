# ADR-002 — Strict Type Enforcement

## Status

Accepted

---

## Context

Async multimedia systems are integration-heavy.

The project contains:

- async workflows
- plugin contracts
- runtime orchestration
- event systems
- external integrations

Without strong typing:

- interface drift becomes common
- async failures become harder to debug
- runtime instability increases
- refactoring becomes dangerous

---

## Decision

The project will enforce:

```text
mypy --strict
```

Strict typing is mandatory.

Typing rules may not be weakened casually.

---

## Consequences

### Positive

- safer refactoring
- clearer interfaces
- reduced runtime surprises
- stronger plugin contracts
- improved IDE support
- better maintainability

### Negative

- increased upfront typing effort
- additional development friction
- stricter review requirements

These tradeoffs are acceptable.

---

## Alternatives Considered

### Weak Typing

Rejected because:

- async systems become runtime-chaotic
- plugin contracts become unstable
- maintenance cost increases over time

### Optional Typing

Rejected because:

- inconsistent enforcement produces unreliable architecture
- weak governance encourages gradual erosion
