# Loom

**Loom is a language-neutral protocol and execution model for discovering, acquiring, composing, and invoking implementations that satisfy contracts.**

Loom is not an AI framework, a Python application, an HTTP API, or a mandatory microservice architecture.

An implementation may be written in Python, Java, Erlang, or another language. A binding may use HTTP/REST, JMS, another URI-addressed transport, or in-process invocation. Those are realizations of Loom, not definitions of it.

## Repository family

Loom follows the FlossWare contract-centric repository convention:

    loom
    loom-python
    loom-ai
    loom-ai-python

- **loom**: foundational, language-neutral Loom protocol and semantic contract.
- **loom-python**: Python implementation of the Loom contract.
- **loom-ai**: AI-domain contracts and semantics built on Loom.
- **loom-ai-python**: Python implementation of the Loom AI contracts.

Future implementations are peers, not replacements for the language-neutral contract:

    loom-java
    loom-erlang
    loom-ai-java
    loom-ai-erlang

The repository naming and layering rule is defined by FlossWare engineering standard ADR-0024.

## Architecture

    Loom
      |
      +-- Contracts
      +-- Discovery
      +-- Invocation
      +-- Providers/Builders
      +-- Implementations
      +-- Bindings
      +-- Plans
      +-- Results / Evidence

The core model is intentionally recursive. Implementations are governed by the same protocol rules regardless of their internal form. A Plan may therefore compose other implementations without becoming a privileged primitive.

## Repository boundary

loom is the normative home of Loom itself: protocol semantics, binding semantics, and conformance requirements.

AI-specific semantics belong in loom-ai. Language implementations belong in the corresponding -{language} repository. loom must remain independent of Python, Java, Erlang, frameworks, and vendors.

## Core principles

1. **Semantics before serialization.** The normative model is independent of JSON, YAML, OpenAPI, Protobuf, or any other representation.
2. **Language neutrality.** Contracts do not encode Python, Java, Erlang, framework, or vendor assumptions.
3. **Transport neutrality.** An endpoint is identified by a URI. A binding interprets the URI scheme and carries the contract operation.
4. **Discovery is normative.** Registry technology is replaceable, but discovery semantics are part of Loom.
5. **Builders are peers of running implementations.** Discovery may resolve either an existing implementation or a provider capable of acquiring/building one.
6. **Plans are implementations.** Composition and execution planning use the same protocol model rather than introducing a special orchestration primitive.
7. **Evidence is first-class.** Results and evidence are language-neutral artifacts that support verification, evaluation, and audit.
8. **Conformance matters.** Interoperability is demonstrated by machine-checkable protocol conformance, not by matching one reference implementation's classes.

## Contract representation

A Loom contract is expressed through complementary layers:

1. **Normative semantics** define meaning, obligations, compatibility, and observable behavior.
2. **Machine-readable schemas** define the structure of contract artifacts. JSON Schema is the initial structural representation.
3. **Executable conformance** verifies behavioral obligations that schemas cannot express.
4. **Protocol bindings** define how the same contract is exposed through a transport. OpenAPI is an HTTP binding, not the definition of Loom.

No single serialization or transport format defines Loom.

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

The repository is intentionally specification-first. The initial work establishes the semantic vocabulary, contract representation layers, and boundaries before implementation is added.

See docs/specification.md for the current normative model, docs/contract-representation.md for the representation layers, and docs/adr/0001-language-neutral-protocol.md for the architectural decision establishing this repository as the home of Loom itself.
