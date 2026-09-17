# ADR 0003: Plan is an Implementation

## Status

Accepted

## Context

Loom needs composition and execution planning without introducing a privileged orchestration primitive. Workers, services, builders, and other implementations should be composable under the same protocol rules.

## Decision

A Plan is an Implementation that describes or realizes a composition of other Implementations.

A Plan therefore participates in Loom using the same Contract, Requirement, Capability, lifecycle, invocation, Result, and Evidence semantics as other Implementations.

A Plan definition is distinct from an Execution instance and its runtime state.

An execution engine may derive a Plan from requirements and available capabilities, but the protocol does not mandate a single planning algorithm.

## Consequences

- Composition is recursive.
- A Plan can contain another Plan.
- Workers do not need a special orchestration exception.
- Execution engines remain implementations of Loom rather than becoming part of the protocol definition.
- Higher-level workflow systems can add domain-specific semantics above Loom.

## Architectural test

A future workflow engine, including a BPEL-oriented engine, should be able to use Loom for service discovery and invocation while retaining workflow semantics in the workflow engine itself.
