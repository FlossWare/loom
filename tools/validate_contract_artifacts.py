#!/usr/bin/env python3
"""Validate Loom JSON Schemas and portable conformance fixture envelopes."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = ROOT / "docs" / "fixtures"
FIXTURE_SCHEMA_PATH = FIXTURE_DIR / "schema-0.1.json"
ACTION_RESULT_SCHEMA_PATH = SCHEMA_DIR / "action-result-0.1.json"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def main() -> int:
    schema_paths = sorted(SCHEMA_DIR.glob("*.json")) + [FIXTURE_SCHEMA_PATH]
    schemas = {path: load_json(path) for path in schema_paths}
    for path, schema in schemas.items():
        Draft202012Validator.check_schema(schema)
        print(f"schema valid: {path.relative_to(ROOT)}")

    fixture_schema = schemas[FIXTURE_SCHEMA_PATH]
    fixture_validator = Draft202012Validator(fixture_schema)
    action_result_schema = schemas[ACTION_RESULT_SCHEMA_PATH]
    action_result_validator = Draft202012Validator(action_result_schema)

    validated = 0
    for path in sorted(FIXTURE_DIR.glob("*.json")):
        if path == FIXTURE_SCHEMA_PATH:
            continue
        fixture = load_json(path)
        if "semantic_area" in fixture and "expected" in fixture:
            fixture_validator.validate(fixture)
            if fixture.get("semantic_area") == "action_result_schema":
                payload = fixture.get("input", {}).get("result")
                if not isinstance(payload, dict):
                    raise ValueError(
                        f"{path.relative_to(ROOT)} must provide input.result"
                    )
                expected_valid = fixture["expected"].get("schema_valid")
                if expected_valid is True:
                    action_result_validator.validate(payload)
                elif expected_valid is False:
                    if action_result_validator.is_valid(payload):
                        raise ValueError(
                            f"{path.relative_to(ROOT)} expected schema rejection"
                        )
                else:
                    raise ValueError(
                        f"{path.relative_to(ROOT)} must declare schema_valid"
                    )
        elif "action_id" in fixture:
            action_result_validator.validate(fixture)
        elif "result_id" in fixture:
            action_result_validator.validate(fixture)
        elif "execution_id" in fixture and "trace_events" in fixture:
            evidence_schema = schemas[SCHEMA_DIR / "execution-evidence-0.1.json"]
            Draft202012Validator(evidence_schema).validate(fixture)
        else:
            raise ValueError(
                f"{path.relative_to(ROOT)} is neither a fixture envelope nor "
                "an Action/Result artifact"
            )
        validated += 1
    print(f"validated {validated} conformance fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
