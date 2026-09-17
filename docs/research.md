# Loom Research Agenda

The semantic model is intentionally established before selecting representation standards. Research should evaluate existing standards as fits for individual layers rather than searching for one standard that defines all of Loom.

## Areas

### Contract and schema representation

Evaluate JSON Schema, OpenAPI components, Protobuf, Avro, and other established schema mechanisms for expressing language-neutral request/response data.

### Operation and invocation description

Evaluate OpenAPI and alternatives for describing operations without making HTTP a protocol assumption.

### Discovery and capability models

Evaluate OSGi requirements/capabilities and service registry models for applicable semantics while excluding JVM-specific assumptions.

### Messaging

Evaluate standards appropriate for asynchronous bindings and correlation semantics.

### Workflow

Evaluate BPEL and related workflow systems as architectural stress tests. Workflow semantics remain above Loom.

### Conformance

Define a machine-checkable conformance approach that can run against independent implementations.

## Rule

Do not invent a Loom-specific markup language merely because the semantic model is new. Reuse established standards where they fit and keep Loom semantics independent of the representation.
