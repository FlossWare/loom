# ADR-0008: External Client Execution Boundary

- **Status:** Proposed
- **Related issue:** #22
- **Depends on:** ADR-0001 (language-neutral protocol), ADR-0007 (contract representation layers)

## Context

Loom implementations may be invoked by local code, remote services, workflow
engines, or external clients. Without a clear boundary, each transport adapter
can become an alternate execution path that bypasses lifecycle management,
result semantics, evidence, or provenance. A client-specific API can also
accidentally become the definition of Loom rather than a binding over a Contract.

The boundary must remain generic. AI-domain terms such as Intent, Worker, and
Arbiter are defined by domain contracts and are not required primitives of
foundational Loom.

## Decision

External clients interact with an Implementation through operations declared by
a Contract and exposed through a Binding. A Binding translates requests and
representations; it MUST NOT redefine the operation semantics or become a
second execution authority.

Loom does not mandate an Orchestrator class, transport, route naming scheme, or
universal set of operations. When an execution Contract supports external work,
it MUST specify the semantics for the operations it exposes, including:

- **Submit:** accept a contract-defined request and return a stable Execution
  identity or handle.
- **Observe:** retrieve lifecycle state, Result, failures, and applicable
  Evidence and provenance for that Execution.
- **Continue:** where supported, resume from persisted execution state while
  preserving the identity and relevant history. A durable-continuation promise
  MUST NOT depend on client transcript replay or reconstruction of hidden state.
- **Request cancellation:** where supported, define idempotency, pending versus
  confirmed termination, and behavior after a terminal outcome.
- **Deadline:** where supported, define an absolute deadline, its propagation
  across handoffs and continuation, and an explicit expiry outcome.

These are semantic capabilities, not mandatory method names or routes. A
Contract may use other names when it defines equivalent, unambiguous behavior.

## Binding and security responsibilities

HTTP/REST, MCP, CLI/TUI, messaging, in-process, and remote Loom-to-Loom
integrations are peers. Each adapter MUST map to the declared Contract operations
and preserve lifecycle, Result, Evidence, provenance, and failure semantics.
No adapter may bypass the execution authority to call internal implementations
as an alternate workflow path.

Every externally reachable Binding MUST document authentication,
authorization, and its trust boundary, including which callers may submit work
and observe Results or Evidence. A binding restricted to a trusted local
environment MUST state that restriction explicitly. Loom does not infer
authorization from a transport, network location, or successful protocol
handshake.

Protocol/binding failures MUST remain distinguishable from execution outcomes.
Results and Evidence exposed to clients MUST NOT disclose credentials, secrets,
or private reasoning traces; Evidence represents externally meaningful facts
and verification artifacts.

Remote Loom-to-Loom execution MUST use the same Contract and Binding semantics
as other external clients. It does not receive a privileged protocol path.

## Conformance consequences

Where a Contract declares external execution operations, conformance MUST verify:

1. Stable execution identity and correct lifecycle observation.
2. Preservation of Result, Evidence, and provenance across the Binding.
3. Continuation from persisted state when durable continuation is promised.
4. Idempotent cancellation and clear pending/confirmed outcomes when supported.
5. Explicit deadline expiry semantics when deadlines are supported.
6. Separation of protocol errors from domain execution failures.
7. Documented authentication, authorization, and trust boundaries.
8. No reliance on language-specific implementation internals or client-specific
   hidden state.

A transport-smoke test alone does not demonstrate real execution or durable
continuation. Those claims require tests at the promised execution boundary.
