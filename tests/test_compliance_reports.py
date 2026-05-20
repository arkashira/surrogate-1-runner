import os
import tempfile
import pytest
from compliance_reports.checker import ComplianceChecker

def test_checker_no_violations(tmp_path):
    file = tmp_path / "good.bin"
    file.write_bytes(b"some content")
    checker = ComplianceChecker(size_limit_bytes=1024)
    violations = checker.check_artifact(str(file))
    assert violations == []

def test_checker_size_violation(tmp_path):
    file = tmp_path / "big.bin"
    file.write_bytes(b"a" * 2048)  # 2KB
    checker = ComplianceChecker(size_limit_bytes=1024)
    violations = checker.check_artifact(str(file))
    assert any("File size" in v for v in violations)

def test_checker_keyword_violation(tmp_path):
    file = tmp_path / "bad.bin"
    file.write_bytes(b"this contains banned content")
    checker = ComplianceChecker(banned_keywords=["banned"])
    violations = checker.check_artifact(str(file))
    assert any("banned" in v for v in violations)