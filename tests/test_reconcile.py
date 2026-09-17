"""Oracle self-tests: the green fixture reconciles, the typo bites, the
coverage rules flag under-declaration, schema + referential integrity
reject malformed files, Decimal semantics are locked, and the corpus itself
holds its keying and encoding contract."""

import copy
import json
from pathlib import Path

import pytest

from reconcile import check, main, sweep

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


def test_schema_rejects_json_float_values(tmp_path):
    # AUDIT-2026-09-16 D4: the exponent-string case above is not a JSON
    # number. A bare 2.0 must be rejected as a schema type error.
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["cells"][0]["value"] = 2.0
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


def test_duplicate_row_index_rejected(tmp_path):
    # AUDIT-2026-09-16 U2: label arrays were not uniqueness-checked.
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["rows"].append({"index": 1, "label": "dup"})
    violations, _ = check(_write(tmp_path, doc))
    assert any("duplicate row index 1" in v for v in violations)


def test_cell_row_without_label_rejected(tmp_path):
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["rows"] = [{"index": 99, "label": "only"}]
    violations, _ = check(_write(tmp_path, doc))
    assert any("has no label" in v for v in violations)


def test_sparse_label_indices_are_green(tmp_path):
    # U2 does not require contiguous indices.
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["rows"].append({"index": 10, "label": "unused sparse"})
    violations, warnings = check(_write(tmp_path, doc))
    assert violations == []
    assert warnings == []


def test_self_target_relation_rejected(tmp_path):
    # AUDIT-2026-09-16 U3: a sum may not list its target as a source.
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["relations"][0]["sources"] = ["r3c1", "r1c1"]
    violations, _ = check(_write(tmp_path, doc))
    assert any("also a source" in v for v in violations)


def test_standalone_source_is_always_red(tmp_path):
    # AUDIT-2026-09-16 U1: DESIGN standalone means no arithmetic, but the
    # oracle only obligated totals and leaves. A source labelled standalone
    # must go red even under --no-strict-coverage.
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    doc["cells"][0]["role"] = "standalone"
    doc["cells"][0]["why"] = "synthetic standalone that still feeds a relation"
    path = _write(tmp_path, doc)
    violations, warnings = check(path)
    assert warnings == []
    assert any("standalone cell r1c1" in v for v in violations)
    lenient, _ = check(path, strict_coverage=False)
    assert any("standalone cell r1c1" in v for v in lenient)


def test_standalone_target_is_always_red(tmp_path):
    doc = json.loads(GREEN.read_text(encoding="utf-8"))
    total = next(c for c in doc["cells"] if c["id"] == "r3c1")
    total["role"] = "standalone"
    total["why"] = "synthetic standalone that is a relation target"
    path = _write(tmp_path, doc)
    violations, _ = check(path)
    assert any("standalone cell r3c1" in v for v in violations)


def test_cli_exit_codes(capsys):
    assert main([str(GREEN)]) == 0
    assert main([str(TYPO)]) == 1
    assert main([str(UNCOVERED)]) == 1  # strict by default
    assert main([str(UNCOVERED), "--no-strict-coverage"]) == 0  # lenient passes
    capsys.readouterr()

def test_corpus_table_ids_match_their_path():
    # AUDIT 2026-08-18 finding 2: 19 of 421 units carried a bare slug while
    # the manifest and the other 402 used <family>/<slug>, and the schema's
    # minLength:1 could not see it. The schema now requires a prefix; this
    # asserts the stronger property a pattern cannot express - that the
    # prefix is the unit's actual family directory.
    units = sorted((ROOT / "tables").glob("**/*.cells.json"))
    assert units, "corpus not found"
    mismatched = [
        p.relative_to(ROOT).as_posix()
        for p in units
        if json.loads(p.read_bytes().decode("utf-8"))["table_id"]
        != f"{p.parent.name}/{p.name[: -len('.cells.json')]}"
    ]
    assert mismatched == []


def test_corpus_is_utf8_lf_without_bom():
    # AUDIT 2026-08-18 finding 3: 78 of 421 units were committed CRLF while
    # the audit records assert "strict UTF-8 with LF and no BOM" as a gate.
    # .gitattributes pins it going forward; this is what fails if it drifts.
    # Byte literals are built numerically so this file can never itself be
    # mangled by an escape-interpreting edit - the defect class it guards.
    cr, bom = bytes([13]), bytes([239, 187, 191])
    offenders = []
    for p in sorted((ROOT / "tables").glob("**/*.cells.json")):
        raw = p.read_bytes()
        raw.decode("utf-8")  # strict - mojibake or stray bytes raise here
        if cr in raw or raw.startswith(bom):
            offenders.append(p.relative_to(ROOT).as_posix())
    assert offenders == []


def test_corpus_standalone_cells_do_not_participate():
    # AUDIT-2026-09-16 U1: 55 cells were standalone while feeding a relation.
    # The oracle now rejects that; this scan is the corpus-wide lock.
    offenders = []
    for p in sorted((ROOT / "tables").glob("**/*.cells.json")):
        doc = json.loads(p.read_bytes().decode("utf-8"))
        used: set[str] = set()
        for rel in doc.get("relations", []):
            used.update(rel.get("sources", []))
            if "target" in rel:
                used.add(rel["target"])
        for cell in doc["cells"]:
            if cell.get("role") == "standalone" and cell["id"] in used:
                offenders.append(
                    f"{p.relative_to(ROOT).as_posix()}:{cell['id']}"
                )
    assert offenders == []


def _tiny_corpus(tmp_path, *files: Path):
    dest = tmp_path / "tables" / "t"
    dest.mkdir(parents=True)
    for src in files:
        (dest / src.name).write_bytes(src.read_bytes())
    return tmp_path


def test_sweep_empty_selection_is_red(tmp_path, capsys):
    # AUDIT-2026-09-16 D6: an empty glob must not print ALL GREEN.
    (tmp_path / "tables").mkdir()
    assert sweep(tmp_path) == 1
    captured = capsys.readouterr()
    assert "no corpus files" in captured.out
    assert "GREEN" not in captured.out


def test_sweep_aggregates_failure(tmp_path, capsys):
    # AUDIT-2026-09-16 U5: a red unit followed by a green unit is still red.
    root = _tiny_corpus(tmp_path, GREEN, TYPO)
    assert sweep(root) == 1
    captured = capsys.readouterr()
    assert "of 2 unit(s) failed" in captured.out


def test_cli_all_rejects_extra_path():
    assert main(["--all", str(GREEN)]) == 2
