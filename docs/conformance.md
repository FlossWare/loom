# Loom Conformance

Conformance is the mechanism by which independent Loom implementations demonstrate interoperability.

The suite will be developed against the normative semantics, not against `loom-ai` implementation classes.

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

The first complete implementation target is `loom-ai`, followed by a deliberately independent implementation path suitable for Java.
