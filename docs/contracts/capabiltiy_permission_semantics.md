# `docs/contracts/capability_permission_semantics.md`

# Capability & Permission Semantics

---

# 1. Purpose

This document defines the authoritative security, authority, and permission model of the runtime.

It specifies:

* capability grants
* authority propagation
* permission isolation
* provider access restrictions
* runtime privilege boundaries
* plugin authority contracts
* filesystem/network/process constraints
* sandbox governance semantics
* privileged operation routing

This document is the canonical governance layer for:

* plugins
* providers
* browser automation
* FFmpeg execution
* network access
* subprocesses
* filesystem access
* extraction engines
* downloaders
* runtime services

This contract is mandatory for long-term maintainability, security, predictability, and plugin ecosystem stability.

---

# 2. Architectural Goals

The capability system exists to guarantee:

```text
1. Explicit authority
2. Least privilege
3. Runtime isolation
4. Predictable governance
5. Deterministic permission resolution
6. Auditable access control
7. Plugin ecosystem safety
8. Future remote execution compatibility
9. Multi-tenant compatibility
10. Sandboxed execution compatibility
```

The runtime MUST NEVER rely on:

* implicit trust
* unrestricted service access
* unrestricted provider access
* unrestricted filesystem access
* unrestricted subprocess execution
* unrestricted network access

---

# 3. Core Security Principle

## Fundamental Rule

```text
No component possesses authority unless explicitly granted.
```

Everything operates under:

```text
default deny
```

Authority is additive only.

---

# 4. Capability Model

---

## 4.1 Capability Definition

A capability is a typed authority token granting access to a bounded operation domain.

Capabilities are:

```text
explicit
typed
immutable
scoped
auditable
revocable
serializable
composable
```

---

## 4.2 Capabilities Are NOT Roles

The system does NOT use RBAC-style role systems.

The runtime uses:

```text
capability-based authority
```

Reason:

Roles become unstable in plugin ecosystems.

Capabilities remain composable and deterministic.

---

# 5. Capability Categories

---

# 5.1 Runtime Capabilities

Examples:

```text
runtime.events.publish
runtime.events.subscribe
runtime.cache.read
runtime.cache.write
runtime.metrics.emit
runtime.logging.write
runtime.config.read
runtime.config.watch
```

---

# 5.2 Filesystem Capabilities

Examples:

```text
fs.read
fs.write
fs.delete
fs.temp
fs.workspace
fs.cache
fs.downloads
```

Filesystem capabilities MUST always include scope constraints.

Example:

```text
fs.read:/workspace/cache
fs.write:/workspace/tmp
```

Global unrestricted filesystem access is forbidden.

---

# 5.3 Network Capabilities

Examples:

```text
network.http
network.websocket
network.dns
network.local
network.external
```

Network permissions MAY include:

```text
host allowlists
protocol restrictions
port restrictions
bandwidth constraints
timeout policies
```

Example:

```text
network.http:https://youtube.com
```

---

# 5.4 Process Execution Capabilities

Examples:

```text
process.spawn
process.ffmpeg
process.mpv
process.browser
```

General unrestricted subprocess execution is forbidden.

Only explicitly approved binaries MAY execute.

---

# 5.5 Browser Automation Capabilities

Examples:

```text
browser.launch
browser.navigate
browser.cookies.read
browser.storage.read
browser.download
```

Sensitive browser operations require elevated privilege.

---

# 5.6 Provider Access Capabilities

Examples:

```text
provider.youtube.read
provider.youtube.stream
provider.youtube.download
provider.reddit.read
provider.generic.http
```

Providers MUST NOT be globally accessible.

---

# 5.7 Download Capabilities

Examples:

```text
download.start
download.pause
download.cancel
download.stream
download.persist
```

---

# 5.8 Media Pipeline Capabilities

Examples:

```text
media.decode
media.encode
media.transcode
media.thumbnail.generate
media.stream
```

---

# 5.9 Database Capabilities

Examples:

```text
db.read
db.write
db.migrate
db.compact
```

Migration capabilities are privileged.

---

# 6. Capability Structure

---

## 6.1 Canonical Capability Shape

```python
Capability(
    namespace="fs",
    action="write",
    scope="/workspace/cache",
    constraints={...},
)
```

---

## 6.2 Capability Components

| Component   | Meaning                       |
| ----------- | ----------------------------- |
| namespace   | authority domain              |
| action      | permitted operation           |
| scope       | bounded resource range        |
| constraints | optional runtime restrictions |

---

# 7. Capability Resolution Semantics

---

## 7.1 Resolution Rule

Capability validation MUST occur:

```text
before operation execution
```

Never after execution begins.

---

## 7.2 Validation Pipeline

Validation order:

```text
1. identity validation
2. capability existence
3. scope validation
4. constraint validation
5. runtime policy validation
6. sandbox policy validation
7. supervision policy validation
```

---

## 7.3 Denial Semantics

If any validation stage fails:

```text
operation MUST fail immediately
```

No partial execution allowed.

---

# 8. Authority Ownership Model

---

# 8.1 Runtime Owns Root Authority

Only runtime bootstrap owns root authority.

All authority derives from runtime.

---

# 8.2 Plugins Never Own Root Authority

Plugins operate under delegated authority only.

Plugins MUST NEVER:

* self-elevate
* mint capabilities
* bypass validation
* mutate permission registries
* bypass sandbox rules

---

# 8.3 Services Operate Under Bounded Authority

Services receive only the capabilities required for operation.

Services MUST NOT inherit runtime-global authority.

---

# 9. Capability Grant Semantics

---

# 9.1 Grants Are Explicit

Capabilities MUST be granted explicitly during:

```text
bootstrap
plugin activation
service initialization
provider binding
task creation
worker spawn
```

Implicit inheritance is forbidden.

---

# 9.2 Capability Sources

Capabilities MAY originate from:

```text
runtime policy
plugin manifest
configuration
bootstrap contract
supervisor policy
sandbox policy
```

---

# 9.3 Capability Aggregation

Effective authority is the union of granted capabilities.

Conflicting capabilities resolve via:

```text
deny overrides allow
```

---

# 10. Plugin Permission Model

---

# 10.1 Plugin Manifests MUST Declare Required Capabilities

Example:

```yaml
capabilities:
  - network.http:https://youtube.com
  - fs.cache
  - process.ffmpeg
```

Undeclared capability usage MUST fail.

---

# 10.2 Plugin Activation Validation

Plugin activation requires:

```text
1. manifest validation
2. capability validation
3. policy approval
4. sandbox validation
5. dependency permission validation
```

Failure aborts activation.

---

# 10.3 Plugin Isolation

Plugins MUST NOT directly access:

* runtime internals
* other plugin memory
* service private state
* provider private state
* supervisor internals

All interactions MUST occur through approved contracts.

---

# 10.4 Plugin-to-Plugin Access

Plugins MUST communicate only via:

```text
events
service contracts
DTOs
approved extension APIs
```

Direct internal access is forbidden.

---

# 11. Provider Access Semantics

---

# 11.1 Providers Are Permission-Bound

Provider access MUST require explicit capability grants.

Example:

```text
provider.youtube.stream
```

---

# 11.2 Provider Isolation

Providers MUST NOT:

* access unrelated providers
* access runtime internals
* bypass service boundaries
* perform unrestricted network calls

---

# 11.3 Generic HTTP Providers

Generic HTTP access is high-risk.

Runtime MAY require:

```text
domain allowlists
rate limiting
sandboxing
traffic auditing
```

---

# 12. Restricted Runtime APIs

---

# 12.1 Internal Runtime APIs

Certain APIs are privileged-only:

```text
scheduler mutation
supervisor control
service registry mutation
capability registry mutation
runtime shutdown
worker orchestration
event bus internals
```

---

# 12.2 Public Runtime Surface

Plugins access runtime only through:

```text
RuntimeFacade
ServiceContracts
ProviderContracts
EventInterfaces
```

Never raw internals.

---

# 13. Sandbox Semantics

---

# 13.1 Sandbox Authority Boundary

Sandbox defines maximum authority ceiling.

Granted capabilities cannot exceed sandbox authority.

---

# 13.2 Sandbox Enforcement

Sandbox MAY enforce:

```text
filesystem isolation
network isolation
process isolation
memory limits
CPU quotas
timeout limits
thread limits
API restrictions
```

---

# 13.3 Sandbox Compatibility Requirement

All plugins MUST remain compatible with future sandboxed execution.

No plugin may assume:

```text
full local machine access
unrestricted subprocesses
global filesystem access
unrestricted network
```

---

# 14. Filesystem Governance

---

# 14.1 Filesystem Access Must Be Scoped

Filesystem access MUST use bounded virtual roots.

Example:

```text
/workspace/cache
/workspace/downloads
/workspace/temp
```

---

# 14.2 Forbidden Filesystem Operations

Plugins MUST NEVER:

* access arbitrary host paths
* access runtime secrets
* mutate runtime installation
* access user home directory
* bypass virtual roots

---

# 14.3 Temporary Storage

Temp storage MUST support:

```text
TTL cleanup
quota enforcement
ownership tracking
crash cleanup
```

---

# 15. Network Governance

---

# 15.1 Network Access Is Restricted

No component has implicit network access.

---

# 15.2 Allowed Network Policies

Policies MAY restrict:

```text
domains
ports
protocols
request rates
payload sizes
request concurrency
connection duration
```

---

# 15.3 Local Network Access

Local network access is privileged.

Example:

```text
network.local
```

This prevents accidental LAN abuse.

---

# 16. Subprocess Governance

---

# 16.1 Approved Executables Only

Only runtime-approved executables MAY spawn.

Example:

```text
ffmpeg
mpv
playwright browser binaries
```

Arbitrary shell execution is forbidden.

---

# 16.2 Process Isolation

Subprocesses MAY execute under:

```text
resource quotas
time limits
sandbox profiles
restricted env vars
restricted filesystem mounts
```

---

# 16.3 Shell Invocation

Shell execution MUST be avoided whenever possible.

Direct exec-style invocation is preferred.

---

# 17. FFmpeg Governance

---

# 17.1 FFmpeg Is Privileged Infrastructure

FFmpeg execution requires explicit capability:

```text
process.ffmpeg
```

---

# 17.2 FFmpeg Restrictions

Runtime MAY restrict:

```text
codec access
output locations
input protocols
resource usage
execution duration
```

---

# 18. Browser Automation Governance

---

# 18.1 Browser Automation Is High-Risk

Browser automation operates under elevated scrutiny.

---

# 18.2 Sensitive Browser Operations

The following require elevated capabilities:

```text
cookies.read
storage.read
credential access
download interception
session persistence
```

---

# 18.3 Browser Isolation

Browser sessions SHOULD support:

```text
ephemeral profiles
isolated storage
network filtering
download isolation
```

---

# 19. Capability Propagation

---

# 19.1 Authority Propagation Must Be Explicit

Capabilities MUST NOT propagate automatically across:

```text
threads
tasks
workers
events
services
plugins
```

---

# 19.2 Delegated Authority

Delegation MUST:

```text
reduce or preserve authority
```

Never elevate authority.

---

# 19.3 Capability Narrowing

Delegated capabilities SHOULD narrow:

```text
scope
duration
operations
resource limits
```

---

# 20. Temporal Permission Semantics

---

# 20.1 Time-Bound Capabilities

Capabilities MAY expire.

Example:

```text
download.persist لمدة 5 minutes
```

---

# 20.2 Revocation

Runtime MAY revoke capabilities dynamically.

Revocation MUST propagate safely.

---

# 20.3 Revocation Guarantees

Revoked capabilities MUST prevent:

```text
new operations
new allocations
new resource acquisition
```

Existing operations MAY terminate gracefully.

---

# 21. Observability & Auditability

---

# 21.1 Capability Usage Must Be Auditable

Runtime SHOULD emit structured events for:

```text
grant
deny
revocation
elevation attempts
sandbox violations
policy violations
```

---

# 21.2 Sensitive Operation Logging

Sensitive operations SHOULD produce audit logs.

Examples:

```text
filesystem writes
network access
browser credential access
subprocess execution
```

---

# 22. Failure Semantics

---

# 22.1 Permission Denial Is Deterministic

Permission failures MUST produce typed exceptions.

Example:

```python
CapabilityDeniedError
SandboxViolationError
ProviderAccessDeniedError
```

---

# 22.2 No Silent Downgrades

Runtime MUST NEVER silently reduce behavior.

Denied authority MUST surface explicitly.

---

# 23. Future Compatibility Requirements

This capability system MUST remain compatible with:

```text
remote execution
distributed workers
containerized runtimes
WASM sandboxing
multi-tenant execution
cloud orchestration
plugin marketplaces
zero-trust execution
```

---

# 24. Architectural Invariants

---

## The following invariants are mandatory.

### Authority

```text
No implicit authority exists.
```

### Security

```text
Default deny is universal.
```

### Plugins

```text
Plugins operate under delegated authority only.
```

### Filesystem

```text
Filesystem access is always scoped.
```

### Network

```text
Network access is always permission-bound.
```

### Runtime

```text
Runtime internals are never directly exposed.
```

### Sandboxing

```text
Sandbox defines the maximum authority boundary.
```

### Propagation

```text
Authority propagation is explicit only.
```

### Governance

```text
Capability validation occurs before execution.
```

### Isolation

```text
Components communicate through contracts only.
```

### Determinism

```text
Permission resolution is deterministic.
```

### Observability

```text
Sensitive authority usage is auditable.
```
