# ADR-0007: Contract Representation Layers

Status: Proposed

## Context

Loom must support independent implementations without making a programming language, serialization format, or transport the definition of the protocol. A contract therefore needs both precise semantics and machine-checkable representations.

## Decision

Loom contracts are expressed through four complementary layers:

1. Normative semantic specification.
2. Machine-readable JSON Schemas for structural artifacts.
3. Executable conformance tests and fixtures for behavioral obligations.
4. Protocol bindings such as OpenAPI for HTTP exposure.

The semantic contract is authoritative for meaning. JSON Schema is authoritative for the structure of serialized artifacts. Conformance is authoritative for executable behavioral verification. A protocol binding is authoritative only for its transport realization.

OpenAPI is therefore a binding, not the definition of Loom.

The same layering applies to domain repositories such as loom-ai. Domain contracts may add domain semantics while preserving foundational Loom semantics.

## Consequences

Implementations can be written in Python, Java, Erlang, or another language without inheriting a language-specific contract. HTTP, messaging, and in-process implementations can expose the same semantics. Schema validation can catch structural incompatibilities, while conformance tests catch behavioral incompatibilities.

The contract repository must not define semantics solely through an implementation API or OpenAPI document.
