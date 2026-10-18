# Capability Discovery and Worker Handoff Contract

## Status and scope

This document defines language-neutral discovery, selection, and handoff behavior
for Loom participants. It does not mandate a registry, queue, transport, workflow
engine, or programming language. Local and remote realizations MUST preserve the
same observable semantics.

## Discovery request

A discovery request identifies the required Contract and version condition,
required and preferred attributes, and cardinality. A bounded request MAY include
a page size and continuation cursor. The response MUST indicate whether it is
complete or bounded and provide a continuation mechanism when more candidates
may exist.

A candidate is eligible only when Contract identity, version compatibility,
required attributes, and required cardinality satisfy ADR-0010. Discovery MUST
NOT use descriptions, fuzzy names, or response order to establish eligibility.
If no eligible set can satisfy the Requirement, return an explicit unsatisfied
outcome. Do not silently substitute an incompatible candidate.

## Selection

Discovery and selection are separate operations. If multiple candidates are
eligible for one required slot, a declared selection policy MUST resolve the
choice. Without such a policy, the result is explicit ambiguity, not first-match
selection. Selection may rank only eligible candidates; it MUST NOT make an
ineligible candidate eligible. Selection rationale and relevant policy/version
identifiers SHOULD be preserved as non-sensitive provenance.

## Handoff envelope

A handoff transfers control and the context required by the receiving Contract.
Its semantic envelope includes:

- a stable handoff identifier and originating Execution identity;
- source and destination Implementation identities;
- the receiving Contract identity/version;
- the validated input or explicitly referenced input artifact;
- the prior structured Result and required Evidence/provenance references;
- applicable deadline, cancellation, authorization, and resource constraints;
- a declared context-size bound and a correlation reference to the originating
  Action/Intent or task.

A receiver MUST receive the structured Result/artifacts required by its Contract.
A prose summary MUST NOT replace required structured input, evidence, or
provenance. The receiver validates its own input and applies its own policy.

## Authorization, bounds, and failure

The source MUST authorize each transferred field or artifact for the receiving
Implementation before transmission. Credentials, hidden prompts, private model
reasoning, unrelated local state, and data the receiver is not authorized to
access MUST NOT be forwarded implicitly.

Context transfer MUST be bounded. If required context cannot be transferred
because of schema, authorization, size, or binding constraints, the handoff MUST
fail explicitly before the receiver executes. Silent truncation, implicit
redaction of required fields, or reinterpretation as a successful handoff is not
conformant. Optional context may be omitted only when the receiving Contract
allows omission and the omission is observable where it affects behavior.

Remote handoffs additionally require authenticated peers, authorization scoped
to the requested Contract/capabilities, and provenance sufficient to correlate
the source request, remote invocation, and returned Result. Delegation MUST be
scoped and expiring where credentials or capabilities are delegated. Remote
transport does not change the semantic obligations of a local handoff.

Retry or duplicate delivery MUST NOT cause duplicate successful completion
unless the receiving Contract defines safe idempotency behavior. A handoff
identifier and originating Execution/task identity SHOULD be used for
deduplication where delivery may be retried.

## Conformance

A conforming implementation SHOULD consume the fixtures in
`docs/fixtures/` for eligible discovery, ambiguity, context preservation,
unauthorized transfer, and context-limit rejection. Adapters may use any native
representation, but they MUST preserve each fixture's expected observable
outcome.
