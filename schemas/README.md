# Loom Schemas

JSON Schemas define the machine-readable structural representation of Loom contract artifacts. They complement, but do not replace, the normative semantic specification and executable conformance suite.

## Initial schema

- `contract.schema.json`

Additional schemas for capabilities, requirements, implementations, results, and evidence should be added alongside their normative artifact definitions and conformance fixtures. They are not included in this initial schema set.

Schemas define structure. The normative specification defines meaning. Conformance tests verify behavior. OpenAPI or another protocol description may reference these schemas when exposing Loom over a transport.
