"""
test_email_generator.py - Unit tests for the email generation and evaluation pipeline.

These tests validate the utility functions without making real API calls.
"""

import pytest
from email_generator import _format_key_facts, _extract_thinking_and_email
from evaluation_metrics import _programmatic_format_checks


class TestFormatKeyFacts:
    """Tests for the key facts formatter."""

    def test_single_fact(self):
        result = _format_key_facts(["Budget is $50,000"])
        assert result == "  - Budget is $50,000"

    def test_multiple_facts(self):
        facts = ["Fact A", "Fact B", "Fact C"]
        result = _format_key_facts(facts)
        lines = result.split("\n")
        assert len(lines) == 3
        assert all(line.startswith("  - ") for line in lines)

    def test_empty_facts(self):
        result = _format_key_facts([])
        assert result == ""


class TestExtractThinkingAndEmail:
    """Tests for the thinking block extractor."""

    def test_with_thinking_block(self):
        raw = "<thinking>My analysis here</thinking>\n\nSubject: Test Email\n\nDear John,\nHello.\nBest,\nAlex"
        result = _extract_thinking_and_email(raw)
        assert result["thinking"] == "My analysis here"
        assert "Subject: Test Email" in result["email"]
        assert "<thinking>" not in result["email"]

    def test_without_thinking_block(self):
        raw = "Subject: Test Email\n\nDear John,\nHello.\nBest,\nAlex"
        result = _extract_thinking_and_email(raw)
        assert result["thinking"] is None
        assert "Subject: Test Email" in result["email"]

    def test_multiline_thinking(self):
        raw = "<thinking>\nLine 1\nLine 2\nLine 3\n</thinking>\n\nSubject: Hello"
        result = _extract_thinking_and_email(raw)
        assert "Line 1" in result["thinking"]
        assert "Line 3" in result["thinking"]


class TestProgrammaticFormatChecks:
    """Tests for the programmatic email structure validator."""

    def test_perfect_email(self):
        email = """Subject: Test Email

Dear Ms. Patel,

Thank you for your time.

Best regards,
Alex"""
        result = _programmatic_format_checks(email)
        assert result["has_subject_line"] is True
        assert result["has_greeting"] is True
        assert result["has_sign_off"] is True
        assert result["has_placeholders"] is False
        assert result["programmatic_score"] == 1.0

    def test_missing_subject(self):
        email = """Dear Mr. Smith,

Thank you for your time.

Sincerely,
Jordan"""
        result = _programmatic_format_checks(email)
        assert result["has_subject_line"] is False
        assert result["has_greeting"] is True
        assert result["has_sign_off"] is True

    def test_with_placeholders(self):
        email = """Subject: Meeting Follow-up

Dear [Your Name],

Thank you for meeting on [Date].

Best regards,
[Insert Name]"""
        result = _programmatic_format_checks(email)
        assert result["has_placeholders"] is True
        assert len(result["placeholders_found"]) >= 1

    def test_no_structure(self):
        email = "Just a random paragraph of text without any email structure."
        result = _programmatic_format_checks(email)
        assert result["has_subject_line"] is False
        assert result["has_greeting"] is False
        assert result["programmatic_score"] < 1.0
