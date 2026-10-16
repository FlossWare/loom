# ADR-0009: Execution Lifecycle and Result Semantics

- **Status:** Proposed
- **Related issues:** #2, #5, #8
- **Depends on:** ADR-0001 (language-neutral protocol), ADR-0007 (contract representation layers), ADR-0008 (external client execution boundary)

## Context

The initial specification defines Execution, Result, Evidence, and lifecycle, but
does not yet make their boundaries precise enough for independent conformance.
In particular, implementation availability can be confused with invocation
state, process completion can be mistaken for task success, and cancellation,
deadline, partial output, and failure causes can be flattened into one status.

## Decision

Loom MUST distinguish three related but separate concepts:

1. **Implementation lifecycle:** whether an Implementation can be discovered,
   acquired, invoked, or is unavailable/retired.
2. **Execution lifecycle:** whether one invocation has not started, is running,
   is interrupted/resumable where supported, or is terminal.
3. **Result outcome:** whether the Contract's success criteria were met and what
   output, artifacts, observations, failures, Evidence, and provenance were
   produced.

A Contract defines its concrete labels and representations, but MUST map them
unambiguously to these semantic distinctions. A successful Result means the
Contract's success criteria were satisfied; a process returning or an invocation
stopping is not sufficient. A partial Result is not full success. Retryability
is classification or policy input, not an instruction that overrides other
constraints.

Terminal Execution outcomes are immutable. A Contract that supports cancellation
must distinguish accepted requests from confirmed termination and must not
report cancellation before work has stopped. A Contract that supports deadlines
must preserve an unambiguous deadline across handoffs and continuation, expose
expiry explicitly, and prevent expiry from being reported as success. Durable
continuation preserves the Execution identity and required state/history.

Evidence consists of externally meaningful facts used for verification,
evaluation, provenance, or audit. It is distinct from derived conclusions and
private reasoning. Contracts define required Evidence for their success claims,
and bindings enforce authorization and redaction.

This ADR does not define a universal wire schema, exact state enum, storage
technology, transport, retry algorithm, or orchestration framework. Those
realizations remain Contract- and Binding-specific, subject to the semantic
requirements above.

## Consequences

- Independent implementations can map their native lifecycle and result types
  to common observable semantics.
- Conformance can test success claims, cancellation, deadline, and continuation
  without depending on Python classes or one wire representation.
- The contract repository can add schemas only after the semantic distinctions
  are reviewed and accepted.
- Domain contracts may add more specific outcomes without collapsing Execution
  lifecycle and Result outcome into one field.

