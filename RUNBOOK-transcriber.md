# Transcriber runbook — dispatched single-unit session

You were dispatched to transcribe **one** table unit. This file is your
whole orientation. Budget: you should be transcribing within ~5k tokens
of reading, not 100k.

**Read ONLY:**
1. This file.
2. `AGENTS.md` §§ 1–7 (the discipline rules — schema, gate, tolerances).
3. Your unit's row in `BACKLOG.md` (grep for its id; do NOT read the
   whole file).
4. ONE exemplar unit from the same family (a sibling `.cells.json` in
   the same `tables/<family>/` folder — pick the closest shape).

**Do NOT read:** `AUDITS.md`, the full `BACKLOG.md`, `log-archive/`,
the atelier week log's history, or other families' units. The detail
there is for reviewers, not you.

## Flow

0. **Preflight.** `ls -la .venv/ | grep lib64` — if a `lib64 -> lib`
   symlink exists, `rm .venv/lib64` (known breaker; a red sweep through
   a broken venv is a venv problem, not a corpus problem). Then
   `git status --short` — if another agent left uncommitted work,
   STOP and report it before touching anything.
1. **Claim your unit.** It's the topmost Queue item in `NEXT.md` that
   fits your harness (HTML units need no vision; PDF units REQUIRE
   vision — text layer + a pypdfium2 page render, see NEXT's harness
   notes). Your corpus number = `ls tables/*/*.cells.json | wc -l` + 1.
   Do not trust a number from a log entry — count.
2. **Read the source** named in your BACKLOG row (under `sources/`,
   already vendored + sha256-ledgered — never re-download).
3. **Build** `tables/<family>/<table-id>.cells.json` — the ONE new
   file this session creates. Conventions that bite (full rules in
   AGENTS.md § 4):
   - Values exactly as printed: strip thousands separators and currency
     symbols, keep sign, parenthesized negatives → leading `-`.
   - Blank ≠ zero (omit blanks); a printed `0` IS a real cell.
   - Duplicate printed row labels get distinct keyed rows (year prefix
     or section suffix) — never merged.
   - A relation needs ≥ 2 sources (schema `minItems`); a printed
     equality with one source becomes `standalone` + `why`.
   - Tolerances only with the source's own rounding note quoted in
     `why`; on sec-10k HTML units expect EXACT — a sum that doesn't
     foot is YOUR error until proven otherwise.
4. **Gate.** All three, no exceptions:
   - `uv run python reconcile.py tables/<family>/<id>.cells.json`
     → `GREEN ... (0 warning(s))`, relation count ≥ your BACKLOG
     row's minimum.
   - `uv run pytest` → 10 passed.
   - `git status --short` shows exactly your one new file (+ the doc
     edits from step 5).
5. **Docs.** Update your BACKLOG row (`QUEUED` → `SHIPPED` with corpus
   #, cells/relations, one-line result) and NEXT.md (drop the Queue
   item, prepend a one-line Shipped entry). Nothing else.
6. **Commit — this step is NOT optional and happens BEFORE clock-out.**
   ```
   git add tables/<family>/<id>.cells.json BACKLOG.md NEXT.md
   git commit -m "ship corpus #<N>: <family>/<table-id> (<cells>c/<relations>r, strict-default GREEN)"
   git push origin main
   git log --oneline -1   # paste this SHA in your log entry
   ```
7. **Clock out** (atelier protocol, one command):
   ```
   katflow clock-out --agent "<YOUR name>" -m "<what you did>" -next "<what's next>"
   ```
   Log-claim rules: write "committed"/"pushed" ONLY after `git log`
   shows the SHA, and cite ONLY SHAs you can paste from real output.
   An unverifiable claim is worse than "not committed" — reviewers
   verify everything.

## Special cases

- **Every-10th audit gate:** if your corpus number is a multiple of 10,
  add a placeholder entry at the bottom of `AUDITS.md` (copy the shape
  of the previous placeholder) and state in NEXT.md that #N+1 is
  blocked. You CANNOT audit your own unit.
- **Anything surprising** (source looks wrong, total doesn't foot, a
  row your BACKLOG spec doesn't mention): STOP, log the finding in your
  clock-out note, don't improvise a fix (AGENTS.md § 4).
- **Never** invent a row the source doesn't print — even with the
  arithmetically correct value. Cells are printed values, full stop
  (defect class caught at unit #340).
