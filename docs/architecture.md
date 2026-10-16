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

## External clients and application boundary

External clients interact with Loom through operations declared by a Contract
and exposed through a Binding. HTTP/REST, MCP, CLI/TUI, messaging, and in-process
adapters are peers: they translate external requests and representations, but
must not create a second execution authority or bypass the implementation's
declared lifecycle, result, evidence, and provenance semantics.

Loom does not mandate a universal Orchestrator class or canonical endpoint names.
A domain Contract may define submit, observe, continue, cancellation, or deadline
operations when its semantics require them. A Binding must document which
operations it exposes and preserve their observable meaning.

A Binding must explicitly document its authentication, authorization, and trust
boundary. A local-only or trusted-environment binding must say so; transport
selection alone does not establish authorization. Remote Loom-to-Loom integration
uses the same Contract and Binding rules rather than introducing a privileged
protocol path.

## Platforms

A platform is a declarative composition of implementations. Concrete platforms are consumers of Loom and domain ecosystems, not part of the Loom protocol itself.

A platform definition is not the same thing as the execution engine that realizes it.

## Architectural tests

The architecture should satisfy these tests:

1. A future `loom-java` can implement Loom without translating Python classes.
2. A future BPEL-oriented engine can use Loom for discovery and invocation while keeping BPEL semantics above Loom.
3. HTTP and JMS bindings can expose the same Contract semantics.
4. A Plan can contain another Plan without a special-case protocol hierarchy.
5. An implementation can be acquired by a Builder when no suitable running instance exists.
6. A concrete platform can consume Loom and a domain ecosystem without defining Loom semantics itself.
