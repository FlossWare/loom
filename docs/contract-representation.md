# Loom Contract Representation

A Loom contract is defined at the semantic level first. Serialization and transport mechanisms are realizations of that contract, not the contract itself.

Loom uses four complementary layers:

1. Normative semantic specification: meaning, obligations, compatibility, and observable behavior.
2. Machine-readable schemas: structural representation of contract artifacts.
3. Executable conformance: verification of semantic obligations.
4. Protocol bindings: transport-specific realization such as HTTP.

No single representation is authoritative for all four layers.

## Authority

The contract repository is authoritative for contract identity and version semantics, operation meaning, capability and requirement semantics, compatibility and matching rules, lifecycle behavior, plan and execution semantics, result and evidence semantics, protocol-level failures, and conformance requirements.

Schemas define structure, but do not replace behavioral semantics.

## Machine-readable representation

JSON Schema is the initial structural representation for Loom artifacts because it is language-neutral, broadly implementable, and independent of transport. Schemas live under schemas/.

## HTTP and OpenAPI

OpenAPI is a binding specification for HTTP exposure of Loom contracts. It is not the normative definition of Loom. An HTTP binding must preserve the semantics defined by the Loom contract.

## Other bindings

The same semantic contract may be realized through messaging systems, in-process APIs, or other protocols. A binding is conformant when it preserves observable contract semantics.

## Behavioral conformance

Conformance tests must cover behavior that schemas cannot express, including capability/requirement matching, discovery, implementation satisfaction, lifecycle transitions, builder acquisition, dependency resolution, plan resolution, execution, result semantics, evidence semantics, and protocol-level failure behavior.

## AI-domain contracts

loom-ai follows the same model. It defines AI-domain semantics above Loom and may provide JSON Schemas and conformance fixtures. loom-ai-python realizes those contracts in Python.

## Design rule

If an artifact answers what Loom means, it belongs in the contract repository. If it answers how a particular language or transport realizes Loom, it belongs in the corresponding implementation or binding.
