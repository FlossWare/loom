# Loom Protocol Specification

## Status

This document is the initial normative semantic model for Loom. It deliberately does not select a programming language, serialization format, registry product, deployment topology, or privileged transport.

## 1. Purpose

Loom defines the semantics for interoperable participants that expose, discover, acquire, compose, and invoke implementations satisfying contracts.

A Loom implementation may be entirely in-process or distributed across processes, hosts, runtimes, or networks. Distribution is an implementation and deployment choice, not a protocol requirement.

## 2. Core vocabulary

### 2.1 Contract

A **Contract** is the stable protocol definition that describes what an implementation offers and how another participant may interact with it.

A Contract defines, at minimum:

- stable identity;
- version and compatibility rules;
- operations and their semantics;
- request shape and validation;
- response shape and semantics;
- protocol-level failure behavior;
- requirements for provenance or evidence when applicable.

A Contract MUST be independent of implementation language, runtime, framework, vendor SDK, and transport.

A Contract does not imply a process, network endpoint, class, object, or microservice.

### 2.2 Implementation

An **Implementation** is a realization that claims to satisfy a Contract.

An Implementation may be local or remote and may itself compose other Implementations.

An Implementation MUST be evaluated against the Contract semantics it claims to satisfy.

### 2.3 Capability

A **Capability** is a declared property or service an Implementation provides and that may be used when resolving requirements.

Capabilities are protocol-level declarations. Their concrete representation is intentionally left open until matching, versioning, cardinality, and compatibility rules are finalized.

### 2.4 Requirement

A **Requirement** expresses a condition that must be satisfied before an Implementation or Plan can execute correctly.

A Requirement may be satisfied by an available Capability or by acquiring/building an Implementation that provides the required Capability.

Requirement-to-Capability matching is normative protocol behavior and MUST NOT depend on implementation language.

### 2.5 Registration

A **Registration** declares that an Implementation is available for discovery.

Conceptually:

```text
contract
contract-version
implementation-id
endpoint-uri
capabilities
metadata
```

Metadata may contain implementation-specific information, but interoperability MUST NOT depend on language-specific metadata.

### 2.6 Discovery

**Discovery** resolves a Requirement or Contract request to one or more suitable Registrations.

Discovery is a normative Loom capability even though registry technology is not.

A discovery implementation may use:

- in-memory state;
- files;
- databases;
- directory services;
- network services;
- another suitable mechanism.

Loom does not require a central registry.

### 2.7 Provider / Builder

A **Provider** or **Builder** is an Implementation capable of acquiring or constructing another Implementation that satisfies a requested Contract or Requirement.

This extends discovery beyond the question "what is already running?" to the question "who can provide an implementation satisfying this requirement?"

The acquisition/build operation remains governed by a Contract. Builders do not receive special protocol status merely because they create other Implementations.

### 2.8 Endpoint

An **Endpoint** identifies where an Implementation may be invoked. It is represented by a URI.

The URI scheme identifies or selects the binding mechanism.

For example:

```text
https://example/loom/service
jms://broker/loom/service
```

These are examples of endpoint addressing, not a requirement that Loom support those particular schemes.

### 2.9 Binding

A **Binding** realizes Loom invocation semantics over a concrete communication mechanism.

Examples may include HTTP/REST, JMS, another messaging system, or in-process invocation.

Bindings MUST preserve the Contract semantics. The Loom protocol MUST NOT contain transport-specific assumptions.

OpenAPI, where useful, describes an HTTP-facing realization. It does not define Loom itself.

### 2.10 Plan

A **Plan** is an Implementation that represents a composition or execution strategy for other Implementations.

A Plan is not a special primitive. It satisfies a Contract and may have Requirements and Capabilities just like other Implementations.

A Plan may therefore contain or reference:

- Workers;
- services;
- builders;
- other Plans;
- evaluators;
- bindings;
- other implementations satisfying its requirements.

This permits recursive composition without introducing a separate protocol hierarchy for orchestration.

### 2.11 Execution

An **Execution** is the runtime realization of an Implementation invocation.

Execution state is distinct from a Plan definition. A Plan describes what may be executed; an Execution records what is actually occurring or occurred.

### 2.12 Result

A **Result** is the protocol-defined outcome of an Execution.

Results MUST be distinguishable from execution state and MUST conform to the Contract's result semantics.

### 2.13 Evidence

**Evidence** is language-neutral information produced or preserved during Execution that supports verification, evaluation, provenance, or audit.

Evidence is not private reasoning. It represents externally meaningful facts about execution, artifacts, observations, decisions, or verification.

## 3. Composition and resolution

Loom does not hard-code a universal sequence of operations. Composition is derived from Requirements and available Capabilities.

A conforming execution system MUST be able to resolve the dependencies necessary for a requested Implementation or Plan.

Conceptually:

```text
Contract / Requirement
        |
        v
    Discovery
        |
        +-------------------+
        |                   |
        v                   v
 running             Provider / Builder
 implementation            |
        |                  v
        |             acquire/build
        |                  |
        +--------+---------+
                 |
                 v
        resolve Requirements
                 |
                 v
              Plan
                 |
                 v
             Execution
                 |
          +------+------+
          |             |
          v             v
       Result        Evidence
```

The exact resolution algorithm is not yet frozen. In particular, matching semantics, cardinality, version ranges, lifecycle transitions, conflict handling, and failure recovery require further normative definition.

## 4. Lifecycle

Loom implementations have lifecycle semantics, but the complete state machine is intentionally a subsequent specification task.

The eventual lifecycle model MUST define:

- discoverable;
- available;
- acquiring/building;
- registered;
- ready;
- executing;
- completed;
- failed;
- unavailable;
- retired;
- relevant transitions and their preconditions.

The model MUST distinguish implementation availability from execution state.

## 5. Conformance

A Loom implementation conforms only to the portions of the protocol it claims to implement and for which it satisfies the normative semantics.

The conformance suite is a first-class deliverable. It SHOULD cover at least:

- Contract identity and compatibility;
- Requirement/Capability matching;
- Registration;
- Discovery;
- Provider/Builder acquisition;
- endpoint resolution;
- binding invocation;
- dependency resolution;
- Plan composition;
- Execution lifecycle;
- Result semantics;
- Evidence shape and provenance.

The suite MUST be runnable against implementations without requiring access to their source language or framework internals.

## 6. Serialization and IDL

The normative semantic model is independent of serialization.

Loom MUST NOT define its semantics by choosing one serialization or interface description language.

Potential realization mechanisms include JSON Schema, OpenAPI, Protobuf, YAML, XML, or another suitable standard. Each must be evaluated according to the layer it describes.

In particular:

- OpenAPI is appropriate to consider for HTTP-facing operations.
- JSON Schema may describe data shapes.
- A messaging-specific mechanism may describe a messaging binding.
- A workflow language such as BPEL may describe higher-level orchestration semantics.

None of these, individually, defines Loom.

## 7. Prior art and interoperability tests

OSGi is useful prior art for dynamic services, requirements/capabilities, and lifecycle. BPEL is useful prior art and a stress test for orchestration semantics.

Loom does not inherit their language, runtime, classloading, workflow, or deployment assumptions.

A strong architectural test is whether a future BPEL engine could use Loom for service discovery and invocation while keeping BPEL process semantics above Loom.

Another strong test is whether a future `loom-java` can consume the same protocol definitions as `loom-ai` without translation of Python classes into Java classes.

## 8. Explicit non-goals

Loom does not define:

- AI-specific services;
- model providers or model selection;
- credentials or secrets;
- provider SDKs;
- coding-agent UX;
- a mandatory central registry;
- a specific database or directory service;
- a particular programming language;
- a particular deployment model;
- HTTP/REST as the protocol;
- private chain-of-thought.

These may be implemented by Loom participants or higher-level ecosystems such as `loom-ai`.
