#!/usr/bin/env python3
"""Validate Loom JSON Schemas and portable conformance fixture envelopes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = ROOT / "docs" / "fixtures"
FIXTURE_SCHEMA_PATH = FIXTURE_DIR / "schema-0.1.json"
ACTION_RESULT_SCHEMA_PATH = SCHEMA_DIR / "action-result-0.1.json"

EXPECTED_SCHEMA_OUTCOMES = {
    True: "schema_valid",
    False: "schema_invalid",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load one JSON object from a repository artifact."""
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def validate_schema_expectation(
    payload: dict[str, Any],
    expected_valid: bool,
    validator: Draft202012Validator,
    *,
    fixture_name: str,
) -> None:
    """Execute a fixture's positive or negative schema assertion."""
    if not isinstance(expected_valid, bool):
        raise ValueError(f"{fixture_name} must declare boolean schema_valid")

    errors = list(validator.iter_errors(payload))
    expected_outcome = EXPECTED_SCHEMA_OUTCOMES[expected_valid]
    if expected_valid and errors:
        details = "; ".join(error.message for error in errors)
        raise ValueError(
            f"{fixture_name} expected {expected_outcome}, but validation failed: "
            f"{details}"
        )
    if not expected_valid and not errors:
        raise ValueError(
            f"{fixture_name} expected {expected_outcome}, but validation passed"
        )


def validate_fixture(
    path: Path,
    fixture: dict[str, Any],
    fixture_validator: Draft202012Validator,
    action_result_validator: Draft202012Validator,
    evidence_validator: Draft202012Validator,
) -> None:
    """Validate a fixture's own envelope and execute its declared assertion."""
    if "semantic_area" in fixture and "expected" in fixture:
        fixture_validator.validate(fixture)
        if fixture.get("semantic_area") == "action_result_schema":
            payload = fixture.get("input", {}).get("result")
            if not isinstance(payload, dict):
                raise ValueError(f"{path.name} must provide input.result")
            expected = fixture["expected"]
            expected_valid = expected.get("schema_valid")
            declared_outcome = expected.get("outcome")
            if declared_outcome != EXPECTED_SCHEMA_OUTCOMES.get(expected_valid):
                raise ValueError(
                    f"{path.name} expected.outcome must match schema_valid "
                    f"(got outcome={declared_outcome!r}, "
                    f"schema_valid={expected_valid!r})"
                )
            validate_schema_expectation(
                payload,
                expected_valid,
                action_result_validator,
                fixture_name=path.name,
            )
    elif "action_id" in fixture or "result_id" in fixture:
        action_result_validator.validate(fixture)
    elif "execution_id" in fixture and "trace_events" in fixture:
        evidence_validator.validate(fixture)
    else:
        raise ValueError(
            f"{path.name} is neither a fixture envelope nor an Action/Result artifact"
        )


def main() -> int:
    schema_paths = sorted(SCHEMA_DIR.glob("*.json")) + [FIXTURE_SCHEMA_PATH]
    schemas = {path: load_json(path) for path in schema_paths}
    for path, schema in schemas.items():
        Draft202012Validator.check_schema(schema)
        print(f"schema valid: {path.relative_to(ROOT)}")

    fixture_validator = Draft202012Validator(schemas[FIXTURE_SCHEMA_PATH])
    action_result_validator = Draft202012Validator(
        schemas[ACTION_RESULT_SCHEMA_PATH]
    )
    evidence_validator = Draft202012Validator(
        schemas[SCHEMA_DIR / "execution-evidence-0.1.json"]
    )

    validated = 0
    fixture_ids: set[str] = set()
    for path in sorted(FIXTURE_DIR.glob("*.json")):
        if path == FIXTURE_SCHEMA_PATH:
            continue
        fixture = load_json(path)
        fixture_id = fixture.get("id")
        if fixture_id is not None:
            if not isinstance(fixture_id, str) or not fixture_id:
                raise ValueError(f"{path.name} has an invalid fixture id")
            if fixture_id in fixture_ids:
                raise ValueError(f"duplicate fixture id: {fixture_id}")
            fixture_ids.add(fixture_id)
        validate_fixture(
            path,
            fixture,
            fixture_validator,
            action_result_validator,
            evidence_validator,
        )
        validated += 1

    print(f"validated {validated} conformance fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
