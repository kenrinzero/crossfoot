"""Oracle self-tests: the green fixture reconciles, the typo bites, the
coverage rules flag under-declaration, schema + referential integrity
reject malformed files, and Decimal semantics are locked."""

import copy
import json
from pathlib import Path

import pytest

from reconcile import check, main

ROOT = Path(__file__).resolve().parent.parent
GREEN = ROOT / "fixtures" / "mini-green.cells.json"
TYPO = ROOT / "fixtures" / "mini-typo.cells.json"
UNCOVERED = ROOT / "fixtures" / "mini-uncovered.cells.json"


def test_green_fixture_reconciles():
    violations, warnings = check(GREEN)
    assert violations == []
    assert warnings == []


def test_green_locks_decimal_semantics():
    # 0.1 + 0.2 == 0.3 holds in Decimal; under binary floats the green
    # fixture would go red — this is the DESIGN.md par.2 regression lock
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    assert any("Decimal" in (r.get("note") or "") for r in doc["relations"])
    assert check(GREEN)[0] == []


def test_single_cell_typo_goes_red():
    violations, _ = check(TYPO)
    assert violations, "typo fixture must not reconcile"
    assert any("r3c1" in v for v in violations)


def test_coverage_bites_by_default_and_warns_in_lenient():
    violations, warnings = check(UNCOVERED)
    assert len(violations) == 3  # r1c3 + r2c3 leaves unfed, r3c3 total untargeted
    assert warnings == []
    lenient_violations, lenient_warnings = check(UNCOVERED, strict_coverage=False)
    assert lenient_violations == []
    assert len(lenient_warnings) == 3


def _mutate(base: Path, **updates):
    doc = json.loads(base.read_text(encoding="utf-8"))
    doc.update(updates)
    return doc


def _write(tmp_path, doc):
    p = tmp_path / "t.cells.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def test_schema_rejects_float_values(tmp_path):
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["cells"][0]["value"] = "1e5"  # exponent form forbidden by pattern
    violations, _ = check(_write(tmp_path, doc))
    assert violations and violations[0].startswith("schema:")


def test_schema_requires_why_on_standalone(tmp_path):
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["cells"][0]["role"] = "standalone"  # no why -> schema error
    violations, _ = check(_write(tmp_path, doc))
    assert violations and violations[0].startswith("schema:")


def test_nondefault_tol_requires_why(tmp_path):
    doc = json.loads(TYPO.read_text(encoding="utf-8"))
    doc["relations"][0]["tol"] = "1"  # would absorb the typo — needs a why
    violations, _ = check(_write(tmp_path, doc))
    assert any("requires a why" in v for v in violations)


def test_id_row_col_mismatch_rejected(tmp_path):
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["cells"][0]["row"] = 9
    violations, _ = check(_write(tmp_path, doc))
    assert any("inconsistent" in v for v in violations)


def test_unknown_relation_ref_rejected(tmp_path):
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["relations"][0]["sources"] = ["r1c1", "r9c9"]
    violations, _ = check(_write(tmp_path, doc))
    assert any("unknown cell ref" in v for v in violations)


def test_cli_exit_codes(capsys):
    assert main([str(GREEN)]) == 0
    assert main([str(TYPO)]) == 1
    assert main([str(UNCOVERED)]) == 1  # strict by default
    assert main([str(UNCOVERED), "--no-strict-coverage"]) == 0  # lenient passes
    capsys.readouterr()
