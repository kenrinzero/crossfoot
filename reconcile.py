#!/usr/bin/env python3
"""reconcile.py — the Crossfoot oracle (DESIGN.md §§ 3-4). FROZEN semantics;
extending relation types or coverage rules is an explicitly-scoped harness
unit, never part of a transcription unit.

Usage: reconcile.py <file.cells.json> [--no-strict-coverage]
       reconcile.py --all [--no-strict-coverage]

Checks, in order: JSON Schema validity; referential integrity (cell ids
unique + consistent with row/col, relation refs exist, label indices
unique, every cell row/col has a label, no direct self-target sums);
every declared relation re-derived from leaf values in exact Decimal
arithmetic; coverage (DESIGN.md § 4 — totals targeted, leaves feed,
standalone participates in no relation; the first two are errors by
default and warnings under --no-strict-coverage; a standalone-in-relation
contradiction is always an error). `--all` walks tables/*/*.cells.json,
fails if the selection is empty, and returns nonzero if any unit is red
or warned. Exit 0 = green; non-zero = red. Importable: check, sweep.
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
    row_labels: set[int] = set()
    col_labels: set[int] = set()
    for item in doc["rows"]:
        idx = item["index"]
        if idx in row_labels:
            violations.append(f"duplicate row index {idx}")
        row_labels.add(idx)
    for item in doc["columns"]:
        idx = item["index"]
        if idx in col_labels:
            violations.append(f"duplicate column index {idx}")
        col_labels.add(idx)

    for cell in doc["cells"]:
        cid = cell["id"]
        if cid in cells:
            violations.append(f"duplicate cell id {cid}")
        if cid != f"r{cell['row']}c{cell['col']}":
            violations.append(
                f"cell {cid}: id inconsistent with row/col "
                f"(r{cell['row']}c{cell['col']})"
            )
        if cell["row"] not in row_labels:
            violations.append(
                f"cell {cid}: row {cell['row']} has no label"
            )
        if cell["col"] not in col_labels:
            violations.append(
                f"cell {cid}: col {cell['col']} has no label"
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
        if rel.get("target") in rel["sources"]:
            violations.append(
                f"relation[{i}]: target {rel['target']} is also a source"
            )
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

    # coverage (DESIGN.md § 4): totals targeted, leaves feed, standalone
    # participates in no relation. The first two follow strict_coverage;
    # a standalone cell used as a source or target is always a violation
    # (AUDIT-2026-09-16 U1 — role contradiction, not under-declaration).
    for cid, cell in cells.items():
        if cell["role"] == "total" and cid not in targets:
            (violations if strict_coverage else warnings).append(
                f"coverage: total cell {cid} is not the target of any relation"
            )
        if cell["role"] == "leaf" and cid not in sources_used:
            (violations if strict_coverage else warnings).append(
                f"coverage: leaf cell {cid} feeds no relation"
            )
        if cell["role"] == "standalone" and (
            cid in sources_used or cid in targets
        ):
            violations.append(
                f"coverage: standalone cell {cid} participates in a relation"
            )
    return violations, warnings


def corpus_files(root: str | Path) -> list[Path]:
    """Shipped corpus units: tables/<family>/<id>.cells.json."""
    return sorted(Path(root).joinpath("tables").glob("*/*.cells.json"))


def sweep(
    root: str | Path,
    *,
    strict_coverage: bool = True,
    out=None,
) -> int:
    """Failure-aggregating nonempty corpus gate. 0 iff every unit is green."""
    if out is None:
        out = sys.stdout
    files = corpus_files(root)
    if not files:
        print("RED: no corpus files under tables/*/*.cells.json", file=out)
        return 1
    errors = 0
    root_path = Path(root)
    for path in files:
        rel = path.relative_to(root_path).as_posix()
        violations, warnings = check(path, strict_coverage=strict_coverage)
        if not violations and not warnings:
            continue
        errors += 1
        for w in warnings:
            print(f"WARN {rel}: {w}", file=out)
        for v in violations:
            print(f"RED  {rel}: {v}", file=out)
    if errors:
        print(f"RED: {errors} of {len(files)} unit(s) failed", file=out)
        return 1
    print(f"GREEN: {len(files)} unit(s)", file=out)
    return 0


def main(argv: list[str]) -> int:
    flags = [a for a in argv if a.startswith("--")]
    args = [a for a in argv if not a.startswith("--")]
    strict = "--no-strict-coverage" not in flags
    unknown = [f for f in flags if f not in ("--all", "--no-strict-coverage")]
    if unknown:
        print(__doc__, file=sys.stderr)
        return 2
    if "--all" in flags:
        if args:
            print(__doc__, file=sys.stderr)
            return 2
        return sweep(Path(__file__).resolve().parent, strict_coverage=strict)
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
