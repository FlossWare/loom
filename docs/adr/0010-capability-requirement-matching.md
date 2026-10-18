# ADR-0010: Capability and Requirement Matching

- **Status:** Accepted
- **Related issues:** #2, #11
- **Depends on:** ADR-0001 (language-neutral protocol), ADR-0007 (contract representation layers)

## Context

Loom defines Capability and Requirement as core concepts, but discovery cannot be
interoperable until implementations agree on what counts as a match. Guessing
from names, silently assuming semantic versioning, or allowing discovery order to
change eligibility would make independent implementations behave differently.

## Decision

A Capability declares that an Implementation provides a service or property
under a Contract identity and version. A Requirement declares the conditions and
cardinality needed by a consuming Implementation or Plan.

A candidate is eligible only when:

1. its Capability identifies the required Contract using the Contract's declared
   identity comparison rules (exact equality when no canonicalization is
   declared);
2. its version satisfies an explicit compatibility condition, or exactly equals
   the required version when no compatibility condition is declared;
3. all required attribute constraints are satisfied; and
4. the available eligible set can satisfy the Requirement's cardinality.

Contract version strings are opaque unless the Contract defines version syntax
and comparison rules. Loom MUST NOT infer semantic-version compatibility from
string shape. Fuzzy matching by names, descriptions, or implementation labels
MUST NOT establish eligibility. Missing required attributes do not match.
Preferred attributes may influence selection among eligible candidates but do
not change eligibility.

A Requirement that needs fan-out or optional capability semantics MUST define
minimum/maximum cardinality. Otherwise, it requires one eligible Implementation.
Cardinality describes the resolved set, not the number of candidates returned
for selection.

Discovery reports eligible candidates and explicitly reports an unsatisfied
Requirement when required cardinality cannot be met. If a response is bounded,
it MUST indicate that fact and allow further retrieval or establish completeness.
Candidate ordering has no semantic meaning unless a Contract declares ordering.

Selection is separate from matching. A selection policy may choose among
eligible candidates using declared cost, health, locality, priority, or other
criteria, but MUST NOT turn an ineligible candidate into an eligible one.

A Provider/Builder is not a substitute for the requested Implementation. When
acquisition/building is supported, the produced Implementation must be checked
against the target Contract and Requirement before it is considered available.

## Consequences

- Independent implementations can agree on eligibility without sharing a
  registry, language, or selection algorithm.
- SemVer, ranking, health, and locality remain explicit policies rather than
  accidental string or ordering behavior.
- Discovery and conformance can test negative cases as well as successful matches.
- The representation remains open until the semantics are accepted; this ADR
  does not introduce a wire schema.
