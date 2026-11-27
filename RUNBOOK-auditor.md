# Auditor runbook — every-10th different-agent spot-audit

You were dispatched to audit a cadence unit (a multiple of 10, or
as directed). If the last ten shipped units share one transcriber, the
working practice is a **whole-batch positional check**, not a 10-cell
sample of the 10th unit alone (`NEXT.md` standing note; lesson from
unit #340). This file is your whole orientation.

**Hard rule:** you must NOT be the unit's transcriber (check the
AUDITS.md placeholder / project log for who shipped it). If you are,
stop and report.

**Read ONLY:** this file, `AGENTS.md` §§ 1–7, the target unit's
`.cells.json`, its `BACKLOG.md` row, its source file, and the ONE
previous audit entry in `AUDITS.md` (for the record format). Do not
read the rest of AUDITS.md or the log archives.

## Flow

0. **Preflight** as in RUNBOOK-transcriber.md step 0 (venv symlink,
   `git status` for orphaned work — uncommitted files from the
   transcriber are a finding to record and land, not to ignore).
1. **Independent extraction.** Re-read the source yourself — never
   audit the unit against its own claims.
   - **Start with the tracked source check.** Run it over the units you
     audit (a batch takes seconds, `--all` about a minute and a half):

     ```bash
     uv run --group sourcecheck python tools/sourcecheck.py --render scratchpad/<your-dir> tables/<family>/<unit>.cells.json ...
     ```

     *Row level:* the values of every unit row must be on ONE printed
     line of the source. This catches a wrong value, also in a
     `standalone` cell that no arithmetic sees. *Column level:* every
     cell must sit in the column the page prints it in, and where the
     unit has no cell the page must not print a number. This catches a
     value in the wrong column, two values swapped, a printed number the
     row leaves out, and a cell the page does not print. The tool prints
     one line per mismatch and exits 1 if there is any. `--render` saves
     a picture of the printed line of each mismatch: **look at it**
     before you record anything. A mismatch is a finding for
     `AUDITS.md`, not a licence to edit; repair only under step 5's
     rule.
   - **Known exceptions** of the tool live in
     `tools/sourcecheck-exceptions.json` (the Census `Z` convention; the
     four FEC capstone units whose rows gather several printed blocks).
     Each is still checked in its own way. Do not add an entry to make a
     run pass: a new entry is the user's decision, with the reason
     written into it.
   - **What the tool does not do:** it does not read labels, it cannot
     see a printed row that the unit lacks, and with very small numbers
     (the 1s and 2s of the OMB tables) a wrong value can pass because
     another printed line nearby carries the same values. So the rest of
     this step and steps 2 and 3 still apply in full. The tool is not one
     of the gates in step 4.
   - HTML/XBRL units: extraction is scriptable. **The whole-file value
     MULTISET comparison is mandatory**: collect every numeric
     `<td class="num|nump">` value in the source, compare as a multiset
     against every cell value in the unit. Counts AND values must match
     exactly. This is the ONLY cheap check that catches fabricated or
     duplicated rows — a sampled audit structurally cannot (lesson from
     unit #340: 6 invented cells passed a 10-cell sample because each
     value was printed *somewhere*).
   - PDF units: text layer (`uv run --with pdfplumber`) + a pypdfium2
     render you actually look at (vision required). Full-coverage value
     check for units ≤ ~60 cells; coverage-stratified sample of ≥ 10
     for larger ones, plus a full row-label and row-COUNT check against
     the print (missing standalone rows are invisible to strict
     coverage — defect class from units #129/#160).
2. **Labels + layout:** every row label, column model, and omission
   (blank ≠ zero) against the source. Cross-check row COUNTS, not just
   names.
3. **Relations:** recompute every declared relation in exact Decimal
   from the unit's own leaf cells. Every non-zero `tol` must equal the
   observed delta AND quote a printed rounding note — flag
   over-declared slack. Also ask whether that slack is **plausible for
   the reason it cites**: rounding cannot explain `tol` larger than the
   source count (the OPM Table 6-C November cell was a 51-unit typo
   absorbed as `tol=50`; `tol == delta` is not enough). Inventory
   identity classes the source prints (DESIGN §4a) — do not only verify
   declared relations. Unused columns that could close against a second
   identity are a missing-class smell (Table 6 has both a monthly and a
   fiscal-year roll-forward).
4. **Gates:** unit reconcile GREEN 0 warnings; `uv run pytest` green;
   full-corpus sweep (`uv run python reconcile.py --all`) all GREEN.
5. **Record:** replace the AUDITS.md placeholder with your audit entry
   (mirror the previous entry's section structure; verdict GREEN or the
   defect list). Real defects: repair only if mechanical and
   value-preserving (cite the #129/#160/#340 precedent, annotate
   `unit_note`, record in AUDITS.md); otherwise record RED and stop.
6. **Unblock + commit + clock out:** update NEXT.md's cadence line
   (#N+1 unblocked, next audit #N+10), then commit/push/clock-out
   exactly as RUNBOOK-transcriber.md steps 6–7, including the
   log-claim rules (only paste-able SHAs; "committed" only after
   `git log` shows it).
