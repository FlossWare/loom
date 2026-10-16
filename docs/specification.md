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

A **Capability** declares a service or property that an Implementation claims to
provide under a Contract identity and version. A Capability MAY include
contract-defined attributes that constrain where or how it can be used.

A capability declaration is an assertion, not proof of conformance. An
Implementation MUST NOT advertise a Capability it does not provide, and a
candidate MUST be evaluated against the referenced Contract and version rules
before it is treated as eligible.

### 2.4 Requirement

A **Requirement** declares the Capability conditions an Implementation or Plan
needs before it can execute correctly. A Requirement identifies the required
Contract, the acceptable version or compatibility condition, required attribute
constraints, and the number of distinct implementations needed where cardinality
matters.

A Requirement may be satisfied by an eligible registered Implementation or,
where supported, by acquiring/building an Implementation that provides the
required Capability. A Provider/Builder does not itself satisfy the target
Requirement merely because it claims it can build something; the produced
Implementation must be validated and made available under the target Contract.

### 2.5 Capability/Requirement matching

Matching is a normative protocol operation and MUST NOT depend on programming
language, registry product, transport, or candidate ordering.

A candidate is eligible only when all required conditions match:

1. **Contract identity:** the candidate's Capability identifies the required
   Contract. Identifiers are compared according to the Contract's declared
   canonicalization rules; absent such rules, equality is exact. Fuzzy names,
   descriptions, or implementation labels MUST NOT establish a match.
2. **Version compatibility:** the candidate's declared Contract version
   satisfies the Requirement's compatibility condition. Version strings are
   opaque unless the Contract defines their syntax and comparison rules. Loom
   MUST NOT infer semantic-version ranges or compatibility from string shape.
   If no compatibility rule is declared, exact version equality is required.
3. **Required attributes:** every required attribute constraint is satisfied.
   A missing attribute MUST NOT be treated as a match. Preferred attributes may
   rank eligible candidates but MUST NOT make an otherwise ineligible candidate
   eligible.
4. **Cardinality:** the resolved set contains the number of distinct
   Implementations required by the Requirement. A Requirement MUST define
   minimum/maximum cardinality when it needs fan-out or optional capability
   semantics; otherwise, it requires one eligible Implementation.

Discovery returns eligible candidates; it does not silently substitute an
incompatible candidate. If the available candidates cannot satisfy required
cardinality, the Requirement is unsatisfied and resolution MUST report that
condition explicitly.

Candidate selection is separate from eligibility. When multiple candidates are
eligible, a selection policy MAY choose among them using declared criteria such
as cost, health, locality, or priority. Unless a Contract explicitly requires
ordering, the order in which Discovery returns eligible candidates has no
semantic meaning. A bounded discovery response MUST indicate that it is bounded
and provide a way to retrieve additional candidates or establish that the result
set is complete.


### 2.6 Registration

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

### 2.7 Discovery

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

### 2.8 Provider / Builder

A **Provider** or **Builder** is an Implementation capable of acquiring or constructing another Implementation that satisfies a requested Contract or Requirement.

This extends discovery beyond the question "what is already running?" to the question "who can provide an implementation satisfying this requirement?"

The acquisition/build operation remains governed by a Contract. Builders do not receive special protocol status merely because they create other Implementations.

### 2.9 Endpoint

An **Endpoint** identifies where an Implementation may be invoked. It is represented by a URI.

The URI scheme identifies or selects the binding mechanism.

For example:

```text
https://example/loom/service
jms://broker/loom/service
```

These are examples of endpoint addressing, not a requirement that Loom support those particular schemes.

### 2.10 Binding

A **Binding** realizes Loom invocation semantics over a concrete communication mechanism.

Examples may include HTTP/REST, JMS, another messaging system, or in-process invocation.

Bindings MUST preserve the Contract semantics. The Loom protocol MUST NOT contain transport-specific assumptions.

OpenAPI, where useful, describes an HTTP-facing realization. It does not define Loom itself.

The proposed HTTP/REST binding requirements are documented separately in [`bindings/http-rest.md`](bindings/http-rest.md). They apply only when an implementation declares an HTTP binding and do not add transport-specific assumptions to this specification.

### 2.11 Plan

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

### 2.12 Execution

An **Execution** is the runtime realization of an Implementation invocation.

An Execution has an identity, a lifecycle, and may produce a Result and Evidence.
Its identity MUST remain stable for the lifetime of that Execution, including
observation and any continuation supported by its Contract.

Execution state is distinct from both a Plan definition and the outcome recorded
in a Result. A Plan describes what may be executed; an Execution records what is
actually occurring or occurred. An Execution can finish normally while its
Result reports that the requested task did not satisfy its success criteria.

### 2.13 Result

A **Result** records the outcome of a Contract operation or Execution. The
Contract MUST define what its outcomes mean and what observable evidence is
required to claim success.

A Result MUST distinguish success from failure. Success MUST mean that the
Contract's declared success criteria were satisfied, not merely that a process
returned, a request was accepted, or an operation stopped without raising an
exception. A Result MAY also distinguish partial outcomes, policy denial,
cancellation, deadline expiry, or other domain-relevant outcomes. If a Contract
maps one of those cases to a broader failure outcome, it MUST preserve the
specific cause when that distinction affects retry, safety, audit, or client
behavior.

A Result MAY contain typed output/artifacts, observations, failure details,
Evidence, and provenance. The Contract defines their shape and semantics.
Retryability is a failure classification or policy input; it MUST NOT by itself
trigger a retry or override the Contract's authorization, deadline, or terminal
state rules. A partial Result MUST NOT be presented as full success.

### 2.14 Evidence

**Evidence** is language-neutral information produced or preserved during
Execution that supports verification, evaluation, provenance, or audit.

Evidence represents externally meaningful facts about execution, artifacts,
observations, decisions, and verification. It is not private reasoning.
Evidence MUST remain distinguishable from conclusions derived from it, and a
Contract MUST identify any evidence required to substantiate a successful Result.
Evidence and provenance exposed to a caller MUST respect the Binding's
authorization and redaction rules.

### 2.15 External invocation boundary

A Contract MAY define operations through which an external participant submits
work to an Implementation and observes the resulting Execution. These operations
are contract-level semantics; they do not require a particular application
service class, URL layout, RPC mechanism, or transport.

When a Contract supports external execution, its declared operations MUST make
the following behavior unambiguous:

- **Submission:** which contract-defined request starts an Execution and how the
  caller obtains a stable execution identity or handle.
- **Observation:** how the caller obtains lifecycle state, the current or final
  Result, protocol-level failures, and applicable Evidence and provenance.
- **Continuation:** whether an interrupted or incomplete Execution can resume,
  what state is retained, and whether the original execution identity and
  history are preserved. A binding that promises durable continuation MUST
  resume from the implementation's persisted execution state; it MUST NOT
  require the client to reconstruct hidden server state or replay a private
  conversation transcript.
- **Cancellation and deadlines:** whether these controls are supported and how
  accepted, pending, confirmed, expired, and terminal outcomes are represented.
  A binding MUST NOT report cancellation as confirmed before the contract's
  termination conditions are satisfied. A deadline MUST NOT be represented as
  successful completion.

These operations are optional capabilities of an execution Contract, not
universal routes or mandatory methods of the Loom protocol. Their exact request
and response representations are defined by the Contract and its Binding.

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

Implementation lifecycle and Execution lifecycle are separate state machines.
A Contract that exposes either lifecycle MUST define its supported states,
transitions, preconditions, and terminality. Implementations MUST NOT use one
state field to ambiguously represent both availability and an individual
invocation.

### 4.1 Implementation lifecycle

An Implementation lifecycle describes whether an Implementation can be
discovered and acquired or invoked. The Contract MAY use different labels, but
its state model MUST distinguish the applicable semantic conditions, including:

- discoverable or registered;
- available or ready to invoke;
- acquiring or building, where applicable;
- unavailable;
- retired.

A Registration is a discovery declaration; it does not by itself prove that an
Implementation is currently ready to execute. A Plan definition is not an
Execution and MUST NOT be assigned an Execution's runtime state.

### 4.2 Execution lifecycle

An Execution lifecycle describes one invocation. A Contract MUST distinguish,
at minimum, these semantic conditions when applicable:

- **not started:** the request has been accepted but execution work has not begun;
- **running:** execution work is in progress;
- **interrupted:** work is temporarily stopped and may continue only if the
  Contract supports continuation;
- **terminal:** the invocation will perform no further work.

The Contract MAY choose its own state labels, but MUST define an unambiguous
mapping to these conditions. It MUST also distinguish normal completion,
execution failure, accepted cancellation, and deadline expiry where those
causes affect observable behavior.

A valid transition MUST be defined before it is used. At minimum, a running
Execution may become terminal or interrupted; an interrupted Execution may
resume only under the Contract's continuation rules or become terminal.
A terminal Execution MUST NOT be silently reopened, rewritten, or reported as
running. A new attempt that is a new Execution MUST have a distinct identity and
an explicit relationship to the prior attempt.

Normal completion of an Execution does not imply that the requested task
succeeded. The Result's outcome determines whether the Contract's success
criteria were met; the Execution lifecycle records whether and how invocation
work ended.

### 4.3 Cancellation, deadlines, and continuation

Where a Contract supports cancellation, it MUST distinguish a request being
accepted from termination being confirmed. Cancellation MUST be idempotent for
the same Execution identity where the operation can be repeated safely. An
Execution MUST NOT be reported as cancelled until its work has stopped and its
terminal state has been committed. A terminal outcome MUST remain unchanged
when a later cancellation request arrives.

Where a Contract supports deadlines, the deadline MUST identify one unambiguous
instant. Expiry MUST be observable and MUST NOT be reported as successful
completion. The Contract MUST define how deadline expiry interacts with active
work, cancellation, and continuation. If deadline expiry maps to a general
failure status, its cause MUST remain explicit.

Where a Contract promises durable continuation, the implementation MUST retain
the state required to resume the same Execution identity and relevant history.
Continuation MUST NOT silently reset or extend the deadline, discard required
Evidence, or require the client to reconstruct hidden server state. These
requirements do not mandate a storage technology or transport.

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
