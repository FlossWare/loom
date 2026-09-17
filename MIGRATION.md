# Migration from `loom-ai`

The Loom protocol was initially documented inside `FlossWare/loom-ai`. With the creation of this repository, generic Loom architecture moves here.

## Canonical ownership

| Concern | Repository |
|---|---|
| Loom protocol and semantics | `FlossWare/loom` |
| Loom conformance | `FlossWare/loom` |
| Loom binding specifications | `FlossWare/loom` |
| AI-specific Contracts and Implementations | `FlossWare/loom-ai` |
| Workers and Arbiters | `FlossWare/loom-ai` |
| Model services/providers | `FlossWare/loom-ai` |
| AI-specific builders | `FlossWare/loom-ai` |
| Concrete platform compositions | platform repository, such as Fullsend |

Issue tracking follows the same ownership boundary. Generic Loom issues belong here; AI-specific implementation issues remain in `loom-ai`.

The migration is deliberately additive. Existing implementation code is not moved merely to make the repository names look tidy. Code moves only when its semantics belong to Loom itself and an implementation-neutral realization is appropriate.
