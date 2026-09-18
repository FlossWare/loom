# Migration from loom-ai

The Loom protocol was initially documented inside loom-ai. Generic Loom architecture now belongs here, while AI-specific contracts and implementations are separated into the contract family defined by the FlossWare repository-layering standard.

## Canonical ownership

| Concern | Repository |
|---|---|
| Loom protocol and semantics | FlossWare/loom |
| Loom conformance | FlossWare/loom |
| Loom binding specifications | FlossWare/loom |
| Loom Python implementation | FlossWare/loom-python |
| AI-specific Contracts and semantics | FlossWare/loom-ai |
| AI Python implementations | FlossWare/loom-ai-python |
| Future AI implementations | {contract}-{domain}-{language} repositories |
| Concrete platform compositions | platform-specific repository |

The repository family follows:

    loom
    loom-python
    loom-ai
    loom-ai-python

Issue tracking follows the same ownership boundary. Generic Loom issues belong here; language-specific implementation issues belong in the relevant implementation repository; AI-domain contract issues belong in loom-ai; AI implementation issues belong in loom-ai-python.

The migration is deliberately semantic rather than cosmetic. Code moves when its ownership belongs in a different layer, not merely to make repository names look tidy.
