# ADR 0006: Builders participate in discovery and acquisition

## Status

Accepted for implementation planning

## Context

Discovery of already-running Implementations is insufficient for systems that can acquire or construct missing implementations. Loom must be able to distinguish finding an existing service from finding a participant capable of producing one.

## Decision

Loom recognizes Providers/Builders as ordinary Implementations that satisfy Contracts for acquisition or construction.

The conceptual resolution flow is:

```text
Requirement
  -> discover suitable running Implementation
  -> or discover suitable Provider/Builder
  -> acquire/build Implementation
  -> register or otherwise make it available
  -> resolve remaining Requirements
  -> execute
```

The protocol does not require a particular provisioning technology or lifecycle manager.

## Consequences

Discovery remains a protocol concept while registry and provisioning technology remain replaceable. Builders can themselves have Requirements and Capabilities and may therefore participate recursively in the same Loom model.
