# HTTP/REST Binding Requirements for Loom

- **Status:** Proposed
- **Scope:** Requirements for an implementation that declares an HTTP/REST binding
- **Related:** [ADR-0031: REST Representation Contracts and API Evolution](https://github.com/FlossWare/engineering-standards/blob/main/adr/ADR-0031-rest-representation-contracts-and-api-evolution.md)

## Purpose and boundary

Loom core is transport- and representation-neutral. It does not define a canonical
HTTP API, require REST, or make JSON, OpenAPI, or any HTTP status code part of
Loom's language-neutral semantics.

This document records the minimum requirements for a future Loom implementation
that chooses to expose a Contract through HTTP/REST. It does **not** define
concrete endpoints or claim that a normative Loom HTTP binding currently exists.
The Python HTTP server in `loom-ai-python` is an implementation-specific binding,
not the definition of Loom's protocol.

These requirements are proposed pending acceptance of FlossWare ADR-0031.

## Binding declaration

An HTTP/REST binding MUST document:

- the Loom Contract and operations it exposes;
- the mapping from each operation/resource to HTTP methods and resource URLs;
- request and response representations and their schemas;
- validation and semantic failure behavior;
- HTTP status mapping for success, client errors, server errors, and execution outcomes;
- supported request and response media types;
- compatibility and deprecation expectations;
- authentication/authorization and the security boundary, or an explicit statement
  that the binding is restricted to a trusted local environment.

The mapping MUST preserve the underlying Contract semantics. A transport status
code MUST NOT silently change the meaning of a Loom Result or lifecycle state.

## Media types and negotiation

- A binding SHOULD use standard media types where they adequately describe the
  representation, including `application/json` for generic JSON.
- A binding MAY define a vendor media type when a stable, distinct representation
  contract needs explicit identification. A vendor type MUST have documented
  semantics and compatibility rules; it MUST NOT be introduced solely for each
  additive field or implementation release.
- Requests with a body MUST declare a supported `Content-Type`. An unsupported
  request representation SHOULD be rejected with `415 Unsupported Media Type`.
- Clients SHOULD declare acceptable response representations with `Accept`.
  If the server cannot provide any acceptable representation, it SHOULD return
  `406 Not Acceptable`.
- A server MUST NOT silently return a representation incompatible with the
  client's declared supported media type.
- Any media-type parameter used to identify a contract version MUST define
  compatibility, negotiation, and fallback behavior explicitly.

The exact supported media types and negotiation policy belong to the binding
contract, not to Loom core.

## HTTP error mapping

HTTP bindings SHOULD use RFC 9457 Problem Details with
`Content-Type: application/problem+json` for machine-readable HTTP errors where
appropriate.

A Problem Details response SHOULD provide a stable problem type and the HTTP
status, and MAY provide a human-readable title/detail and instance identifier.
The representation MUST NOT expose credentials, secrets, private reasoning, or
internal implementation details that the caller is not authorized to receive.

A binding MUST document how HTTP failures relate to protocol-level outcomes.
For example, malformed HTTP requests and unsupported representations are binding
errors; an executed operation that returns a Loom Result with a failure status is
an execution outcome. Those categories MUST NOT be conflated.

The exact status mapping is defined by each HTTP binding and its operation
contract. This document does not assign universal routes or make HTTP status codes
normative Loom Result values.

## Compatibility and evolution

- Existing resource URLs and representations MUST NOT be removed solely to adopt
  a preferred style or media type.
- Additive changes SHOULD preserve existing client behavior, including clients
  that validate responses strictly.
- A client requesting a specific representation contract MUST receive its
  documented semantics or an explicit negotiation error; the server MUST NOT
  silently reinterpret the request under an incompatible contract.
- Breaking representation changes MUST include migration/deprecation guidance
  where practical.
- Schemas and compatibility tests SHOULD be maintained independently of framework
  implementation details.
- Any migration from an existing JSON representation MUST be incremental and
  preserve current behavior until a separately documented compatibility decision
  authorizes a change.

Resource URL versioning MAY be retained when it provides a useful operational or
compatibility boundary. Stable resource identity SHOULD be preferred where
practical, but existing versioned URLs MUST NOT be removed merely for stylistic
reasons.

## Conformance

A binding that claims conformance to these requirements SHOULD have executable
tests or fixtures covering:

1. operation-to-resource mapping and request validation;
2. successful response representations and their declared media types;
3. unsupported `Content-Type` and unacceptable `Accept` behavior;
4. HTTP error mapping, including Problem Details where implemented;
5. compatibility of existing routes and representations;
6. equivalence of the underlying Loom Contract semantics across bindings;
7. security and redaction boundaries for errors and evidence.

These tests validate the HTTP binding. They do not replace Loom's language-neutral
conformance suite.

## Current status

The Loom core specification and architecture documents reviewed for this decision
do not define a normative HTTP route set or HTTP-specific data representation.
They define Endpoint URIs and Binding as concepts and explicitly state that
transport-specific assumptions do not belong in core semantics.

The current `loom-ai-python` server provides a concrete HTTP realization. Its
route inventory and current JSON/error behavior are documented in that repository;
those implementation details are not imported into this core binding document.

A future HTTP binding should be specified alongside its actual Contract operations
and schemas before it is treated as a supported interoperable binding.
