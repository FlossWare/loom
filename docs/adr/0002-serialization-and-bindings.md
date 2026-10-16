# ADR 0002: Serialization and bindings are realization layers

## Status

Accepted for investigation

## Context

Loom needs machine-readable representations of contracts and operations, but selecting a single serialization or interface description language as the definition of Loom would couple the semantic model to a representation or transport.

OpenAPI is useful for HTTP-facing APIs. JSON Schema is useful for data shapes. Other mechanisms may be better suited to messaging or other bindings.

## Decision

The Loom semantic model remains normative and representation-independent.

Serialization and interface-description mechanisms are realization layers. A realization MAY use an established standard when that standard accurately represents the relevant Loom semantics without changing them.

OpenAPI is a candidate for HTTP binding descriptions, not for defining Loom itself.

Any future schema or IDL adopted by Loom MUST preserve the distinction between:

```text
Loom semantics
     |
     +-- representation
     |
     +-- binding
     |
     +-- implementation
```

## Consequences

- The protocol can support multiple representations and bindings.
- Existing standards can be reused where appropriate.
- No custom Loom markup is required merely to make the protocol machine-readable.
- Conformance must test semantics rather than serialized syntax alone.

## Proposed HTTP/REST binding profile

The following profile proposes requirements for future HTTP/REST bindings. It does not impose HTTP on Loom core or assert that this repository currently defines an HTTP API. When an implementation chooses HTTP/REST, its binding contract MUST document resource/operation mapping, request and response representations, media negotiation, protocol errors, and compatibility expectations. This is a binding requirement only: HTTP, JSON, OpenAPI, and vendor media types MUST NOT become normative requirements of Loom core.

HTTP bindings SHOULD use standard media types where sufficient, SHOULD use RFC 9457 Problem Details for machine-readable HTTP errors where appropriate, and SHOULD define explicit `406 Not Acceptable` and `415 Unsupported Media Type` behavior. A binding MUST distinguish transport/protocol failures from Loom domain outcomes and preserve contract semantics through serialization.

Adoption of the shared FlossWare [ADR-0031: REST Representation Contracts and API Evolution](https://github.com/FlossWare/engineering-standards/blob/main/adr/ADR-0031-rest-representation-contracts-and-api-evolution.md) is conditional on that ADR being accepted. Existing HTTP implementations must be inventoried and migrated incrementally; this ADR does not invent routes or require an HTTP implementation.

## Open work

Evaluate existing standards for:

- contract/data schemas;
- operation descriptions;
- discovery and capability metadata;
- asynchronous messaging;
- workflow/orchestration integration;
- conformance testing.
