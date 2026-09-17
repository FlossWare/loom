# ADR 0004: Conformance is a first-class Loom deliverable

## Status

Accepted for implementation planning

## Context

Loom is intended to support independent implementations in multiple languages and environments. Tests tied to one implementation cannot establish interoperability.

## Decision

Loom will maintain a machine-checkable conformance suite that tests normative protocol semantics independently of implementation language and framework.

The initial conformance scope includes:

- Contract identity and compatibility;
- Requirement/Capability matching;
- Registration and Discovery;
- Provider/Builder acquisition;
- endpoint and binding invocation;
- dependency resolution;
- Plan composition;
- lifecycle behavior;
- Results;
- Evidence and provenance.

Implementation repositories may add local tests, but local tests do not replace protocol conformance.

## Consequences

A future `loom-java` can be validated against the same semantic expectations as `loom-ai`. Concrete platform compositions provide useful end-to-end integration tests, but they are not themselves the conformance suite.
