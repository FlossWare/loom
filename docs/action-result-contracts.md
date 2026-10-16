# Action and Result Contracts

## Status

This document defines the initial language-neutral shape and semantic obligations for typed Actions and Results. Schema version `0.1` is an interoperable envelope, not a universal domain payload or a mandatory runtime API.

## Action

An **Action** is a contract-defined request to perform an operation. An Action MUST identify the target Contract and its version and carry input that can be validated against that Contract's input schema or equivalent rules.

The common Action envelope contains:

- `action_id`: stable identifier for this request artifact;
- `contract_id` and `contract_version`: exact target Contract identity;
- `input`: contract-specific structured input;
- optional `execution_id`: caller-provided execution identity only where the target Contract explicitly permits it;
- optional `metadata`: non-sensitive context defined by the Contract.

A Binding MUST validate the envelope and contract-specific input before accepting execution. A malformed or unsupported Action rejected before acceptance is a protocol failure, not an Execution Result. A binding MUST NOT invent a successful Result for a request it did not accept.

The Action envelope does not define a universal action vocabulary. Domain-specific action types and payload schemas belong in the relevant contract layer.

## Result

A **Result** records the observable outcome of an accepted Contract operation or Execution. Its common envelope contains:

- `result_id` and `execution_id`: stable identifiers for the Result and its execution;
- `outcome`: explicit outcome independent of the Execution lifecycle;
- optional typed `output`, `artifacts`, and `observations`;
- optional structured `failure`, `evidence`, and `provenance`.

The initial common outcomes are:

- `succeeded`: declared success criteria were satisfied;
- `partially_succeeded`: only a declared subset of success criteria was satisfied;
- `failed`: the operation did not satisfy its success criteria;
- `policy_denied`: an accepted operation was denied by an applicable policy;
- `cancelled`: execution was cancelled under the applicable Contract;
- `deadline_exceeded`: the execution deadline expired before success was established.

A Contract MAY define additional outcomes, but MUST document their mapping to the common semantic conditions when claiming conformance. A completed Execution does not imply a `succeeded` Result. Worker/process completion, request acceptance, absence of an exception, or a missing Evaluation MUST NOT be treated as proof of success.

## Failure classification and retry

A failure MAY include a stable machine-readable `category`, a human-readable `message`, and a `retryable` hint. The category MUST preserve the cause distinctions needed for client behavior, audit, and safety. Human-readable messages MAY change without changing category semantics.

The `retryable` field is information for the applicable policy, not an instruction to retry. A retry MUST be authorized by the Contract and execution policy and MUST respect deadlines, cancellation, idempotency, and terminal-state rules. Policy denial, cancellation, and deadline expiry MUST NOT be silently rewritten as generic transient failures.

A pre-acceptance protocol failure is represented by the Binding's protocol-failure contract, not by fabricating an Execution Result. Once an Action is accepted, its eventual Result and failure category MUST remain observable by execution identity.

## Typed artifacts, observations, evidence, and provenance

Artifacts SHOULD identify a stable reference and media type; inline payloads MAY be used when the Contract permits them. Observations SHOULD identify their kind and structured value. Evidence MUST remain distinguishable from derived conclusions. Provenance SHOULD identify the producing implementation and relevant execution or event references.

The common envelope does not authorize access to any artifact. A Binding MUST apply authorization and redaction before exposing output, evidence, or provenance. Credentials, access tokens, hidden prompts, and private model chain-of-thought MUST NOT be persisted as Result data.

## Schema and compatibility

The JSON Schema `schemas/action-result-0.1.json` defines the common envelope for an Action and a Result. The contract-specific `input` and `output` payloads remain open objects unless the referenced Contract supplies stricter schemas. This preserves domain-neutral structure without pretending every operation has the same payload.

Schema validation proves only structural conformance. It does not establish that a result is truthful, that evidence is valid, that a caller is authorized, or that success criteria were satisfied. Those obligations require executable conformance and implementation-specific evaluation.

Breaking changes to existing field meaning require a new schema version. Additive fields MAY be introduced compatibly when consumers can safely ignore unknown fields.

## Conformance expectations

Implementations claiming this contract SHOULD demonstrate that:

1. malformed input is rejected before execution acceptance;
2. accepted Actions return a stable execution identity and an explicit Result outcome;
3. lifecycle completion is distinct from Result success;
4. partial success cannot be represented as full success;
5. failure categories survive serialization and observation;
6. retryable failures do not trigger retries without policy authorization;
7. cancellation, deadline expiry, and policy denial remain distinguishable;
8. output, artifacts, evidence, and provenance preserve their declared structure;
9. authorization and redaction apply before sensitive Result data is disclosed;
10. language and transport adapters preserve the same observable semantics.

Portable examples are provided under `docs/fixtures/`. They are conformance inputs, not an alternate specification.
