# Distributed Worker Protocol 0.1

## Scope

This contract defines registration, liveness, task leasing, lease fencing,
retry/requeue, idempotency, and result acceptance for local and remote Loom
Workers. It is independent of any queue, database, container runtime, transport,
or programming language. See ADR-0012 for the decision record.

## Worker registration and lifecycle

A Worker registers a stable Worker identity, its Implementation and Contract
identity/version, advertised capabilities, supported protocol version, and
current lifecycle state. Registration is authorized by the coordinator's
deployment policy. Advertising a capability does not grant permission to invoke
it or make the Worker eligible for every task.

Lifecycle states are `starting`, `ready`, `draining`, `stopped`, and
`unhealthy`. Only a ready and eligible Worker may receive a new lease. A
draining Worker receives no new tasks but may complete or safely release work
already leased. Stopping is idempotent. The coordinator MUST NOT infer health
from registration alone; liveness is based on a bounded heartbeat/lease policy.

## Task leasing

A task has a stable task identity, originating run/execution identity, input
reference, requirements, deadline/cancellation constraints, idempotency key,
and retry policy. A claim returns a finite lease with an opaque lease identifier,
expiry instant, and monotonically increasing fencing generation scoped to the
task. The Worker may execute only while holding the current lease.

A heartbeat renews a lease only if the Worker identity, lease identifier, and
fencing generation match the current assignment and the lease has not expired.
An expired lease cannot be revived. A late heartbeat or result from a stale
generation is rejected with a stable machine-readable category. The scheduler
may lease the task to another eligible Worker after expiry according to retry
policy.

## Results, retry, and idempotency

A result submission identifies the task, originating execution/run, Worker,
attempt, lease identifier/generation, outcome, evidence, and non-sensitive
provenance. The coordinator accepts a result only from the current lease holder.
Once a terminal result is committed, duplicate submission with the same task
identity returns or references the recorded result; it MUST NOT execute the
task again or rewrite terminal evidence.

Retryable failure and lease expiry are nonterminal only when retry policy permits
another attempt and cancellation/deadline constraints allow it. A permanent
failure, cancellation, deadline expiry, or successful completion is terminal
according to the Result/Execution contract. A retry receives a new attempt and
lease generation but preserves task/run correlation and prior-attempt evidence.

The protocol provides at-least-once delivery by default. Exactly-once side effects
are not promised by transport semantics; they require idempotent bindings or
application-level deduplication. A stale Worker cannot commit a result merely
because its local computation completed successfully.

## Security and context

Registration, heartbeat, claim, renewal, release, and result submission require
authenticated peers and operation-level authorization. Delegated capabilities
must be scoped to the task and expire or be revocable. Lease identifiers are
fencing tokens, not credentials. Task context is transferred under the
Capability Discovery and Worker Handoff Contract, with bounded payloads,
validated input, provenance, and no implicit credential or private-reasoning
transfer.

## Local dogfood

A deterministic local multi-worker harness SHOULD run at least two independently
executing Worker processes against the same coordinator contract. It should
exercise registration, separate lease claims, heartbeat renewal, lease expiry,
stale result rejection, retry/requeue, duplicate delivery, and persisted result
correlation. Such a harness proves protocol behavior but does not by itself
qualify production network security, multi-host durability, or live fleet
availability.

## Conformance

The fixtures under `docs/fixtures/distributed-worker-*` define required
observable outcomes. An implementation may use native messages or HTTP endpoints
as long as it preserves these semantics.
