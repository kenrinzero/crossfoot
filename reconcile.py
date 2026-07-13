#!/usr/bin/env python3
"""reconcile.py — the Crossfoot oracle (DESIGN.md §§ 3-4). FROZEN semantics;
extending relation types or coverage rules is an explicitly-scoped harness
unit, never part of a transcription unit.

Usage: reconcile.py <file.cells.json> [--no-strict-coverage]

Checks, in order: JSON Schema validity; referential integrity (cell ids
unique + consistent with row/col, relation refs exist); every declared
relation re-derived from leaf values in exact Decimal arithmetic; coverage
(DESIGN.md § 4 — errors by default, warnings under --no-strict-coverage).
Exit 0 = green; non-zero = red. Importable: check(path, strict_coverage).
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

import jsonschema

_SCHEMA_PATH = Path(__file__).resolve().parent / "schema" / "cells.schema.json"

DEFAULT_TOL = {"sum": Decimal("0"), "percent-closure": Decimal("0.05")}
DEFAULT_CLOSURE_TOTAL = Decimal("100")


def check(path: str | Path, strict_coverage: bool = True):
    """Return (violations, warnings) — green iff violations is empty."""
    violations: list[str] = []
    warnings: list[str] = []

    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(
        json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    )
    schema_errors = [
        f"schema: {e.json_path}: {e.message}" for e in validator.iter_errors(doc)
    ]
    if schema_errors:
        return schema_errors, warnings

    cells: dict[str, dict] = {}
    for cell in doc["cells"]:
        cid = cell["id"]
        if cid in cells:
            violations.append(f"duplicate cell id {cid}")
        if cid != f"r{cell['row']}c{cell['col']}":
            violations.append(
                f"cell {cid}: id inconsistent with row/col "
                f"(r{cell['row']}c{cell['col']})"
            )
        cells[cid] = cell

    def value(cid: str) -> Decimal:
        return Decimal(cells[cid]["value"])

    targets: set[str] = set()
    sources_used: set[str] = set()

    for i, rel in enumerate(doc["relations"]):
        refs = list(rel["sources"]) + ([rel["target"]] if "target" in rel else [])
        missing = [r for r in refs if r not in cells]
        if missing:
            violations.append(f"relation[{i}]: unknown cell ref(s) {missing}")
            continue
        tol = Decimal(rel["tol"]) if "tol" in rel else DEFAULT_TOL[rel["type"]]
        if "tol" in rel and Decimal(rel["tol"]) != DEFAULT_TOL[rel["type"]] and "why" not in rel:
            violations.append(
                f"relation[{i}]: non-default tol {rel['tol']} requires a why"
            )
        total = sum((value(s) for s in rel["sources"]), Decimal("0"))
        sources_used.update(rel["sources"])
        if rel["type"] == "sum":
            expected = value(rel["target"])
            targets.add(rel["target"])
            delta = abs(total - expected)
            if delta > tol:
                violations.append(
                    f"relation[{i}] sum -> {rel['target']}: sources total {total}, "
                    f"target {expected}, |delta| {delta} > tol {tol}"
                )
        else:  # percent-closure
            expected = Decimal(rel.get("total", str(DEFAULT_CLOSURE_TOTAL)))
            delta = abs(total - expected)
            if delta > tol:
                violations.append(
                    f"relation[{i}] percent-closure: sources total {total}, "
                    f"expected {expected} ±{tol}, |delta| {delta}"
                )

    # coverage (DESIGN.md § 4): totals must be targeted, leaves must feed
    for cid, cell in cells.items():
        if cell["role"] == "total" and cid not in targets:
            (violations if strict_coverage else warnings).append(
                f"coverage: total cell {cid} is not the target of any relation"
            )
        if cell["role"] == "leaf" and cid not in sources_used:
            (violations if strict_coverage else warnings).append(
                f"coverage: leaf cell {cid} feeds no relation"
            )
    return violations, warnings


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    strict = "--no-strict-coverage" not in argv
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    violations, warnings = check(args[0], strict_coverage=strict)
    for w in warnings:
        print(f"WARN {w}")
    for v in violations:
        print(f"RED  {v}")
    if violations:
        print(f"RED: {len(violations)} violation(s) in {args[0]}")
        return 1
    print(f"GREEN: {args[0]} reconciles ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
