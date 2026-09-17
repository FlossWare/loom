# Conformance Fixtures

Conformance fixtures are machine-readable test inputs and expected outcomes for Loom protocol semantics.

They are **test artifacts**, not a Loom wire format. A fixture may be represented as YAML or JSON, and an implementation-specific adapter may translate it into the native test environment. The fixture's semantic meaning is independent of that representation.

## Fixture structure

A fixture SHOULD contain these fields:

```yaml
id: discovery-requirement-satisfied-001
semantic_area: discovery
contract:
  id: example.echo
  version: 1.0
requirement:
  capability: example.echo
expected:
  outcome: satisfied
  selected_implementation: example.echo.impl.1
```

The exact field vocabulary is provisional until the corresponding protocol semantics are frozen. Once the semantic model is accepted, fixture fields that represent normative concepts become part of the conformance contract.

## Required fixture properties

Each fixture MUST be:

- deterministic;
- independent of implementation language;
- independent of a particular registry or transport;
- explicit about the semantic area under test;
- explicit about expected success or failure;
- suitable for execution by more than one implementation.

Fixtures SHOULD include both positive and negative cases.

## Initial fixture categories

The suite should grow from the protocol's semantic model in this order:

1. Contract identity and compatibility
2. Capability and Requirement matching
3. Registration and Discovery
4. Provider/Builder acquisition
5. Endpoint and binding resolution
6. Dependency resolution
7. Plan composition
8. Lifecycle transitions
9. Result semantics
10. Evidence and provenance
11. Protocol failures

Each category should include boundary and rejection cases, not merely successful examples.

## Adapter boundary

A conformance adapter is responsible for translating a fixture into the implementation under test. It MUST NOT change the expected protocol semantics to accommodate implementation-specific behavior.

For example, a `loom-ai` adapter may construct Python objects while a future `loom-java` adapter constructs Java objects. Both execute the same semantic fixture and evaluate the same expected outcome.

## Relationship to the normative specification

This document describes the test mechanism. It does not freeze unresolved protocol semantics.

The normative specification must first define the meaning of matching, lifecycle transitions, protocol failures, evidence, and other required behaviors. Conformance fixtures then turn those definitions into executable interoperability tests.

That ordering is deliberate. Otherwise the test suite becomes a second, accidental specification, which is precisely the sort of architectural archaeology Loom is intended to avoid.
