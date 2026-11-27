#!/usr/bin/env python3
"""sourcecheck: compare units with their vendored sources.

reconcile.py proves the arithmetic a unit declares. It cannot see a cell that
takes part in no arithmetic, and it cannot see a number that sits in the wrong
column of a row whose sums still close. This tool reads the source itself.

Row level
    The values of a unit row must all be found on ONE printed line of the
    source: one line of the PDF character layer on the cited page (two pages
    before to four after it, then the whole document for rows taken from
    elsewhere), or one <tr> of an HTML source.

Column level
    Each cell must sit in the column the page prints it in, and where the unit
    has no cell the page must not print a number. Nothing about the columns is
    configured: a cell is placed by the horizontal position of its printed
    number, the rows of a unit must agree with each other about where each
    column is, and rows are matched to printed lines in reading order. A
    missing cell is counted as sitting on dots or `(**)`, or on empty paper.

Values are compared as exact strings. There is no numeric tolerance anywhere.
The few constants below describe how characters are grouped into lines and
tokens; they never decide whether two numbers are "close enough".

Usage
    uv run --group sourcecheck python tools/sourcecheck.py --all
    uv run --group sourcecheck python tools/sourcecheck.py tables/<family>/<unit>.cells.json ...
    ... --render DIR     also save a picture of the printed line of each mismatch

One line is printed per mismatch. The exit code is 1 when there is any mismatch
(or a stale entry in the exceptions file) and 0 otherwise. The known exceptions
in tools/sourcecheck-exceptions.json are not skipped: each replaces the usual
check by the one its convention calls for. The tool only reads; it never edits
a unit.

What it does not check: row and column labels, and whether a printed row is
absent from the unit. A wrong value still passes the row level when another
printed line nearby carries the row's values, which happens with the very small
numbers (1, 2) of the OMB tables.

This is an auditor's tool, not a gate: it needs the PDF libraries of the
optional `sourcecheck` dependency group and takes a minute or two over the corpus.
"""

from __future__ import annotations

import argparse
import bisect
import html as html_lib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCEPTIONS_FILE = Path(__file__).resolve().with_name("sourcecheck-exceptions.json")

# How the character layer is read (PDF points). Not value tolerances.
LINE_PITCH = 2.2  # characters whose tops differ by no more than this share a printed line
WORD_GAP = 1.2  # a horizontal gap wider than this separates two tokens
BODY_SHARE = 0.80  # glyphs smaller than this share of the page's digit size are superscripts
NEAR_BEFORE, NEAR_AFTER = 2, 4  # pages searched around the cited page before the whole document

# Families whose source pages are set in two columns of text. Their printed
# lines are split at the centre of the page (unless a line runs across it), the
# left column is read before the right one, and positions in the right column
# are measured from that column's own margin, so a table that runs on from one
# text column into the other keeps its column positions.
TWO_COLUMN_FAMILIES = {"omb"}

CID = re.compile(r"\(cid:(\d+)\)")
_NUMBER = r"\d[\d,]*(?:\.\d+)?"
NUMBER = re.compile(r"-?" + _NUMBER)
# One printed entry: (123) and "- 123" are negatives, dots and (**) mark an empty cell.
SCAN = re.compile(
    r"\(\s*\$?\s*(?P<paren>" + _NUMBER + r")\s*\)"
    r"|(?<![\d,.])-\s{1,2}(?P<spaced>" + _NUMBER + r")"
    r"|(?P<plain>-?" + _NUMBER + r")"
    r"|(?P<blank>\(\*\*\)|\.{2,})"
)
DASHES = str.maketrans({"−": "-", "–": "-", "—": "-", " ": " "})


# --------------------------------------------------------------------------
# text
# --------------------------------------------------------------------------


def decode_cid(text: str) -> str:
    """The May 2026 statement stores its text as undecoded glyph codes."""
    return CID.sub(lambda m: chr(int(m.group(1)) + 29), text)


def numbers_in(text: str) -> list[str]:
    """Every number printed in a piece of text, thousands separators removed."""
    text = text.translate(DASHES)
    text = re.sub(r"\(\s*\$?\s*(" + _NUMBER + r")\s*\)", r"-\1", text)
    text = re.sub(r"(?<![\d,.])-\s{1,2}(?=\d)", "-", text)
    return [m.group(0).replace(",", "") for m in NUMBER.finditer(text)]


def spellings(value: str) -> list[str]:
    """The ways a unit value may be printed: 5.0 as 5, 0.5 as .5."""
    out = [value]
    if "." in value:
        out.append(value.rstrip("0").rstrip("."))
        if value.startswith("0."):
            out.append(value[1:])
        if value.startswith("-0."):
            out.append("-" + value[2:])
    return out


def uncovered(values: list[str], printed: Counter) -> list[str]:
    """The values of a unit row that a printed line does not carry (as a multiset)."""
    left = Counter(printed)
    missing = []
    for value in values:
        for spelling in spellings(value):
            if left[spelling] > 0:
                left[spelling] -= 1
                break
        else:
            missing.append(value)
    return missing


# --------------------------------------------------------------------------
# printed lines
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Token:
    kind: str  # "num", "blank" (dots or (**)) or "word"
    text: str  # the number without separators, or the printed text
    x0: float
    x1: float


@dataclass
class Line:
    page: int | None  # 1-based PDF page; None for an HTML source
    pos: float  # position in reading order within the page
    text: str
    values: Counter  # the numbers printed on the line (row level)
    tokens: list[Token]  # positioned entries (column level)
    box: tuple | None = None  # (x0, top, x1, bottom) on the page, for renders
    rotated: bool = False
    column: int = 0  # text column of a two-column page
    wide: bool = False  # on a two-column page: the line runs across both columns

    @property
    def key(self):
        return (self.page or 0, self.column, self.pos)


def tokens_of(text: str, extent) -> list[Token]:
    """Positioned tokens of one line. extent(a, b, digits_only) gives the
    horizontal span of the characters text[a:b]."""
    out = []
    for m in SCAN.finditer(text):
        if m.group("blank"):
            x0, x1 = extent(m.start(), m.end(), False)
            out.append(Token("blank", m.group("blank"), x0, x1))
            continue
        if m.group("paren"):
            value = "-" + m.group("paren")
        elif m.group("spaced"):
            value = "-" + m.group("spaced")
        else:
            value = m.group("plain")
        # the right edge of a number is its last digit: a closing parenthesis or
        # a trailing comma is not part of the column alignment
        x0, _ = extent(m.start(), m.end(), False)
        _, x1 = extent(m.start(), m.end(), True)
        out.append(Token("num", value.replace(",", ""), x0, x1))
    for m in re.finditer(r"\S+", text):
        x0, x1 = extent(m.start(), m.end(), False)
        out.append(Token("word", m.group(0), x0, x1))
    return out


def line_from_glyphs(glyphs, page, pos, box=None, rotated=False) -> Line:
    """glyphs: (text, x0, x1) along the reading direction."""
    glyphs = sorted(glyphs, key=lambda g: g[1])
    chars, owner = [], []
    prev_x1 = None
    for i, (text, x0, x1) in enumerate(glyphs):
        if prev_x1 is not None and x0 - prev_x1 > WORD_GAP:
            chars.append(" ")
            owner.append(None)
        for ch in text:
            chars.append(ch)
            owner.append(i)
        prev_x1 = x1
    text = "".join(chars).translate(DASHES)

    def extent(a, b, digits_only):
        idx = [owner[i] for i in range(a, b) if owner[i] is not None and (not digits_only or text[i].isdigit())]
        return glyphs[idx[0]][1], glyphs[idx[-1]][2]

    tokens = tokens_of(text, extent)
    values = Counter(t.text for t in tokens if t.kind == "num")
    return Line(page, pos, text, values, tokens, box, rotated)


def cluster(items, key, pitch=LINE_PITCH):
    items = sorted(items, key=key)
    groups, current = [], []
    for item in items:
        if current and key(item) - key(current[0]) > pitch:
            groups.append(current)
            current = []
        current.append(item)
    if current:
        groups.append(current)
    return groups


def page_lines(chars, page_no: int, width: float, height: float, two_columns: bool = False) -> list[Line]:
    """The printed lines of one PDF page, from pdfplumber character dicts.

    Footnote superscripts are dropped by size. A page whose digits are mostly
    rotated (the landscape Census tables) is read in its own direction. With
    two_columns, a line that does not run across the centre of the page is
    split there into a left and a right line.
    """
    glyphs = []
    for c in chars:
        text = decode_cid(c["text"])
        if not text.strip():
            continue
        upright = bool(c.get("upright", True))
        # the extent of a glyph across its baseline: its height when upright,
        # its width when the text runs up or down the page
        measure = c["size"] if upright else c["x1"] - c["x0"]
        glyphs.append((text, c, upright, round(measure, 1)))
    if not glyphs:
        return []
    digit_sizes = Counter(g[3] for g in glyphs if g[0].isdigit())
    usual = (digit_sizes or Counter(g[3] for g in glyphs)).most_common(1)[0][0]
    body = [g for g in glyphs if g[3] >= BODY_SHARE * usual]
    digits = [g for g in body if g[0].isdigit()]
    rotated = bool(digits) and sum(1 for g in digits if not g[2]) > len(digits) / 2

    def box_of(group):
        return (
            min(g[1]["x0"] for g in group),
            min(g[1]["top"] for g in group),
            max(g[1]["x1"] for g in group),
            max(g[1]["bottom"] for g in group),
        )

    lines = []
    if not rotated:
        middle = width / 2
        for group in cluster(body, key=lambda g: g[1]["top"]):
            parts = [(0, group)]
            split = two_columns and not any(g[1]["x0"] < middle < g[1]["x1"] for g in group)
            if split:
                parts = [
                    (0, [g for g in group if g[1]["x1"] <= middle]),
                    (1, [g for g in group if g[1]["x0"] >= middle]),
                ]
            for column, part in parts:
                if not part:
                    continue
                line = line_from_glyphs(
                    [(g[0], g[1]["x0"], g[1]["x1"]) for g in part],
                    page_no,
                    min(g[1]["top"] for g in part),
                    box_of(part),
                )
                line.column = column
                line.wide = two_columns and not split
                lines.append(line)
        return lines

    turned = [g for g in body if not g[2]]
    # the second matrix entry is the vertical part of the writing direction:
    # positive means the text reads from the bottom of the page to the top
    upward = sum(1 for g in turned if (g[1].get("matrix") or (0, 1))[1] > 0) >= len(turned) / 2
    if upward:
        def along(c):
            return height - c["bottom"], height - c["top"]

        def across(c):
            return c["x0"]
    else:
        def along(c):
            return c["top"], c["bottom"]

        def across(c):
            return width - c["x1"]
    for group in cluster(turned, key=lambda g: across(g[1])):
        line = line_from_glyphs(
            [(g[0],) + along(g[1]) for g in group],
            page_no,
            min(across(g[1]) for g in group),
            box_of(group),
            rotated=True,
        )
        lines.append(line)
    return lines


def align_text_columns(pages: list[list[Line]]):
    """Measure the right text column from its own margin. The distance between
    the two margins is read off the pages (the leftmost ink of each column) and
    the value most pages agree on is used for the whole document."""
    seen = Counter()
    for page in pages:
        left = [t.x0 for line in page if line.column == 0 and not line.wide for t in line.tokens]
        right = [t.x0 for line in page if line.column == 1 for t in line.tokens]
        if left and right:
            seen[round(min(right) - min(left), 1)] += 1
    if not seen:
        return
    shift = seen.most_common(1)[0][0]
    for page in pages:
        for line in page:
            if line.column == 1:
                line.tokens = [Token(t.kind, t.text, t.x0 - shift, t.x1 - shift) for t in line.tokens]


def html_lines(raw: str) -> list[Line]:
    """One line per <tr>. The row level reads the row's text as a whole; the
    column level places each number by the table column of its cell."""

    def clean(fragment):
        text = html_lib.unescape(re.sub(r"(?s)<[^>]+>", " ", fragment))
        text = re.sub(r"\(\s+", "(", text)
        text = re.sub(r"\s+\)", ")", text)
        return re.sub(r"\$\s+", "$", text)

    lines = []
    for n, row in enumerate(re.findall(r"(?is)<tr\b.*?</tr>", raw)):
        text = clean(row)
        tokens = []
        column = 0
        for attrs, inner in re.findall(r"(?is)<t[dh]\b([^>]*)>(.*?)</t[dh]>", row):
            span = re.search(r"(?i)colspan\s*=\s*[\"']?(\d+)", attrs)
            cell_text = clean(inner).translate(DASHES)
            tokens.extend(tokens_of(cell_text, lambda a, b, d, c=column: (c, c + 0.5)))
            column += int(span.group(1)) if span else 1
        lines.append(Line(None, float(n), " ".join(text.split()), Counter(numbers_in(text)), tokens))
    return lines


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------


class Sources:
    """Reads each source once. pages() gives a list of pages, each a list of lines."""

    def __init__(self):
        self._cache = {}

    def pages(self, path: Path, two_columns: bool = False) -> list[list[Line]]:
        key = (str(path), two_columns)
        if key not in self._cache:
            if path.suffix.lower() == ".pdf":
                self._cache[key] = self._pdf(path, two_columns)
            else:
                raw = path.read_text(encoding="utf-8", errors="replace")
                self._cache[key] = [html_lines(raw)]
        return self._cache[key]

    @staticmethod
    def _pdf(path: Path, two_columns: bool) -> list[list[Line]]:
        try:
            import pdfplumber
        except ImportError:
            raise SystemExit(
                "sourcecheck needs pdfplumber to read a PDF source. Run it as:\n"
                "    uv run --group sourcecheck python tools/sourcecheck.py ..."
            )
        pages = []
        with pdfplumber.open(str(path)) as pdf:
            for number, page in enumerate(pdf.pages, start=1):
                pages.append(page_lines(page.chars, number, float(page.width), float(page.height), two_columns))
                page.flush_cache()
        if two_columns:
            align_text_columns(pages)
        return pages


# --------------------------------------------------------------------------
# units and known exceptions
# --------------------------------------------------------------------------


@dataclass
class Unit:
    path: Path
    name: str  # the table_id, e.g. treasury-mts/2026-06-table9
    family: str
    source: Path
    page: int | None
    columns: list[int]
    labels: dict[int, str]
    rows: dict[int, list[dict]]  # row index -> its cells, in column order

    @classmethod
    def load(cls, path: Path) -> "Unit":
        doc = json.loads(Path(path).read_bytes().decode("utf-8"))
        rows = defaultdict(list)
        for cell in doc["cells"]:
            rows[cell["row"]].append(cell)
        for cells in rows.values():
            cells.sort(key=lambda c: c["col"])
        return cls(
            path=Path(path),
            name=doc["table_id"],
            family=Path(path).resolve().parent.name,
            source=ROOT / doc["source"]["path"],
            page=doc["source"].get("page"),
            columns=sorted(c["index"] for c in doc["columns"]),
            labels={r["index"]: r["label"] for r in doc["rows"]},
            rows=dict(sorted(rows.items())),
        )


class Exceptions:
    """The explicit list of known exceptions (tools/sourcecheck-exceptions.json).

    printed_as     a cell whose value the page prints as a marker, by a
                   documented transcription convention (Census prints Z for a
                   value that rounds to zero). The check looks for that marker
                   on the row's line and in the cell's column.
    combined_rows  units whose rows gather several printed blocks by design, so
                   no single printed line carries a row. Every value must still
                   be printed in the source. Their columns are not compared.
    """

    def __init__(self, doc: dict | None = None):
        doc = doc or {}
        self.printed_as = {(e["unit"], e["cell"]): e for e in doc.get("printed_as", [])}
        self.combined = {e["unit"]: e for e in doc.get("combined_rows", [])}
        self.used = set()
        self.rows_seen = {}

    @classmethod
    def load(cls, path: Path) -> "Exceptions":
        return cls(json.loads(Path(path).read_bytes().decode("utf-8")))

    def marker(self, unit: Unit, cell: dict):
        entry = self.printed_as.get((unit.name, cell["id"]))
        if entry is None or entry["value"] != cell["value"]:
            return None
        self.used.add((unit.name, cell["id"]))
        return entry["printed"]

    def is_combined(self, unit: Unit) -> bool:
        if unit.name not in self.combined:
            return False
        self.rows_seen[unit.name] = len(unit.rows)
        return True

    def stale(self, checked_units: set) -> list[str]:
        """Entries that no longer describe the units that were checked."""
        out = []
        for (unit, cell), entry in self.printed_as.items():
            if unit in checked_units and (unit, cell) not in self.used:
                out.append(f"printed_as {unit} {cell}: the unit no longer holds {entry['value']} there")
        for unit, entry in self.combined.items():
            if unit in checked_units and entry["rows"] != self.rows_seen.get(unit):
                out.append(f"combined_rows {unit}: lists {entry['rows']} rows, the unit has {self.rows_seen.get(unit)}")
        return out


# --------------------------------------------------------------------------
# row level
# --------------------------------------------------------------------------


@dataclass
class RowResult:
    scope: str | None  # "near", "doc", "combined", or None when no line carries the row
    lines: list[Line]  # every printed line that carries the row
    missing: list[str]  # for a row not found: what its nearest line lacks
    best: Line | None = None


def is_marker(token: Token, marker: str) -> bool:
    return token.kind == "word" and token.text.strip("*") == marker


def check_row(values, markers, near, doc) -> RowResult:
    """Find the printed lines that carry all values (and markers) of a row."""
    best = None
    for scope, lines in (("near", near), ("doc", doc)):
        hits = []
        for line in lines:
            missing = uncovered(values, line.values)
            missing += [m for m in markers if not any(is_marker(t, m) for t in line.tokens)]
            if not missing:
                hits.append(line)
            elif best is None or len(missing) < len(best[0]):
                best = (missing, line)
        if hits:
            return RowResult(scope, hits, [])
        if doc is near:
            break
    return RowResult(None, [], best[0] if best else list(values), best[1] if best else None)


# --------------------------------------------------------------------------
# column level
# --------------------------------------------------------------------------


def overlap(a0, a1, b0, b1) -> float:
    return min(a1, b1) - max(a0, b0)


def embed(cells, line: Line, markers):
    """Place the cells of a row, in column order, on the entries of a line read
    left to right. Returns for each cell the tokens it could be, or None when
    the line does not carry the values in that order."""
    printed = sorted((t for t in line.tokens if t.kind in ("num", "word")), key=lambda t: (t.x0, t.x1))

    def fits(cell, token):
        marker = markers.get(cell["id"])
        if marker is not None:
            return is_marker(token, marker)
        return token.kind == "num" and token.text in spellings(cell["value"])

    earliest, at = [], -1
    for cell in cells:
        at = next((i for i in range(at + 1, len(printed)) if fits(cell, printed[i])), None)
        if at is None:
            return None
        earliest.append(at)
    latest, at = [], len(printed)
    for cell in reversed(cells):
        at = next(i for i in range(at - 1, -1, -1) if fits(cell, printed[i]))
        latest.append(at)
    latest.reverse()
    out = []
    for n, cell in enumerate(cells):
        lo = earliest[n - 1] if n else -1
        hi = latest[n + 1] if n + 1 < len(cells) else len(printed)
        out.append([printed[i] for i in range(lo + 1, hi) if fits(cell, printed[i])])
    return out


def in_reading_order(candidates: list[list[tuple]]) -> list[list[tuple]]:
    """Unit rows follow the page from top to bottom. Among the printed
    positions each row could have, keep those that lie on a longest chain of
    rows in reading order. A row on no such chain (a total re-anchored from
    another page) keeps all its positions."""

    def chains(rows):
        tails, out = [], []
        for positions in rows:
            got = {p: bisect.bisect_left(tails, p) + 1 for p in sorted(set(positions))}
            for p, n in got.items():
                if n > len(tails):
                    tails.append(p)
                elif p < tails[n - 1]:
                    tails[n - 1] = p
            out.append(got)
        return out, len(tails)

    def mirror(p):
        return tuple(-x for x in p)

    forward, longest = chains(candidates)
    backward, _ = chains([[mirror(p) for p in positions] for positions in reversed(candidates)])
    backward.reverse()
    kept = []
    for positions, ahead, behind in zip(candidates, forward, backward):
        on_chain = sorted(p for p in set(positions) if ahead[p] + behind[mirror(p)] - 1 == longest)
        kept.append(on_chain or sorted(set(positions)))
    return kept


@dataclass
class Frame:
    """One printed grid: for each unit column, the horizontal stretch that every
    number printed in that column shares."""

    cores: dict = field(default_factory=dict)  # column -> (x0, x1)
    rows: set = field(default_factory=set)  # (row, line key) of the rows that agree

    def has_other_row(self, row) -> bool:
        return any(r != row for r, _ in self.rows)

    def fits(self, placed: dict) -> int:
        """Columns shared with a row's placed tokens; -1 when one disagrees."""
        shared = 0
        for col, token in placed.items():
            if col in self.cores:
                if overlap(token.x0, token.x1, *self.cores[col]) <= 0:
                    return -1
                shared += 1
        return shared

    def add(self, row, placed: dict):
        for col, token in placed.items():
            if col in self.cores:
                lo, hi = self.cores[col]
                self.cores[col] = (max(lo, token.x0), min(hi, token.x1))
            else:
                self.cores[col] = (token.x0, token.x1)
        self.rows.add(row)

    def agrees(self, other: "Frame") -> bool:
        return all(overlap(*self.cores[c], *other.cores[c]) > 0 for c in self.cores.keys() & other.cores.keys())

    def merge(self, other: "Frame"):
        for col, (lo, hi) in other.cores.items():
            if col in self.cores:
                self.cores[col] = (max(lo, self.cores[col][0]), min(hi, self.cores[col][1]))
            else:
                self.cores[col] = (lo, hi)
        self.rows |= other.rows


def build_frames(placements: dict) -> list[Frame]:
    """placements: (row, line key) -> {column: token} for the cells whose printed
    token on that line is not in doubt. Rows that agree about where their
    columns are form a frame."""
    frames: list[Frame] = []
    for row, placed in sorted(placements.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if not placed:
            continue
        fitting = [f for f in frames if f.fits(placed) > 0]
        if not fitting:
            frame = Frame()
            frame.add(row, placed)
            frames.append(frame)
            continue
        fitting.sort(key=lambda f: -f.fits(placed))
        home = fitting[0]
        home.add(row, placed)
        for other in fitting[1:]:
            if home.agrees(other):
                home.merge(other)
                frames.remove(other)
    return frames


def extend_frame(frame: Frame, columns: list[int], lines: list[Line]):
    """Locate the columns in which no row of the frame has a cell, from what the
    page prints there (dots, (**) or a number) on the lines of the frame's rows.

    Between two located columns the page must print exactly as many entries as
    the unit has columns there. Left or right of all located columns the
    nearest entries are taken, but only when the located columns are shown to
    be neighbours on the page (nothing printed between two adjacent ones), and
    only when every line agrees on where those entries are.
    """
    rows = []
    for line in lines:
        rows.append(sorted((t for t in line.tokens if t.kind in ("num", "blank")), key=lambda t: (t.x0, t.x1)))

    def centre(span):
        return (span[0] + span[1]) / 2

    def between(entries, lo, hi):
        return [
            t
            for t in entries
            if (lo is None or (overlap(t.x0, t.x1, *lo) <= 0 and centre((t.x0, t.x1)) > centre(lo)))
            and (hi is None or (overlap(t.x0, t.x1, *hi) <= 0 and centre((t.x0, t.x1)) < centre(hi)))
        ]

    located = sorted(frame.cores)
    index = {col: n for n, col in enumerate(columns)}
    adjacent = [(a, b) for a, b in zip(located, located[1:]) if index[b] - index[a] == 1]
    neighbours = bool(adjacent) and all(
        not between(entries, frame.cores[a], frame.cores[b]) for a, b in adjacent for entries in rows
    )
    new = {}
    runs, run = [], []
    for col in columns:
        if col in frame.cores:
            if run:
                runs.append(run)
            run = []
        else:
            run.append(col)
    if run:
        runs.append(run)
    for run in runs:
        lower = max((c for c in located if c < run[0]), default=None)
        upper = min((c for c in located if c > run[-1]), default=None)
        lo = frame.cores[lower] if lower is not None else None
        hi = frame.cores[upper] if upper is not None else None
        picks = []
        for entries in rows:
            found = between(entries, lo, hi)
            if lo is not None and hi is not None:
                if not found:
                    continue  # empty paper on this line
                if len(found) != len(run):
                    picks = None
                    break
            elif not neighbours or len(found) < len(run):
                continue
            else:
                found = found[-len(run):] if lo is None else found[: len(run)]
            picks.append(found)
        if not picks or (len(picks) < 2 and (lo is None or hi is None)):
            continue
        for n, col in enumerate(run):
            core = (max(p[n].x0 for p in picks), min(p[n].x1 for p in picks))
            if core[1] - core[0] <= 0:
                break
            new[col] = core
    frame.cores.update(new)


def describe(tokens) -> str:
    numbers = [t.text for t in tokens if t.kind == "num"]
    if numbers:
        return "prints " + " and ".join(numbers)
    blanks = [t.text for t in tokens if t.kind == "blank"]
    if blanks:
        return "prints " + ("dots" if blanks[0].startswith(".") else blanks[0])
    return "prints nothing"


def compare(unit: Unit, cells, line: Line, frame: Frame, markers):
    """Compare one row with one printed line under one frame.
    Returns (problems, tally); problems is a list of (cell id, text)."""
    problems = []
    tally = Counter()
    by_col = {c["col"]: c for c in cells}
    located = sorted(frame.cores)

    def in_column(col):
        lo, hi = frame.cores[col]
        return [t for t in line.tokens if overlap(t.x0, t.x1, lo, hi) > 0]

    def column_of(token):
        hits = [(overlap(token.x0, token.x1, *frame.cores[c]), c) for c in located]
        hits = [h for h in hits if h[0] > 0]
        return max(hits)[1] if hits else None

    def is_cell(token, cell):
        marker = markers.get(cell["id"])
        if marker is not None:
            return is_marker(token, marker)
        return token.kind == "num" and token.text in spellings(cell["value"])

    row = cells[0]["row"]
    for col in unit.columns:
        cell = by_col.get(col)
        cid = cell["id"] if cell else f"r{row}c{col}"
        if col not in frame.cores:
            if cell is None:
                tally["missing-unplaced"] += 1
                continue
            # no other row prints this column: the value must at least sit
            # between the columns to its left and right
            lower = max((frame.cores[c][1] for c in located if c < col), default=float("-inf"))
            upper = min((frame.cores[c][0] for c in located if c > col), default=float("inf"))
            if any(is_cell(t, cell) for t in line.tokens if t.x0 >= lower and t.x1 <= upper and column_of(t) is None):
                tally["present-between"] += 1
            else:
                problems.append((cid, f"{cell['value']} is not printed between the neighbouring columns"))
            continue
        here = in_column(col)
        if cell is None:
            numbers = [t for t in here if t.kind == "num"]
            if numbers:
                problems.append((cid, f"the unit has no cell, the page {describe(numbers)} in this column"))
            elif any(t.kind == "blank" for t in here):
                tally["missing-on-marker"] += 1
            else:
                tally["missing-on-empty"] += 1
            continue
        if any(is_cell(t, cell) for t in here):
            tally["present"] += 1
            continue
        where = ""
        for t in line.tokens:
            if t.kind == "num" and t.text in spellings(cell["value"]) and t not in here:
                other = column_of(t)
                if other is not None:
                    where = f"; {cell['value']} is printed in the column of c{other}"
                else:
                    where = f"; {cell['value']} is printed outside the unit's columns"
                break
        printed = describe([t for t in here if t.kind != "word"])
        problems.append((cid, f"the unit has {cell['value']}, the page {printed} in this column{where}"))
    return problems, tally


@dataclass
class Mismatch:
    level: str  # "row" or "column"
    unit: str
    row: int
    cell: str | None
    text: str
    label: str = ""
    line: Line | None = None

    def render(self) -> str:
        where = f" p{self.line.page}" if self.line is not None and self.line.page else ""
        target = self.cell or f"r{self.row}"
        label = f" [{self.label[:60]}]" if self.label else ""
        return f"{self.level.upper():6} {self.unit} {target}{where}: {self.text}{label}"


def check_columns(unit: Unit, results: dict, markers_by_row: dict):
    """Column level for the rows the row level found. Returns (mismatches, tally)."""
    tally = Counter()
    mismatches: list[Mismatch] = []
    rows = [r for r in unit.rows if results[r].scope in ("near", "doc")]
    if not rows:
        return mismatches, tally

    # 1. where each row could be, with its cells in column order
    spots: dict[int, dict] = {}  # row -> {line key: (line, tokens per cell)}
    for row in rows:
        found = {}
        for line in results[row].lines:
            placed = embed(unit.rows[row], line, markers_by_row[row])
            if placed is not None:
                found[line.key] = (line, placed)
        spots[row] = found

    # 2. rows are in reading order: keep, for each row, the lines that fit that order
    allowed = dict(zip(rows, in_reading_order([sorted(spots[r]) for r in rows])))

    # 3. frames, from cells whose printed token is not in doubt. A row printed
    #    in two places (the same line in two tables) takes part in both.
    placements = {}
    for row in rows:
        for key in allowed[row]:
            line, placed = spots[row][key]
            placements[(row, key)] = {
                cell["col"]: tokens[0] for cell, tokens in zip(unit.rows[row], placed) if len(tokens) == 1
            }
    frames = [f for f in build_frames(placements) if len({r for r, _ in f.rows}) > 1]
    for frame in frames:
        extend_frame(frame, unit.columns, [spots[r][key][0] for r, key in sorted(frame.rows)])

    # 4. every row against the frames that other rows establish
    for row in rows:
        cells = unit.rows[row]
        label = unit.labels.get(row, "")
        tally["column-rows"] += 1
        lines = [spots[row][key][0] for key in allowed[row]]
        if not lines:
            # the values are on a printed line, but not in the unit's column order
            lines = results[row].lines
        best = None
        for line in lines:
            for frame in frames:
                if not frame.has_other_row(row):
                    continue
                problems, row_tally = compare(unit, cells, line, frame, markers_by_row[row])
                if best is None or len(problems) < len(best[0]):
                    best = (problems, row_tally, line)
                if not problems:
                    break
            if best is not None and not best[0]:
                break
        if best is None:
            tally["column-rows-alone"] += 1
            text = "no other row of the unit shares this row's printed columns, so its columns could not be compared"
            mismatches.append(Mismatch("column", unit.name, row, None, text, label, lines[0]))
            continue
        problems, row_tally, line = best
        if problems:
            tally["column-rows-off"] += 1
            for cid, text in problems:
                mismatches.append(Mismatch("column", unit.name, row, cid, text, label, line))
        else:
            tally["column-rows-ok"] += 1
            for key, count in row_tally.items():
                tally["column-" + key] += count
    return mismatches, tally


def check_unit(unit: Unit, sources: Sources, exceptions: Exceptions, levels=("row", "column")):
    """Check one unit against its source. Returns (mismatches, tally)."""
    pages = sources.pages(unit.source, unit.family in TWO_COLUMN_FAMILIES)
    doc = [line for page in pages for line in page]
    if unit.source.suffix.lower() == ".pdf" and unit.page is not None:
        near = [
            line
            for number, page in enumerate(pages, start=1)
            if unit.page - NEAR_BEFORE <= number <= unit.page + NEAR_AFTER
            for line in page
        ]
    else:
        near = doc
    tally = Counter(units=1)
    mismatches: list[Mismatch] = []
    combined = exceptions.is_combined(unit)
    everywhere = Counter()
    if combined:
        for line in doc:
            everywhere.update(line.values)

    results: dict[int, RowResult] = {}
    markers_by_row: dict[int, dict] = {}
    for row, cells in unit.rows.items():
        label = unit.labels.get(row, "")
        tally["rows"] += 1
        tally["cells"] += len(cells)
        markers = {}
        for cell in cells:
            marker = exceptions.marker(unit, cell)
            if marker is not None:
                markers[cell["id"]] = marker
                tally["known-printed-as"] += 1
        markers_by_row[row] = markers
        values = [c["value"] for c in cells if c["id"] not in markers]
        if combined:
            tally["known-combined-rows"] += 1
            absent = [v for v in values if not any(everywhere[s] > 0 for s in spellings(v))]
            if absent:
                text = f"{', '.join(absent)} is not printed anywhere in the source"
                mismatches.append(Mismatch("row", unit.name, row, None, text, label))
            else:
                tally["combined-rows-in-source"] += 1
            results[row] = RowResult("combined", [], [])
            continue
        result = check_row(values, list(markers.values()), near, doc)
        results[row] = result
        if result.scope is None:
            tally["rows-not-found"] += 1
            ids = ", ".join(c["id"] for c in cells if c["value"] in result.missing)
            text = f"no printed line carries this row; the nearest one lacks {', '.join(result.missing)} ({ids})"
            mismatches.append(Mismatch("row", unit.name, row, None, text, label, result.best))
        else:
            tally["rows-on-one-line"] += 1
            tally["rows-" + result.scope] += 1

    if "row" not in levels:
        mismatches = []
    if "column" in levels:
        found, column_tally = check_columns(unit, results, markers_by_row)
        mismatches += found
        tally.update(column_tally)
    return mismatches, tally


# --------------------------------------------------------------------------
# renders
# --------------------------------------------------------------------------


def render_line(source: Path, line: Line, target: Path, scale: float = 3.0, margin: float = 28.0):
    """Save a picture of one printed line with some of the page around it."""
    import pypdfium2

    pdf = pypdfium2.PdfDocument(str(source))
    try:
        image = pdf[line.page - 1].render(scale=scale).to_pil()
    finally:
        pdf.close()
    x0, top, x1, bottom = line.box
    if line.rotated:
        box = (int(max(0, x0 - margin) * scale), 0, int(min(image.width, (x1 + margin) * scale)), image.height)
        crop = image.crop(box).rotate(-90, expand=True)
    else:
        box = (0, int(max(0, top - margin) * scale), image.width, int(min(image.height, (bottom + margin) * scale)))
        crop = image.crop(box)
    target.parent.mkdir(parents=True, exist_ok=True)
    crop.save(str(target))


# --------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------


SUMMARY = [
    ("rows", "rows"),
    ("rows-on-one-line", "found on one printed line"),
    ("rows-doc", "of those, outside the cited pages"),
    ("rows-not-found", "NOT found on one printed line"),
    ("known-combined-rows", "known exception: rows that gather several printed blocks"),
    ("combined-rows-in-source", "of those, with every value printed in the source"),
    ("known-printed-as", "known exception: cells printed as a marker"),
    ("column-rows", "rows compared column by column"),
    ("column-rows-ok", "rows with every cell in its printed column"),
    ("column-rows-off", "rows with a cell OUT of its printed column"),
    ("column-rows-alone", "rows whose columns could NOT be compared"),
    ("column-present", "cells on their printed number"),
    ("column-present-between", "cells placed between their neighbours only"),
    ("column-missing-on-marker", "missing cells on dots or (**)"),
    ("column-missing-on-empty", "missing cells on empty paper"),
    ("column-missing-unplaced", "missing cells in a column the unit never fills (not located)"),
]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare units with their vendored sources, row by row and column by column.",
    )
    parser.add_argument("units", nargs="*", type=Path, help="unit files (*.cells.json)")
    parser.add_argument("--all", action="store_true", help="check every unit under tables/")
    parser.add_argument("--level", choices=("row", "column", "both"), default="both")
    parser.add_argument("--render", type=Path, metavar="DIR", help="save a picture of the printed line of each mismatch")
    parser.add_argument("--exceptions", type=Path, default=EXCEPTIONS_FILE, help="known-exceptions file")
    parser.add_argument("--quiet", action="store_true", help="print mismatches only, no summary")
    args = parser.parse_args(argv)

    if args.all == bool(args.units):
        parser.error("give unit files or --all (not both)")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    paths = sorted((ROOT / "tables").glob("*/*.cells.json")) if args.all else args.units
    if not paths:
        print("no unit files found", file=sys.stderr)
        return 2
    levels = ("row", "column") if args.level == "both" else (args.level,)
    exceptions = Exceptions.load(args.exceptions)
    sources = Sources()
    per_family = defaultdict(Counter)
    mismatches: list[Mismatch] = []
    checked = set()
    for path in paths:
        unit = Unit.load(path)
        checked.add(unit.name)
        found, tally = check_unit(unit, sources, exceptions, levels)
        per_family[unit.family].update(tally)
        mismatches += found
        for m in found:
            print(m.render())
            if args.render and m.line is not None and m.line.page:
                name = unit.name.replace("/", "__") + f"-r{m.row}.png"
                render_line(unit.source, m.line, args.render / name)
    stale = exceptions.stale(checked)
    for text in stale:
        print(f"STALE  {text}")

    if not args.quiet:
        if mismatches or stale:
            print()
        for family in sorted(per_family):
            tally = per_family[family]
            print(f"{family}: {tally['units']} unit(s)")
            for key, label in SUMMARY:
                if tally[key]:
                    print(f"    {label}: {tally[key]}")
        print()
        print(f"{len(mismatches)} mismatch(es), {len(stale)} stale exception(s) in {len(checked)} unit(s)")
    return 1 if mismatches or stale else 0


if __name__ == "__main__":
    sys.exit(main())
