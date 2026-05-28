# Async Execution Model

The project uses async orchestration extensively.

---

## Goals

- concurrency
- provider fan-out
- streaming responsiveness
- cancellation support
- backpressure handling

---

## Rules

- avoid blocking operations in async paths
- isolate CPU-heavy work
- preserve cancellation propagation
- use bounded concurrency

---