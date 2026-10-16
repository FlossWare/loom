# ADR-0011: Capability Acquisition and Handoff

- **Status:** Proposed
- **Related issues:** #2, #11
- **Depends on:** ADR-0008 (external client execution boundary), ADR-0009 (Execution lifecycle and Result semantics), ADR-0010 (Capability and Requirement matching)

## Context

Capability matching identifies which Implementations are eligible, but it does
not alone define how a resolver chooses among candidates, obtains a missing
Implementation, or transfers the context required by the next stage of a Plan.
If those steps are implicit, implementations can disagree based on registry
ordering, flatten structured results into summaries, or forward sensitive state
without authorization.

## Decision

### Resolution and selection

Resolution MUST validate the Requirement, discover eligible registered
Implementations, and determine whether the eligible set can satisfy the declared
cardinality. Candidate eligibility is governed by ADR-0010.

When more than one eligible candidate can satisfy a single required slot, a
declared selection policy MUST resolve the choice. If no policy resolves the
ambiguity, the resolver MUST report ambiguity rather than silently select by
registry or response order.

When registered candidates are insufficient and acquisition is supported, the
resolver MAY discover a Provider/Builder that declares the ability to produce an
Implementation for the target Contract. The Builder's own Capability does not
satisfy the target Requirement. The produced Implementation MUST be checked
against the target Contract and required Capabilities before it is accepted.

If required cardinality cannot be satisfied, resolution MUST report an explicit
unsatisfied outcome. An incompatible candidate MUST NOT be substituted silently.

### Handoff

A handoff transfers control and the contract-required context between
Implementations in a Plan or composed Execution. It is behavior of composition,
not a new protocol primitive.

A handoff MUST preserve the Execution identity and transfer the inputs, prior
structured Result, required Evidence, provenance, and execution constraints
required by the receiving Contract. A receiving Contract that needs the original
Result or artifacts MUST NOT receive only a prose summary instead.

Context transfer MUST be authorized and bounded. Credentials, private reasoning,
and unrelated local state MUST NOT be forwarded implicitly. The receiver
validates its inputs and applies its own authorization rules. If required context
cannot be preserved due to schema, size, or binding limitations, the handoff
MUST fail explicitly; silent truncation or reinterpretation is not conformant.

Where cancellation, deadlines, or other execution constraints apply to a
handoff, the Contract MUST define propagation and the handoff MUST NOT reset or
extend their meaning. Local and remote handoffs preserve the same observable
Contract semantics. Idempotent delivery or retry behavior is defined only when
the relevant Contract promises it, and that Contract MUST specify duplicate
handling.

## Consequences

- Resolution is independent of registry ordering and programming language.
- Selection policy cannot weaken Capability/Requirement eligibility.
- Builders are validated producers, not substitutes for the target implementation.
- Composed Implementations receive explicit, bounded, authorized context.
- Remote bindings add transport and security requirements without changing
  the underlying Contract semantics.
- No wire schema or registry product is mandated by this ADR.
