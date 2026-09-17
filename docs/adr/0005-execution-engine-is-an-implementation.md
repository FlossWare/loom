# ADR 0005: An execution engine is an Implementation

## Status

Accepted for implementation planning

## Context

Loom describes services and compositions, but an execution engine is needed to resolve requirements, discover or acquire implementations, construct execution plans, and run them.

Making the execution engine part of Loom itself would collapse protocol semantics and runtime machinery again.

## Decision

An execution engine is an Implementation of Loom.

The engine may:

- consume platform definitions;
- resolve Requirements against Capabilities;
- discover running Implementations;
- discover Providers/Builders;
- acquire or construct Implementations;
- construct or select Plans;
- execute Plans;
- collect Results and Evidence.

The protocol defines the semantics and contracts used by these activities but does not mandate one engine architecture or planning algorithm.

## Consequences

A `loom-ai` execution engine may be one implementation. A future Java or other-language engine may implement the same semantics. Higher-level platforms remain declarative compositions rather than becoming hidden execution engines.
