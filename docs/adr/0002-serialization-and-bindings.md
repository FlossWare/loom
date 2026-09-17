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

## Open work

Evaluate existing standards for:

- contract/data schemas;
- operation descriptions;
- discovery and capability metadata;
- asynchronous messaging;
- workflow/orchestration integration;
- conformance testing.
