# `docs/contracts/scheduling_execution_semantics.md`

# Scheduling & Execution Semantics

---

# 1. Purpose

This document defines the authoritative scheduling and execution model of the runtime.

It specifies:

* task scheduling semantics
* prioritization rules
* fairness guarantees
* starvation prevention
* queue governance
* retry scheduling semantics
* work stealing policy
* resource contention handling
* execution lifecycle rules
* concurrency coordination
* scheduling observability

This document governs execution behavior across:

* downloads
* streaming
* transcoding
* browser automation
* FFmpeg pipelines
* metadata extraction
* plugin execution
* provider operations
* workers
* orchestration systems

This is the canonical execution governance layer.

---

# 2. Architectural Goals

The scheduling system exists to guarantee:

```text id="7d3m9x"
1. Deterministic execution behavior
2. Fair resource allocation
3. Predictable prioritization
4. Starvation prevention
5. Bounded retry behavior
6. Resource isolation
7. Graceful degradation
8. Backpressure propagation
9. Operational stability
10. Long-term maintainability
```

---

# 3. Core Principles

---

## 3.1 Scheduling Is Explicit

Execution ordering MUST be governed by explicit scheduling policies.

Implicit scheduling behavior is forbidden.

---

## 3.2 Fairness Over Opportunism

The runtime prioritizes fairness and stability over maximum instantaneous throughput.

---

## 3.3 Starvation Is Forbidden

No eligible long-lived task may be indefinitely prevented from execution.

---

## 3.4 Scheduling Must Be Observable

Scheduling decisions SHOULD be inspectable and auditable.

---

## 3.5 Execution Is Resource-Bounded

All execution occurs within bounded resource governance.

---

# 4. Execution Taxonomy

---

# 4.1 CPU-Bound Work

Examples:

```text id="df2zk5"
transcoding
thumbnail generation
media analysis
hashing
compression
```

CPU-bound work SHOULD use bounded worker pools.

---

# 4.2 IO-Bound Work

Examples:

```text id="8a3m0f"
downloads
network requests
database access
filesystem operations
```

IO-bound work SHOULD prefer async scheduling.

---

# 4.3 Latency-Sensitive Work

Examples:

```text id="xq4k2v"
stream playback
adaptive bitrate switching
interactive CLI actions
```

Latency-sensitive work receives elevated scheduling priority.

---

# 4.4 Background Work

Examples:

```text id="9w5m4j"
cache cleanup
thumbnail regeneration
metadata refresh
analytics computation
```

Background work SHOULD yield aggressively.

---

# 4.5 Long-Running Work

Examples:

```text id="4c1p9h"
browser automation
large transcoding jobs
playlist downloads
```

Long-running tasks require cooperative scheduling semantics.

---

# 5. Scheduling Model

---

# 5.1 Scheduler Ownership

The runtime scheduler is the authoritative owner of execution ordering.

Plugins MUST NOT directly control global scheduling.

---

# 5.2 Cooperative Scheduling

The runtime primarily uses cooperative scheduling semantics.

Tasks SHOULD:

```text id="5y4f8m"
yield
checkpoint
respect cancellation
respect backpressure
```

---

# 5.3 Preemption Policy

Hard preemption SHOULD be minimized.

Soft cooperative interruption is preferred.

---

# 5.4 Scheduling Determinism

Scheduling SHOULD remain deterministic where feasible.

Undefined race-driven scheduling behavior is discouraged.

---

# 6. Prioritization Semantics

---

# 6.1 Priority Classes

Canonical priority tiers:

| Tier       | Examples         |
| ---------- | ---------------- |
| critical   | runtime recovery |
| high       | active playback  |
| normal     | downloads        |
| low        | metadata refresh |
| background | cleanup          |

---

# 6.2 Priority Is Advisory

Priority influences scheduling preference but MUST NOT violate fairness guarantees.

---

# 6.3 Priority Escalation

Schedulers MAY temporarily escalate priority for:

```text id="5xk6dp"
starvation prevention
deadline-sensitive work
backpressure recovery
interactive responsiveness
```

---

# 6.4 Priority Inversion Protection

Schedulers SHOULD mitigate priority inversion.

Examples:

```text id="j6s0pl"
lock inheritance
temporary priority boosting
resource fairness balancing
```

---

# 7. Fairness Semantics

---

# 7.1 Fairness Requirement

Eligible tasks MUST receive execution opportunity within bounded time.

---

# 7.2 Queue Fairness

Schedulers SHOULD avoid monopolization by:

```text id="e4z4b7"
single plugins
single providers
single downloads
single workers
```

---

# 7.3 Weighted Fairness

Weighted fairness MAY be used.

Examples:

```text id="8f9j1d"
playback > transcoding
interactive CLI > background cleanup
```

---

# 7.4 Fairness Scope

Fairness SHOULD apply across:

```text id="d2j7e1"
tasks
plugins
providers
worker pools
resource domains
```

---

# 8. Starvation Prevention Semantics

---

# 8.1 Starvation Prevention Is Mandatory

Schedulers MUST prevent indefinite execution denial.

---

# 8.2 Aging Policies

Schedulers MAY increase task priority over time.

---

# 8.3 Starvation Detection

Schedulers SHOULD detect:

```text id="u8r3m2"
queue stagnation
repeated deferral
resource monopolization
```

---

# 8.4 Recovery Strategies

Recovery MAY include:

```text id="n1q7ts"
priority boosting
queue reshuffling
work redistribution
resource throttling
```

---

# 9. Queue Scheduling Semantics

---

# 9.1 Queues Are Explicit Runtime Resources

Queues MUST define:

```text id="4k3jvv"
capacity
ordering semantics
priority behavior
overflow policy
retry semantics
```

---

# 9.2 Queue Types

Supported queue styles MAY include:

| Type                | Purpose                      |
| ------------------- | ---------------------------- |
| FIFO                | general execution            |
| priority queue      | latency-sensitive work       |
| delayed queue       | retries/backoff              |
| bounded queue       | resource protection          |
| work-stealing queue | distributed worker balancing |

---

# 9.3 Queue Capacity

Queues SHOULD be bounded.

Unbounded queues are discouraged.

---

# 9.4 Overflow Policy

Overflow behavior MUST be explicit.

Examples:

```text id="e7u4kt"
reject new work
backpressure propagation
drop low-priority work
defer scheduling
```

---

# 9.5 Queue Ordering

Queue ordering MUST be deterministic within defined policies.

---

# 10. Work Stealing Semantics

---

# 10.1 Work Stealing Is Optional

The runtime MAY support work stealing.

---

# 10.2 Stealing Constraints

Work stealing MUST preserve:

```text id="1r2t9w"
capability isolation
ownership semantics
resource boundaries
priority guarantees
```

---

# 10.3 Stealable Work

Not all tasks are stealable.

Examples of non-stealable work:

```text id="8u4wod"
thread-affine operations
browser session state
exclusive resource ownership
```

---

# 10.4 Locality Preference

Schedulers SHOULD prefer local execution before stealing.

---

# 11. Retry Scheduling Semantics

---

# 11.1 Retries Are Scheduled Operations

Retries MUST re-enter scheduling pipelines.

Retries are not immediate recursive execution.

---

# 11.2 Retry Policies

Retry behavior MUST define:

```text id="2s5n9r"
retry limits
backoff policy
jitter policy
retry classification
retry deadlines
```

---

# 11.3 Retry Classification

Retryability MUST depend on failure type.

Examples:

| Failure Type                  | Retryable |
| ----------------------------- | --------- |
| transient network error       | yes       |
| invalid configuration         | no        |
| permission denial             | no        |
| temporary provider throttling | yes       |

---

# 11.4 Exponential Backoff

Retries SHOULD use bounded exponential backoff.

---

# 11.5 Retry Storm Prevention

Schedulers MUST prevent retry amplification storms.

Strategies MAY include:

```text id="d6w9j8"
global retry throttling
provider cooldowns
queue rate limiting
circuit breakers
```

---

# 12. Resource Contention Semantics

---

# 12.1 Shared Resource Governance

Schedulers MUST coordinate shared resources.

Examples:

```text id="k8j5y1"
CPU
network bandwidth
disk IO
browser instances
FFmpeg workers
```

---

# 12.2 Resource Quotas

Subsystems MAY define quotas.

Examples:

```text id="6d4vpc"
max concurrent downloads
max transcoding workers
max browser sessions
```

---

# 12.3 Contention Resolution

Contention SHOULD resolve predictably.

Undefined competition behavior is forbidden.

---

# 13. Backpressure Semantics

---

# 13.1 Backpressure Is Mandatory

Schedulers MUST support backpressure propagation.

---

# 13.2 Backpressure Sources

Examples:

```text id="x6n4qv"
queue saturation
network exhaustion
disk saturation
provider throttling
worker exhaustion
```

---

# 13.3 Backpressure Propagation

Backpressure SHOULD propagate upstream.

Examples:

```text id="q0k9v4"
slow producers
defer scheduling
pause downloads
reduce concurrency
```

---

# 14. Cancellation Semantics

---

# 14.1 Cancellation Is Cooperative

Tasks SHOULD cooperate with cancellation requests.

---

# 14.2 Cancellation Propagation

Cancellation SHOULD propagate through:

```text id="s8r4g1"
child tasks
dependent pipelines
worker hierarchies
```

---

# 14.3 Cancellation Safety

Cancelled tasks MUST release:

```text id="8w7fkp"
locks
resources
queue reservations
temporary state
```

---

# 15. Deadline & Timeout Semantics

---

# 15.1 Time-Bounded Execution

Tasks MAY define deadlines or execution timeouts.

---

# 15.2 Deadline Awareness

Schedulers SHOULD prioritize deadline-sensitive tasks appropriately.

---

# 15.3 Timeout Handling

Timeout expiration MUST produce explicit failure semantics.

---

# 16. Execution Isolation Semantics

---

# 16.1 Isolation Boundaries

Schedulers MUST preserve:

```text id="1d4nmt"
plugin isolation
provider isolation
sandbox boundaries
resource quotas
```

---

# 16.2 Fault Isolation

Misbehaving tasks MUST NOT destabilize unrelated workloads.

---

# 16.3 Execution Domains

Execution MAY be partitioned into domains.

Examples:

```text id="3z2k8p"
download workers
browser workers
transcoding pools
metadata workers
```

---

# 17. Browser Automation Scheduling

---

# 17.1 Browser Resources Are Scarce

Browser automation requires bounded scheduling.

---

# 17.2 Browser Session Limits

Schedulers SHOULD enforce:

```text id="r0x4ys"
max concurrent sessions
tab limits
resource quotas
session reuse policies
```

---

# 17.3 Browser Fairness

Single plugins/providers MUST NOT monopolize browser resources.

---

# 18. FFmpeg Scheduling

---

# 18.1 FFmpeg Is Resource-Heavy

FFmpeg execution MUST be strongly resource-governed.

---

# 18.2 FFmpeg Concurrency

Schedulers SHOULD bound:

```text id="g7y5w9"
CPU utilization
parallel transcodes
memory consumption
disk IO
```

---

# 18.3 Adaptive Scheduling

Schedulers MAY reduce FFmpeg concurrency under pressure.

---

# 19. Download Scheduling

---

# 19.1 Download Fairness

Schedulers SHOULD prevent single downloads from monopolizing bandwidth.

---

# 19.2 Adaptive Concurrency

Download concurrency MAY adapt based on:

```text id="6p1kqm"
network quality
provider throttling
disk pressure
system load
```

---

# 19.3 Stream vs Download Priority

Active playback SHOULD outrank bulk downloading.

---

# 20. Observability & Auditability

---

# 20.1 Scheduling Decisions SHOULD Be Observable

Examples:

```text id="x7m4wq"
queue depth
task latency
retry counts
starvation events
resource contention
```

---

# 20.2 Queue Metrics

Schedulers SHOULD expose:

```text id="6w2mrx"
queue occupancy
wait time
throughput
drop rates
retry pressure
```

---

# 20.3 Execution Tracing

Long-running operations SHOULD support tracing.

---

# 21. Failure Semantics

---

# 21.1 Scheduling Failures Must Be Explicit

Scheduling failures MUST produce typed failures.

Examples:

```python id="u7j0da"
QueueOverflowError
RetryLimitExceededError
TaskStarvationError
SchedulingPolicyViolationError
```

---

# 21.2 Retry Exhaustion

Retry exhaustion MUST terminate predictably.

Infinite retries are forbidden unless explicitly configured.

---

# 21.3 Graceful Degradation

Under overload, the runtime SHOULD degrade gracefully.

Examples:

```text id="d4w8ns"
drop background work
reduce concurrency
throttle retries
defer non-critical tasks
```

---

# 22. Future Compatibility Requirements

This scheduling system MUST remain compatible with:

```text id="1m4c7n"
distributed execution
remote workers
container orchestration
GPU scheduling
cloud-native runtimes
WASM workers
multi-tenant execution
```

---

# 23. Architectural Invariants

---

## Fairness

```text id="5r9m1d"
Eligible tasks eventually receive execution opportunity.
```

---

## Determinism

```text id="8x1m5q"
Scheduling policies are explicit and deterministic.
```

---

## Isolation

```text id="4z6t3n"
Execution isolation boundaries are preserved.
```

---

## Resource Governance

```text id="2k4x8w"
All execution occurs within bounded resource governance.
```

---

## Retry Safety

```text id="1j8s9m"
Retries re-enter scheduling pipelines with bounded behavior.
```

---

## Backpressure

```text id="7f0k2r"
Backpressure propagates through execution systems.
```

---

## Starvation Prevention

```text id="0t3v9x"
Long-lived starvation is forbidden.
```

---

## Queue Safety

```text id="5w1m8n"
Queue overflow behavior is explicitly defined.
```

---

## Cancellation

```text id="9n6q4p"
Cancellation is cooperative and resource-safe.
```

---

## Stability

```text id="3d8m2v"
Misbehaving workloads cannot destabilize the runtime.
```
