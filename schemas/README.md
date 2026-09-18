# Loom Schemas

JSON Schemas define the machine-readable structural representation of Loom contract artifacts. They complement, but do not replace, the normative semantic specification and executable conformance suite.

Initial schema set:

- contract.schema.json
- capability.schema.json
- requirement.schema.json
- implementation.schema.json
- result.schema.json
- evidence.schema.json

Schemas define structure. The normative specification defines meaning. Conformance tests verify behavior. OpenAPI or another protocol description may reference these schemas when exposing Loom over a transport.
