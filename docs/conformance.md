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
- Implementation lifecycle and Execution lifecycle as distinct state machines
- Valid transitions, terminal immutability, and stable Execution identity
- Result success/failure semantics independent of process completion
- Evidence required to substantiate successful Results and provenance redaction
- Failure classification, cancellation, deadline, and continuation behavior
- Failure and protocol error behavior
- External invocation boundary where declared by a Contract:
  - stable execution identity and lifecycle observation;
  - preservation of Result, Evidence, and provenance through a Binding;
  - continuation from persisted state when durable continuation is promised;
  - cancellation/deadline semantics where supported;
  - separation of protocol failures from execution outcomes;
  - documented authentication, authorization, and trust boundaries

## Implementation model

The suite should expose protocol-level fixtures and assertions that can be consumed by independent implementations. A language-specific adapter may translate those fixtures into the native test environment, but the expected semantics remain shared.

The first complete implementation target is loom-python. AI-specific implementations are a separate domain layer and are not required to define Loom conformance.

A future loom-java or loom-erlang implementation must be able to exercise the same conformance semantics without depending on Python implementation details.


## Binding-specific conformance profiles

Core conformance verifies Loom semantics independently of transport and serialization. A binding-specific profile verifies that a chosen transport preserves those semantics without making the transport normative for Loom itself.

### HTTP/REST profile

The `loom` repository currently defines no normative HTTP routes or HTTP execution API. An implementation that later provides an HTTP/REST binding must document and test that binding separately. The profile must reference the proposed [FlossWare ADR-0031: REST Representation Contracts and API Evolution](https://github.com/FlossWare/engineering-standards/blob/main/adr/ADR-0031-rest-representation-contracts-and-api-evolution.md), subject to its adoption through the organization-wide ADR process.

Where an HTTP binding exists, its conformance fixtures should cover:

- contract operation to resource/method mapping;
- request and response schemas and media types;
- `Accept` and `Content-Type` behavior, including `406 Not Acceptable` and `415 Unsupported Media Type` where applicable;
- documented machine-readable errors, using RFC 9457 Problem Details where appropriate;
- distinction between HTTP/protocol failures and domain-level execution outcomes;
- compatibility behavior for supported representations and versions;
- preservation of Loom lifecycle, result, evidence, and provenance semantics through serialization.

These checks are conditional on a binding being implemented. Core conformance must not require HTTP, JSON, OpenAPI, a vendor media type, or a particular URL layout.
