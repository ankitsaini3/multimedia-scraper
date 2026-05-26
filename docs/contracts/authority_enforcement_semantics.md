The goal is NOT merely “permissions”.
It must formally unify:

* capabilities
* runtime authority
* task inheritance
* plugin isolation
* security boundaries
* delegation
* revocation
* resource ownership
* supervision
* execution scopes

without accidentally creating:

```text
service possession == implicit authority
```

That is the critical danger.

Your existing architecture already strongly implies the correct direction:

* authority is explicit
* authority is capability-bound
* authority is not ambient
* boundaries require validation
* plugins are zero-trust compatible

So this contract should crystallize those semantics into one authoritative model.

Below is the architecture review of what this document MUST achieve, followed by the structure I recommend.

---

# What This Contract Must Solve

This document must answer these questions decisively:

| Question                                              | Must Be Explicit                              |
| ----------------------------------------------------- | --------------------------------------------- |
| Does resolving a service imply authority?             | NO                                            |
| Is authority ambient/global?                          | NO                                            |
| Is authority inherited by child tasks?                | Controlled                                    |
| Can authority be delegated?                           | Yes, explicitly                               |
| Can authority be reduced?                             | Yes                                           |
| Can authority be escalated dynamically?               | No implicit escalation                        |
| Are capabilities runtime-scoped?                      | Yes                                           |
| Can plugins bypass validation?                        | No                                            |
| Can authority survive scope teardown?                 | No                                            |
| Can resources be used without authority revalidation? | No                                            |
| Is revocation supported?                              | Yes                                           |
| Is authority serializable?                            | No (except explicit tokens if designed later) |

If these are not frozen,
future implementation WILL drift into:

* ambient authority,
* accidental privilege escalation,
* hidden trust channels.

---

# The Most Important Architectural Decision

This MUST become a frozen invariant:

```text
Possession of a dependency does NOT imply authority.
```

This is the single most important rule in the document.

Example:

```python
ffmpeg_service = container.resolve(FFmpegService)
```

MUST NOT automatically imply:

```text
process.ffmpeg authority
```

Instead:

* operations validate authority,
* execution scopes carry authority context,
* privileged actions require explicit validation.

Otherwise the entire capability architecture collapses into DI-driven ambient authority.

This is your highest-risk future failure mode.

---

# The Correct Authority Model For Your Runtime

Your architecture is already converging toward this model:

```text
Authority is:
- explicit
- scoped
- immutable
- delegatable
- reducible
- observable
- lifecycle-bound
- non-ambient
```

That is the correct design.

---

# Recommended Architectural Model

You should formally define:

---

# 1. Authority Context

Every execution scope carries:

```text
AuthorityContext
```

Containing:

* granted capabilities
* delegation metadata
* scope lineage
* sandbox constraints
* authority expiration
* revocation hooks

Authority flows THROUGH scopes,
not through services.

This is critical.

---

# 2. Authority Is Scope-Bound

Authority belongs to:

* runtime scopes
* supervised execution scopes
* plugin scopes
* task scopes

NOT:

* services
* DTOs
* runtime singletons
* global state

Excellent alignment with your existing ownership theory.

---

# 3. Child Tasks Inherit Restricted Authority

Child tasks MAY inherit:

* same authority
  OR
* reduced authority

But MUST NOT gain:

* broader authority automatically.

This is critical.

---

# 4. Delegation Must Be Explicit

Authority delegation MUST define:

* delegator
* delegatee
* delegated capability subset
* duration
* revocation semantics

Implicit delegation is forbidden.

---

# 5. Authority Reduction Must Be First-Class

Your runtime should encourage:

```text
least privilege execution
```

This means:

* plugin tasks can run under narrower authority
* subprocesses can run under narrower authority
* browser sessions can run under narrower authority

This is VERY important for future sandboxing.

---

# 6. Revocation Semantics

Revocation MUST:

* propagate downward
* invalidate future privileged actions
* remain observable
* avoid corrupting running state

Revocation is hard.
You do not need perfect preemptive revocation yet.

But you MUST freeze semantics now.

---

# 7. Ambient Authority Must Be Forbidden

You MUST explicitly forbid:

* global authority registries
* thread-local hidden authority
* implicit plugin authority
* service-based privilege assumptions

This is critical.

---

# 8. DTOs Must NEVER Carry Runtime Authority

Very important.

DTOs may contain:

* identifiers
* claims
* metadata

But MUST NOT carry:

* live runtime authority
* executable permissions
* privileged runtime handles

Otherwise replay/persistence becomes unsafe.

---

# 9. Capability Validation Timing

You need explicit semantics for:

```text
when validation occurs
```

Correct answer:

* validation occurs at privileged operation boundaries.

NOT:

* only during dependency resolution.

Example:

```python
await ffmpeg.transcode()
```

must validate authority at execution time.

Not merely at service acquisition time.

---

# 10. Authority + Supervision Must Integrate

Very important.

Supervisors should own:

* authority propagation
* authority reduction
* revocation propagation

This aligns perfectly with your structured concurrency model.

Excellent fit architecturally.

---

# 11. Authority + Resources Must Integrate

Resources MUST remain bound to:

* authority scope
* owner scope

Examples:

* browser sessions
* temp dirs
* FFmpeg processes
* download handles

Authority revocation SHOULD eventually invalidate resource usage.

---

# 12. Sandbox = Upper Bound Of Authority

You already implied this correctly in security semantics.

Formalize:

```text
effective authority
=
capability grant
∩
sandbox constraints
∩
runtime policy
```

Very important.



# Critical Frozen Invariants

These MUST appear explicitly.

---

## Invariant 1

```text
Authority is explicit and never ambient.
```

---

## Invariant 2

```text
Possession of a dependency does not imply authority.
```

---

## Invariant 3

```text
Authority is scope-bound and lifecycle-bound.
```

---

## Invariant 4

```text
Child scopes may inherit equal or reduced authority, never implicit escalation.
```

---

## Invariant 5

```text
All privileged operations require authority validation at execution time.
```

---

## Invariant 6

```text
Authority delegation must be explicit and observable.
```

---

## Invariant 7

```text
Authority revocation propagates downward through supervision hierarchy.
```

---

## Invariant 8

```text
Serialized payloads never carry live runtime authority.
```

---

## Invariant 9

```text
Sandbox constraints define upper bounds of effective authority.
```

---

## Invariant 10

```text
Authority validation failures fail safely and observably.
```


