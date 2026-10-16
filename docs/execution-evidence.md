# Execution Evidence, Trace, and Evaluation Contracts

## Status

This document defines the initial language-neutral contract for observable execution evidence. The envelope version is `0.1`. It is a semantic contract and schema, not a mandated storage format, tracing vendor, or execution framework.

## Goals and boundaries

A conforming implementation SHOULD make an execution independently inspectable without exposing private reasoning or credentials. The contract separates three related artifacts:

- **Trace events** record observable lifecycle and coordination facts in occurrence order.
- **Evidence** records artifacts or observations that support or contradict a Result.
- **Evaluation** records a domain-neutral assessment of a Result against declared criteria.

These artifacts are related by stable identifiers, but they are not interchangeable. A trace says what was observed to happen; evidence supports a claim; an evaluation explains whether declared criteria were met. None of them alone proves that an implementation is trustworthy.

OpenTelemetry, log systems, databases, and vendor-specific evaluation products MAY be adapters. They MUST NOT redefine the Loom semantics or become required protocol dependencies.

## Execution identity and correlation

Every artifact MUST identify the execution it belongs to using a stable, opaque `execution_id`. The identifier MUST remain unchanged across observation and any continuation promised by the applicable Contract. A new execution attempt MUST use a distinct identifier and MAY refer to a prior attempt using `parent_execution_id` or another explicitly defined relationship.

Where applicable, artifacts SHOULD include `task_id`, `plan_id`, and `implementation_id`. These identifiers are opaque values, not instructions and not authorization credentials.

## Trace event semantics

A trace event records one observable fact. It MUST include:

- a unique `event_id`;
- `execution_id`;
- a stable, machine-readable `event_type`;
- an occurrence timestamp in RFC 3339 date-time format;
- an `outcome` or event-specific payload when the event semantics require one.

An event MAY include a monotonic sequence number scoped to an execution. Consumers MUST NOT infer causal ordering solely from wall-clock timestamps. When sequence numbers are supplied, they MUST be non-negative and MUST NOT be reused within that execution.

Event types SHOULD cover lifecycle transitions, implementation/worker handoffs, retries, verification, cancellation/deadline observations, and terminal outcomes. Implementations MAY define additional namespaced event types. Unknown event types MUST remain safely inspectable and MUST NOT be silently reinterpreted as a known event.

Trace events MUST describe observable actions, decisions, states, or references to artifacts. They MUST NOT contain private model chain-of-thought, hidden prompts, credentials, session cookies, access tokens, or unrelated sensitive context. A concise decision code and its externally observable rationale MAY be recorded when permitted by policy.

## Evidence semantics

Evidence is a structured claim-supporting artifact or reference. Each item SHOULD state its kind, source, creation time, integrity information where available, and the claim or criterion it supports. Evidence MAY be inline or externally referenced. A reference MUST be accompanied by enough metadata to identify the referenced artifact without embedding secrets.

Evidence provenance SHOULD identify the producing implementation or tool and relevant execution/event identifiers. Provenance is an attribution claim, not cryptographic proof. Where integrity verification is available, implementations SHOULD include a digest and algorithm identifier. Consumers MUST distinguish unavailable, invalid, and verified integrity states rather than treating absence of a digest as verified.

A Result that requires evidence MUST NOT be treated as conformant success when required evidence is absent, inaccessible, malformed, or fails the applicable integrity checks. Evidence does not override authorization: a consumer MUST apply access controls before exposing an artifact or its contents.

## Evaluation semantics

An evaluation assesses a Result against an explicitly identified criterion set. It MUST identify the execution and the Result being evaluated, and MUST state an outcome with contract-defined meaning. The initial common semantic outcomes are:

- `met`: all required criteria are satisfied;
- `not_met`: one or more required criteria are not satisfied;
- `inconclusive`: available information is insufficient to decide;
- `not_evaluated`: no assessment was performed.

Implementations MAY expose additional domain-specific outcomes, but MUST document their mapping to these common conditions when claiming conformance. A missing evaluation MUST NOT be interpreted as `met`.

An evaluation SHOULD include criterion-level findings and references to supporting or contradicting evidence. It MAY include a score, but a score MUST NOT replace the explicit outcome or its criteria. Scores from different evaluators MUST NOT be compared unless their scales and semantics are declared compatible.

## Failure and redaction

Protocol rejection before an execution is accepted is distinct from a failure of an accepted execution. Trace and evaluation adapters MUST preserve that distinction. Failure categories SHOULD be stable machine-readable identifiers; human-readable messages MAY change.

Sensitive values MUST be redacted or replaced with non-reversible references before an artifact crosses an authorization boundary. Redaction MUST NOT destroy the stable identifiers or failure category needed to diagnose the execution. Implementations MUST NOT persist credentials or private model chain-of-thought as execution evidence.

## Schema and compatibility

The initial JSON Schema is `schemas/execution-evidence-0.1.json`. It defines a versioned envelope and the core structure of trace events, evidence items, and evaluations. It intentionally permits extension fields so domain-specific evidence can evolve without changing the common envelope.

The schema checks structure, not truth, authorization, causal ordering, artifact availability, integrity, or evaluation correctness. Those are behavioral conformance obligations. Breaking changes to the meaning of existing fields require a new schema version; additive fields MAY be introduced compatibly when unknown fields are safely ignored.

## Conformance expectations

A conforming implementation SHOULD demonstrate that:

1. execution identity remains stable across emitted events and continuation;
2. event IDs are unique and any supplied per-execution sequence is not reused;
3. a trace preserves the distinction between protocol rejection and accepted-execution failure;
4. required evidence is linked to the Result and its provenance is inspectable;
5. missing or invalid required evidence prevents a claim of conformant success;
6. evaluation outcome is explicit and missing evaluation is not success;
7. credentials and private model chain-of-thought are excluded from artifacts;
8. adapters preserve artifact semantics and apply authorization before disclosure.

Fixtures under `docs/fixtures/` provide portable examples. They are test artifacts, not a second specification.
