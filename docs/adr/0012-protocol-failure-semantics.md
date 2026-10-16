# ADR-0012: Protocol Failure Semantics

- **Status:** Proposed
- **Related issues:** #2, #5, #8
- **Depends on:** ADR-0007 (contract representation layers), ADR-0008 (external client execution boundary), ADR-0009 (Execution lifecycle and Result semantics)

## Context

External clients and independent implementations need to distinguish a request
that could not be accepted or resolved from a valid Execution whose Result
reports failure. If these are flattened into one error channel, callers cannot
reliably observe lifecycle, decide whether retry is safe, or preserve a terminal
outcome. Transport-specific status codes also must not become the definition of
Loom semantics.

## Decision

A protocol failure is an operation that could not be interpreted, authorized,
resolved, or carried out according to the applicable Contract semantics. A
protocol failure is distinct from an execution Result.

Contracts MUST define applicable protocol-failure categories, including malformed
requests, unsupported operations/versions, unmet preconditions, authorization
denial, unresolved Requirements, invalid lifecycle transitions, and missing
Execution identities where applicable.

Before an Execution is accepted, a protocol failure MUST NOT be represented as
a successful Result or as if execution had begun. After acceptance, failures
during work are reported through the Execution lifecycle and its Result/failure
semantics. Failures in later observation or continuation operations MUST NOT
erase or rewrite the accepted Execution's persisted outcome.

Protocol failures MUST have a stable machine-readable category or code. A
human-readable message MAY supplement it but MUST NOT be the only semantic
identifier. Retryability, idempotency, deadline, and terminal-state behavior
remain explicit Contract concerns; a retryable classification does not
automatically authorize a retry. Repeating a non-idempotent request MUST NOT
silently duplicate work unless the Contract allows it.

Bindings map protocol failures to their own transport representation while
preserving semantic category and authorization boundaries. Loom does not
mandate HTTP status codes, MCP error envelopes, or a universal wire schema.
Failure responses MUST NOT expose credentials, secrets, private reasoning, or
Evidence the caller is not authorized to receive.

## Consequences

- Clients can distinguish request/contract failures from valid failed executions.
- Retry and recovery policies can use stable classifications without inferring
  semantics from human-readable strings.
- HTTP, MCP, messaging, and in-process bindings can represent the same semantic
  failures without sharing a transport format.
- Conformance can test failure boundaries before and after Execution acceptance.
