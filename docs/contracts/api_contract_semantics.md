# `docs/contracts/api_contract_semantics.md`

# API & External Contract Semantics

---

# 1. Purpose

This document defines the authoritative external contract model of the runtime.

It specifies:

* public API stability guarantees
* semantic versioning rules
* compatibility windows
* deprecation policy
* transport compatibility semantics
* SDK compatibility expectations
* plugin API stability rules
* CLI compatibility guarantees
* HTTP API evolution policy
* external contract governance

This document governs all externally consumable interfaces including:

* CLI
* HTTP APIs
* plugin APIs
* SDKs
* automation interfaces
* event interfaces
* extension contracts
* serialization contracts
* RPC interfaces
* future remote APIs

This is the canonical external compatibility governance layer.

---

# 2. Architectural Goals

The external contract system exists to guarantee:

```text id="71gh6x"
1. Predictable integration behavior
2. Stable external interfaces
3. Safe ecosystem evolution
4. Deterministic compatibility guarantees
5. Controlled breaking changes
6. Long-term SDK maintainability
7. Plugin ecosystem stability
8. Explicit version governance
9. Transport independence
10. Operational reliability
```

---

# 3. Core Principles

---

## 3.1 Public Contracts Are Stable Commitments

Public APIs are long-term compatibility promises.

Public contracts MUST NOT change casually.

---

## 3.2 Internal and External Contracts Are Distinct

Internal DTOs are not automatically public APIs.

Only explicitly exported interfaces become public contracts.

---

## 3.3 Compatibility Is Intentional

Compatibility guarantees MUST be explicitly defined.

Undefined compatibility behavior is forbidden.

---

## 3.4 Transport Must Not Define Domain Semantics

Domain semantics MUST remain transport-independent.

HTTP, CLI, RPC, and SDK layers are transport adapters only.

---

# 4. Public Contract Taxonomy

---

# 4.1 Public APIs

Interfaces intended for external consumers.

Examples:

```text id="3exr1e"
HTTP API
CLI commands
plugin interfaces
SDK interfaces
automation APIs
```

Public APIs require compatibility guarantees.

---

# 4.2 Internal APIs

Runtime-private interfaces.

Examples:

```text id="uz7j9u"
internal services
worker coordination
runtime orchestration
private repositories
```

Internal APIs MAY evolve freely.

---

# 4.3 Experimental APIs

Experimental APIs have reduced stability guarantees.

Experimental status MUST be explicit.

Examples:

```text id="2w8yxt"
experimental plugins
beta streaming APIs
preview SDK features
```

---

# 4.4 Deprecated APIs

Deprecated APIs remain temporarily supported during migration windows.

Deprecation MUST be explicit and observable.

---

# 5. Public API Stability Semantics

---

# 5.1 Stable APIs

Stable APIs MUST preserve backward compatibility within the same major version.

Breaking changes are forbidden inside a major line.

---

# 5.2 Compatibility Definition

Backward compatibility means existing valid consumers continue functioning without modification.

---

# 5.3 Stability Scope

Stability guarantees apply to:

```text id="f0g4u6"
request formats
response formats
field meanings
error semantics
CLI flags
plugin contracts
SDK interfaces
event payloads
```

---

# 5.4 Stability Exclusions

The following MAY evolve without compatibility guarantees unless explicitly public:

```text id="r98r83"
internal logs
internal metrics
private DTOs
private service contracts
debug output
```

---

# 6. Semantic Versioning Semantics

---

# 6.1 Canonical Version Format

The runtime MUST use semantic versioning:

```text id="w8jgj7"
MAJOR.MINOR.PATCH
```

Example:

```text id="jv0o54"
2.4.1
```

---

# 6.2 Major Versions

Major versions indicate breaking changes.

Breaking external compatibility requires major version increment.

---

# 6.3 Minor Versions

Minor versions MAY add:

```text id="pn6m3n"
new endpoints
optional fields
new CLI commands
new plugin hooks
new SDK capabilities
```

Minor releases MUST remain backward compatible.

---

# 6.4 Patch Versions

Patch versions MUST contain only:

```text id="o6p1lb"
bug fixes
security fixes
performance improvements
internal refactors
```

Patch releases MUST preserve full compatibility.

---

# 7. Breaking Change Semantics

---

# 7.1 Breaking Changes Require Major Versions

Examples of breaking changes:

```text id="bjlwmh"
field removal
field type changes
semantic behavior changes
endpoint removal
CLI flag removal
plugin hook removal
event schema changes
```

---

# 7.2 Silent Breaking Changes Are Forbidden

Behavioral semantic changes count as breaking changes even if schemas remain identical.

---

# 7.3 Additive Changes

The following are generally non-breaking:

```text id="qmp8ck"
optional response fields
new endpoints
new optional CLI flags
new optional event fields
```

---

# 8. Compatibility Window Semantics

---

# 8.1 Compatibility Windows Must Be Defined

Public APIs MUST define support duration expectations.

---

# 8.2 Stable Support Window

Stable APIs SHOULD remain supported for at least:

```text id="uzxg25"
one major release cycle
```

after deprecation.

---

# 8.3 Plugin Compatibility Window

Plugin APIs SHOULD support:

```text id="w0n87e"
cross-minor compatibility
```

within a major release line.

---

# 8.4 SDK Compatibility Window

SDKs SHOULD remain compatible with:

```text id="q1m52j"
supported API major versions
```

during their declared lifecycle.

---

# 9. Deprecation Policy

---

# 9.1 Deprecation Must Be Explicit

Deprecated interfaces MUST provide:

```text id="2o1yzc"
deprecation warning
replacement guidance
removal timeline
migration path
```

---

# 9.2 Deprecation Lifecycle

Canonical lifecycle:

```text id="r2h8ux"
stable
-> deprecated
-> sunset announced
-> removed
```

---

# 9.3 Deprecated Feature Behavior

Deprecated features MUST continue functioning during support windows.

Silent degradation is forbidden.

---

# 9.4 Deprecation Visibility

Deprecation SHOULD surface through:

```text id="nys32z"
CLI warnings
HTTP headers
documentation
SDK warnings
plugin validation warnings
```

---

# 10. Transport Compatibility Policy

---

# 10.1 Transport Independence

Public semantics MUST remain transport-independent.

Equivalent operations SHOULD behave consistently across:

```text id="6kv2gk"
CLI
HTTP
SDK
RPC
future transports
```

---

# 10.2 Transport Adapters

Transport layers MUST act as adapters only.

Business logic MUST NOT live inside transport layers.

---

# 10.3 Serialization Stability

Transport payloads MUST use stable serialization semantics.

---

# 10.4 Cross-Transport Consistency

Equivalent operations SHOULD preserve:

```text id="sdvxxk"
error semantics
validation behavior
authorization semantics
state transitions
```

---

# 11. CLI Contract Semantics

---

# 11.1 CLI Is a Public API

CLI behavior is externally consumable and version-governed.

---

# 11.2 Stable CLI Guarantees

Stable CLI contracts include:

```text id="o5o0jz"
command names
flag names
exit codes
structured output formats
```

---

# 11.3 CLI Human vs Machine Output

Human-readable output MAY evolve.

Machine-readable output MUST define stable contracts.

Examples:

```text id="k0v0e2"
JSON mode
structured event mode
automation output mode
```

---

# 11.4 Exit Code Stability

Exit codes MUST preserve semantic meaning across compatible versions.

---

# 12. HTTP API Semantics

---

# 12.1 HTTP APIs Must Be Versioned

HTTP APIs SHOULD expose explicit versions.

Examples:

```text id="7vv49v"
/api/v1/
/api/v2/
```

---

# 12.2 HTTP Compatibility

HTTP APIs MUST preserve:

```text id="9lhxjv"
status code semantics
response schemas
authentication behavior
pagination behavior
```

within stable versions.

---

# 12.3 Optional Fields

Clients MUST tolerate unknown optional fields.

Servers SHOULD preserve additive compatibility.

---

# 12.4 Error Contracts

HTTP error payloads MUST remain schema-stable.

---

# 13. Plugin API Semantics

---

# 13.1 Plugin APIs Are Strict Compatibility Contracts

Plugin ecosystems require strong compatibility guarantees.

---

# 13.2 Plugin Interface Stability

Stable plugin contracts MUST preserve:

```text id="pjlwm3"
hook signatures
capability semantics
lifecycle semantics
provider contracts
event schemas
```

---

# 13.3 Plugin Negotiation

Plugins SHOULD declare:

```text id="mjlwmr"
minimum supported runtime version
maximum supported runtime version
required capability version
```

---

# 13.4 Plugin Isolation

Plugins MUST NOT depend on:

```text id="67htav"
private runtime internals
private service APIs
undocumented DTOs
private implementation details
```

---

# 14. SDK Semantics

---

# 14.1 SDKs Are Compatibility Layers

SDKs MUST abstract transport complexity from consumers.

---

# 14.2 SDK Stability

Stable SDKs MUST preserve:

```text id="i1fclx"
method signatures
error semantics
authentication flow
serialization semantics
```

---

# 14.3 SDK Transport Independence

SDK internals MAY evolve without breaking public SDK contracts.

---

# 14.4 Generated SDKs

Generated SDKs MUST derive from authoritative API schemas.

Manual drift is forbidden.

---

# 15. Event Contract Semantics

---

# 15.1 Public Events Are APIs

Externally consumable events are public contracts.

---

# 15.2 Event Compatibility

Stable event contracts MUST preserve:

```text id="8ek0e8"
event name
event ordering guarantees
field semantics
timestamp semantics
```

---

# 15.3 Event Evolution

Event schemas SHOULD evolve additively.

Field removal requires major version changes.

---

# 16. Serialization Compatibility

---

# 16.1 Stable Serialization Formats

Public APIs SHOULD use stable serialization formats.

Examples:

```text id="3m4ok3"
JSON
msgpack
protobuf
```

---

# 16.2 Serialization Evolution

Serialized payloads SHOULD tolerate:

```text id="x3vk1y"
unknown fields
optional fields
schema extension
```

---

# 16.3 Unsafe Serialization Forbidden

Unsafe runtime-bound formats are forbidden for public contracts.

Examples:

```text id="gmjlwm"
pickle
raw memory dumps
runtime object serialization
```

---

# 17. Capability & Authorization Compatibility

---

# 17.1 Authorization Semantics Are Contractual

Public authorization behavior MUST remain stable.

---

# 17.2 Capability Evolution

New capabilities MAY be added additively.

Capability removal requires migration policy.

---

# 17.3 Permission Failure Semantics

Authorization failures MUST remain semantically stable.

---

# 18. Documentation Semantics

---

# 18.1 Public APIs Require Documentation

Stable public APIs MUST define:

```text id="fjlwm3"
version
stability status
compatibility guarantees
deprecation state
examples
error semantics
```

---

# 18.2 Documentation Drift

Documentation MUST evolve alongside public contracts.

Undocumented breaking behavior is forbidden.

---

# 19. Testing & Compatibility Validation

---

# 19.1 Compatibility Tests Are Mandatory

Stable public APIs SHOULD include:

```text id="gjlwm8"
contract tests
snapshot tests
schema compatibility tests
migration tests
```

---

# 19.2 Breaking Change Detection

CI SHOULD detect:

```text id="0ekjlwm"
schema changes
signature changes
event contract changes
CLI contract changes
```

---

# 20. Observability & Auditability

---

# 20.1 API Version Visibility

Public systems SHOULD expose:

```text id="3jlwm0"
API version
runtime version
compatibility state
deprecation status
```

---

# 20.2 Compatibility Events

Runtime SHOULD emit compatibility-related audit events.

Examples:

```text id="jlwm98"
deprecated API usage
unsupported plugin load
version negotiation failure
```

---

# 21. Failure Semantics

---

# 21.1 Compatibility Violations Must Fail Explicitly

Version incompatibility MUST produce typed failures.

Examples:

```python id="jlwm87"
IncompatibleApiVersionError
PluginCompatibilityError
UnsupportedContractVersionError
```

---

# 21.2 Undefined Compatibility Forbidden

APIs MUST NOT expose undefined compatibility behavior.

---

# 21.3 Graceful Negotiation Failure

Version negotiation failures SHOULD fail safely and observably.

---

# 22. Future Compatibility Requirements

This contract system MUST remain compatible with:

```text id="3jlwm1"
remote runtimes
distributed orchestration
cloud APIs
plugin marketplaces
multi-runtime SDKs
WASM execution
RPC transports
future protocol layers
```

---

# 23. Architectural Invariants

---

## Stability

```text id="jlwm12"
Public APIs are long-term compatibility commitments.
```

---

## Determinism

```text id="jlwm13"
Compatibility behavior is explicitly defined.
```

---

## Versioning

```text id="jlwm14"
Breaking changes require major version increments.
```

---

## Deprecation

```text id="jlwm15"
Deprecated APIs remain functional during support windows.
```

---

## Transport Independence

```text id="jlwm16"
Domain semantics remain transport-independent.
```

---

## Plugin Safety

```text id="jlwm17"
Plugins depend only on stable documented contracts.
```

---

## SDK Safety

```text id="jlwm18"
SDKs abstract transport complexity behind stable contracts.
```

---

## Serialization

```text id="jlwm19"
Public serialization formats remain stable and evolvable.
```

---

## Documentation

```text id="jlwm20"
Stable APIs are fully documented and version-governed.
```

---

## Governance

```text id="jlwm21"
Compatibility validation is part of runtime governance.
```
