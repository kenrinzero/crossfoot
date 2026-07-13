> **Managed under atelier.** Before starting, read
> `C:\Users\kenrin\Project\.atelier\CHARTER.md` (from WSL:
> `/mnt/c/Users/kenrin/Project/.atelier/CHARTER.md`), the current week log in
> `.atelier\logs\`, and this project's brief + log at
> `.atelier\projects\coding\crossfoot\`. Clock out per the charter when done.

<!-- Project-specific instructions below this line. -->

# Working on Crossfoot

1. **Read `DESIGN.md`** (frozen), then take a READY unit from
   `BACKLOG.md` — `NEXT.md` holds the suggested order, difficulty tiers,
   and harness needs. One session = one table.
2. **A transcription unit touches exactly one new file** —
   `tables/<family>/<table-id>.cells.json`. It never edits `reconcile.py`,
   `schema/`, vendored `sources/`, or another unit's table. New relation
   types / schema needs are separate harness units — stop and log if you
   hit one.
3. **The gate:** `uv run python reconcile.py <your file>` exits 0, with
   **zero coverage warnings**, and your relation count ≥ the manifest's
   minimum. Also keep `uv run pytest` green.
4. **Transcription discipline:** values are decimal STRINGS exactly as
   printed (strip thousands separators; keep sign); row/col labels are
   required; parenthesized accounting negatives become `-`; a cell that
   genuinely participates in no arithmetic is `role: standalone` with a
   `why`. A non-default tolerance requires quoting the source's own
   rounding note in `why` — never invent slack to make a sum close. If a
   published total truly doesn't foot and the source doesn't say why, STOP
   and log it (that's a finding, not a tolerance).
5. **Do not re-derive sources.** If a table looks wrong in the vendored
   file, the vendored file is still the ground truth for this corpus —
   note discrepancies in the unit's `note` fields.
6. Every 10th shipped unit: non-arithmetic spot-audit by a DIFFERENT agent
   (labels/units/periods + 10 sampled cells vs the source) → `AUDITS.md`.
