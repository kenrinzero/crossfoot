# Auditor runbook — every-10th different-agent spot-audit

You were dispatched to audit **one** corpus unit (a multiple of 10, or
as directed). This file is your whole orientation.

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
   over-declared slack.
4. **Gates:** unit reconcile GREEN 0 warnings; `uv run pytest` green;
   full-corpus sweep (`for f in tables/*/*.cells.json; ...`) all GREEN.
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
