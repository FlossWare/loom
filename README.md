# Loom

**Loom is a language-neutral protocol and execution model for discovering, acquiring, composing, and invoking implementations that satisfy contracts.**

Loom is not an AI framework, a Python application, an HTTP API, or a mandatory microservice architecture.

An implementation may be written in Python, Java, Erlang, or another language. A binding may use HTTP/REST, JMS, another URI-addressed transport, or in-process invocation. Those are realizations of Loom, not definitions of it.

## Architecture

```text
                         Loom
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
   Contracts          Discovery          Invocation
       │                  │                  │
   Requirements      Providers/Builders    Bindings
   Capabilities          │                  │
       │             Implementations      URI
       └──────────────────┼──────────────────┘
                          │
                       Plans
                          │
                 Results / Evidence
```

The core model is intentionally recursive. A Worker, Plan, service, builder, or other implementation is governed by the same protocol rules. A Plan may therefore compose other implementations without becoming a privileged primitive.

## Repository boundaries

- **`loom`**: the normative Loom protocol, semantic model, binding model, and conformance requirements.
- **`loom-ai`**: an AI-oriented implementation of Loom, including Workers, Arbiters, model capabilities, and AI-specific realizations.

`loom-ai` must not become the de facto specification for Loom. A future `loom-java` should be able to implement the same semantics from this repository without reverse-engineering Python classes.

## Core principles

1. **Semantics before serialization.** The normative model is independent of JSON, YAML, OpenAPI, Protobuf, or any other representation.
2. **Language neutrality.** Contracts do not encode Python, Java, Erlang, framework, or vendor assumptions.
3. **Transport neutrality.** An endpoint is identified by a URI. A binding interprets the URI scheme and carries the contract operation.
4. **Discovery is normative.** Registry technology is replaceable, but discovery semantics are part of Loom.
5. **Builders are peers of running implementations.** Discovery may resolve either an existing implementation or a provider capable of acquiring/building one.
6. **Plans are implementations.** Composition and execution planning use the same protocol model rather than introducing a special orchestration primitive.
7. **Evidence is first-class.** Results and evidence are language-neutral artifacts that support verification, evaluation, and audit.
8. **Conformance matters.** Interoperability is demonstrated by machine-checkable protocol conformance, not by matching one reference implementation's classes.

## What Loom does not define

Loom does not require:

- AI or model providers
- a particular programming language or runtime
- HTTP/REST
- a central registry service
- a specific registry technology
- a particular serialization format
- a microservice for every contract
- provider credentials or vendor SDKs
- AI prompting or coding-agent UX
- workflow semantics belonging to a higher-level orchestration language such as BPEL

## Specification status

The repository is intentionally specification-first. The initial work establishes the semantic vocabulary and boundaries before implementation is added.

See [`docs/specification.md`](docs/specification.md) for the current normative model and [`docs/adr/0001-language-neutral-protocol.md`](docs/adr/0001-language-neutral-protocol.md) for the architectural decision establishing this repository as the home of Loom itself.
