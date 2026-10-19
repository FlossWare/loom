"""Tests for the executable Action/Result schema conformance assertions."""

from __future__ import annotations

import unittest

from jsonschema import Draft202012Validator

from tools.validate_contract_artifacts import validate_schema_expectation


class SchemaExpectationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = Draft202012Validator(
            {
                "type": "object",
                "required": ["required_field"],
                "properties": {"required_field": {"type": "string"}},
                "additionalProperties": False,
            }
        )

    def test_accepts_valid_payload_when_fixture_expects_valid(self) -> None:
        validate_schema_expectation(
            {"required_field": "value"},
            True,
            self.validator,
            fixture_name="positive.json",
        )

    def test_accepts_invalid_payload_when_fixture_expects_invalid(self) -> None:
        validate_schema_expectation(
            {},
            False,
            self.validator,
            fixture_name="negative.json",
        )

    def test_fails_when_fixture_claims_valid_payload_is_invalid(self) -> None:
        with self.assertRaisesRegex(ValueError, "expected schema_invalid"):
            validate_schema_expectation(
                {"required_field": "value"},
                False,
                self.validator,
                fixture_name="incorrect-negative.json",
            )

    def test_fails_when_fixture_claims_invalid_payload_is_valid(self) -> None:
        with self.assertRaisesRegex(ValueError, "expected schema_valid"):
            validate_schema_expectation(
                {},
                True,
                self.validator,
                fixture_name="incorrect-positive.json",
            )

    def test_requires_boolean_expectation(self) -> None:
        with self.assertRaisesRegex(ValueError, "boolean schema_valid"):
            validate_schema_expectation(
                {},
                "false",  # type: ignore[arg-type]
                self.validator,
                fixture_name="malformed-expectation.json",
            )


if __name__ == "__main__":
    unittest.main()
