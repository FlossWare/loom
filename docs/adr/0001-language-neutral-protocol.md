# ADR 0001: Loom is the language-neutral protocol

## Status

Accepted

## Context

Loom originated as an implementation inside `loom-ai`, but the architecture now requires Loom to be a protocol and semantic model that can have multiple independent implementations.

The Python `loom-ai` implementation, HTTP server, and current execution classes are useful realizations, but allowing any of them to define Loom would make future implementations translations of Python rather than peers.

The architecture also requires pluggable endpoint bindings, implementation discovery, implementation builders/providers, recursive composition, and a conformance model that is independent of language and deployment topology.

## Decision

`FlossWare/loom` is the canonical home of the Loom protocol and semantic specification.

Loom defines language-neutral concepts and semantics including:

- Contracts;
- Implementations;
- Capabilities;
- Requirements;
- Registration;
- Discovery;
- Providers/Builders;
- Endpoint URIs;
- Bindings;
- Plans;
- Execution;
- Results;
- Evidence;
- lifecycle and conformance semantics.

`FlossWare/loom-ai` is an implementation and AI-oriented ecosystem built on Loom. Its Python types are not normative Loom definitions.

A future implementation such as `loom-java` is a peer implementation and MUST be able to conform to Loom without changing the protocol because of language or framework differences.

## Binding decision

The endpoint is identified by a URI. A binding interprets the URI scheme and carries the contract operation to the endpoint.

HTTP/REST, JMS, in-process invocation, and other mechanisms are peers. No transport is privileged by Loom.

OpenAPI may describe an HTTP-facing realization, but OpenAPI does not define Loom.

## Composition decision

A Plan is an Implementation governed by the same protocol rules as other Implementations. It is not a privileged orchestration primitive.

Execution systems resolve Requirements through available Capabilities, discovered Implementations, and Providers/Builders. The protocol does not hard-code a universal execution sequence.

## Conformance decision

Machine-checkable conformance is a first-class protocol deliverable. A reference implementation is useful, but matching its classes or internal architecture is not sufficient evidence of conformance.

## Consequences

### Positive

- Loom can have independent implementations in multiple languages.
- `loom-ai` can evolve without becoming the specification.
- Transport and deployment can vary without redefining contracts.
- Fullsend can be validated as a platform composition rather than as the definition of Loom.
- Other ecosystems, including workflow engines, can use Loom without adopting AI-specific semantics.

### Negative

- The semantic specification must be more precise than the existing Python implementation.
- Compatibility and protocol evolution become explicit responsibilities.
- Conformance requires work independent of implementation tests.

## Rejected alternatives

### Keep Loom defined in `loom-ai`

Rejected. `loom-ai` is an AI-oriented implementation and must not own the generic protocol definition.

### Make REST the Loom API

Rejected. REST is one possible binding and would unnecessarily constrain other URI schemes and local implementations.

### Define Loom as a custom markup language

Rejected for now. The semantic model comes first. Existing standards will be evaluated for individual representation and binding layers before any new language is invented.

### Make every Contract a microservice

Rejected. A Contract boundary does not imply a deployment boundary.
