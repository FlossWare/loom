# Loom Conformance

Conformance is the mechanism by which independent Loom implementations demonstrate interoperability.

The suite will be developed against the normative semantics in this repository, not against implementation classes in a language or domain repository.

## Initial areas

- Contract identity and version compatibility
- Requirement/Capability matching
- Registration
- Discovery
- Provider/Builder acquisition
- Endpoint URI resolution
- Binding invocation
- Dependency resolution
- Plan composition
- Lifecycle transitions
- Result semantics
- Evidence and provenance
- Failure and protocol error behavior

## Implementation model

The suite should expose protocol-level fixtures and assertions that can be consumed by independent implementations. A language-specific adapter may translate those fixtures into the native test environment, but the expected semantics remain shared.

The first complete implementation target is loom-python. AI-specific implementations are a separate domain layer and are not required to define Loom conformance.

A future loom-java or loom-erlang implementation must be able to exercise the same conformance semantics without depending on Python implementation details.
