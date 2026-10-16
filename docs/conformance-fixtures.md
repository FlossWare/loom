# Conformance Fixtures

Conformance fixtures are machine-readable test inputs and expected outcomes for Loom protocol semantics.

They are **test artifacts**, not a Loom wire format. A fixture may be represented as YAML or JSON, and an implementation-specific adapter may translate it into the native test environment. The fixture's semantic meaning is independent of that representation.

## Fixture structure

The versioned envelope schema is [schema-0.1.json](fixtures/schema-0.1.json), and [protocol-failure-malformed-request-001.json](fixtures/protocol-failure-malformed-request-001.json) is the first fixture using it. Validate fixtures against the schema version they declare before passing them to an implementation adapter. The schema validates the common envelope only; domain-specific input and expected-outcome details remain extensible until their semantics are accepted.

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

The envelope is versioned independently from Loom wire representations. Schema 0.1 freezes only the fields needed to identify a fixture and its contract; it does not freeze domain-specific payload vocabulary or define a Loom wire format. When normative semantics change, introduce a compatible schema revision or a new schema version rather than silently changing the meaning of an existing fixture.

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
2. Capability and Requirement matching (identity, compatibility, attributes, cardinality)
3. Registration and Discovery (eligible candidates, completeness, and explicit unsatisfied results)
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

## Execution and Result lifecycle fixtures

Once the lifecycle semantics in the normative specification are accepted, the
fixture suite SHOULD include positive and negative cases for:

- an Execution that completes normally with a successful Result;
- an Execution that completes but whose Result reports failure to meet the
  Contract's success criteria;
- a running Execution whose cancellation request is accepted but remains
  pending until work stops;
- a cancellation request against a terminal Execution that leaves its outcome
  unchanged;
- a deadline that expires before work starts and prevents new work from being
  scheduled;
- an interrupted Execution that resumes with the same identity and required
  persisted context;
- a successful Result missing required Evidence, which MUST fail conformance;
- a partial Result that is incorrectly presented as full success.

These fixtures test semantic distinctions, not a required wire vocabulary. Each
fixture must state the Contract-specific labels and their mapping to the
normative semantic conditions.

## Resolution and handoff fixtures

The conformance suite SHOULD include cases for:

- no candidate satisfying the required Contract identity or version condition;
- a missing required attribute that makes a candidate ineligible;
- several eligible candidates with no selection policy, producing explicit
  ambiguity rather than discovery-order selection;
- an eligible Builder whose produced Implementation fails target-contract
  validation and therefore does not satisfy the Requirement;
- a handoff that preserves required prior Result, Evidence, provenance, and
  execution constraints;
- a handoff that attempts to transfer unauthorized context and is rejected;
- context that exceeds a declared limit, producing an explicit failure rather
  than silent truncation;
- local and remote handoffs that preserve the same observable contract semantics.

## Protocol-failure fixtures

The suite SHOULD include positive and negative cases that distinguish:

- malformed or unsupported requests rejected before an Execution is accepted;
- an authorization denial that does not expose protected Result or Evidence data;
- an accepted Execution whose Worker/Implementation later returns a failure Result;
- an observation request for a missing Execution identity;
- an invalid lifecycle transition that leaves terminal state unchanged;
- a retryable failure classification that does not automatically trigger a retry;
- a repeated non-idempotent request without a declared idempotency contract;
- a protocol failure whose machine-readable category remains available even if
  its human-readable message changes.


## Execution evidence, trace, and evaluation fixture

[execution-evidence-success-001.json](fixtures/execution-evidence-success-001.json) demonstrates a successful execution with ordered trace events, a provenance-linked output artifact, and a criterion-level evaluation. Its envelope is defined by [execution-evidence-0.1.json](../../schemas/execution-evidence-0.1.json); the semantic requirements are defined in [Execution Evidence, Trace, and Evaluation Contracts](execution-evidence.md).

The fixture is illustrative and intentionally marks the artifact digest as `unverified`. A digest value alone is not proof that the artifact was fetched or verified. Conformance adapters SHOULD validate the envelope against the declared JSON Schema and then test behavioral requirements that structural validation cannot establish.

Additional fixtures SHOULD cover at least:

- accepted execution failure versus protocol rejection before acceptance;
- missing required evidence despite a claimed successful Result;
- evidence whose integrity check fails or whose artifact is unavailable;
- evaluations with `not_met`, `inconclusive`, and `not_evaluated` outcomes;
- trace events with duplicate identifiers or reused per-execution sequence numbers;
- redaction of credentials and exclusion of private model chain-of-thought.

## Typed Action and Result fixtures

The initial common envelopes are defined by [action-result-0.1.json](../../schemas/action-result-0.1.json), with the semantic contract in [Action and Result Contracts](../action-result-contracts.md). The following examples cover distinct artifacts:

- [action-envelope-001.json](fixtures/action-envelope-001.json): a contract-identified Action with structured input;
- [result-envelope-success-001.json](fixtures/result-envelope-success-001.json): a successful Result with typed output, observation, evidence reference, and provenance;
- [result-policy-denied-001.json](fixtures/result-policy-denied-001.json): an explicit policy-denial outcome with a stable failure category and non-retryable classification.

The policy-denial example is an accepted-operation Result, not a pre-acceptance protocol rejection. A binding must report pre-acceptance rejection through its protocol-failure contract and must not invent an execution Result for work that was never accepted.

## Relationship to the normative specification

This document describes the test mechanism. It does not freeze unresolved protocol semantics.

The normative specification must first define the meaning of matching, lifecycle transitions, protocol failures, evidence, and other required behaviors. Conformance fixtures then turn those definitions into executable interoperability tests.

That ordering is deliberate. Otherwise the test suite becomes a second, accidental specification, which is precisely the sort of architectural archaeology Loom is intended to avoid.
