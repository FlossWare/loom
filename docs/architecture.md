# Loom Architecture

Loom separates four concerns that are easy to accidentally collapse into one implementation:

```text
Protocol
   │
   ├── semantics and contracts
   │
   ▼
Implementation
   │
   ├── language/runtime realization
   │
   ▼
Binding
   │
   ├── communication mechanism
   │
   ▼
Deployment
```

## Loom

The protocol defines the meaning of Contracts, Implementations, Capabilities, Requirements, Discovery, Providers/Builders, Endpoints, Bindings, Plans, Execution, Results, Evidence, lifecycle, and conformance.

## Execution engine

An execution engine consumes Loom-described requirements and compositions, resolves dependencies, acquires implementations when necessary, constructs or selects Plans, and executes them. An execution engine is an implementation of Loom, not part of the normative protocol.

## Domain ecosystems

A domain ecosystem adds domain-specific Contracts and Implementations without changing Loom's generic semantics.

`loom-ai` is the AI-oriented ecosystem and reference implementation currently being developed. It may define Workers, Arbiters, model services, and AI-specific builders, but those remain Loom Implementations.

## Platforms

A platform is a declarative composition of implementations. Fullsend is intended to be a platform built from Loom and `loom-ai` services.

A platform definition is not the same thing as the execution engine that realizes it.

## Architectural tests

The architecture should satisfy these tests:

1. A future `loom-java` can implement Loom without translating Python classes.
2. A future BPEL-oriented engine can use Loom for discovery and invocation while keeping BPEL semantics above Loom.
3. HTTP and JMS bindings can expose the same Contract semantics.
4. A Plan can contain another Plan without a special-case protocol hierarchy.
5. An implementation can be acquired by a Builder when no suitable running instance exists.
6. Fullsend can consume Loom and `loom-ai` services without defining Loom semantics itself.
