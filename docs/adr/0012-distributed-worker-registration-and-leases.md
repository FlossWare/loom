# ADR-0012: Distributed Worker Registration and Lease Semantics

- **Status:** Accepted
- **Related issues:** #11, #12
- **Depends on:** ADR-0009 (Execution lifecycle and Result semantics), ADR-0010 (Capability and Requirement matching), ADR-0011 (Capability acquisition and handoff)

## Context

A local Worker and a Worker process running on another machine must satisfy the
same Worker contract. A distributed realization needs explicit registration,
liveness, task ownership, lease expiry, duplicate-delivery, and result acceptance
semantics. Without those rules, stale workers can publish results after losing
ownership, retries can duplicate completed work, and scheduler behavior can
depend on queue implementation details.

## Decision

- Worker identity is stable across heartbeats and task attempts. A registration
  advertises the Worker's Implementation/Contract identity, capabilities,
  protocol version, and lifecycle state. Capability advertisements are claims
  to be checked against registration policy, not authorization grants.
- A scheduler assigns a task only to an eligible registered Worker. Each claim
  creates a lease with an opaque lease identifier and monotonically increasing
  fencing generation for that task.
- A lease has a finite expiry. A Worker must renew before expiry to retain
  ownership. Once expired or superseded, the lease cannot be revived by a late
  heartbeat or result submission. The scheduler rejects results from stale
  generations.
- Task delivery is at least once unless a binding explicitly guarantees stronger
  delivery. A stable task/idempotency identity and durable accepted result make
  duplicate submissions safe: a completed task returns its recorded outcome
  and MUST NOT execute again under the same identity.
- Retryable failure or lease expiry may return incomplete work to the queue only
  under the task's retry policy, deadline, cancellation state, and idempotency
  contract. Terminal outcomes remain immutable.
- Worker lifecycle distinguishes starting, ready, draining, stopped, and
  unhealthy. A draining Worker receives no new leases but may finish or safely
  release current leases. Shutdown and lease release are idempotent.
- Results carry task/run/execution correlation, Worker identity, attempt number,
  lease generation, outcome, evidence, and non-sensitive provenance. Only the
  current lease holder may commit a result.
- Registration, heartbeat, claim, renewal, release, and result submission require
  authenticated identities and authorization appropriate to the deployment.
  Lease tokens are not a substitute for authentication or capability policy.
- Local and remote Workers use the same semantic protocol. The contract does
  not mandate a queue, database, container runtime, language, or transport.

## Consequences

- Lease expiry and fencing make stale-worker behavior deterministic.
- At-least-once delivery is safe only when task identity and duplicate handling
  are explicit.
- A local in-memory implementation can exercise the same contract as a remote
  fleet without pretending it proves production network security or durability.
