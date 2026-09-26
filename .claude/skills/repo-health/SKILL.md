---
name: repo-health
description: Read-only repo health check for the manuscript-tracking repo (tracker <-> snapshot files, "Pass logged" claims <-> room ledgers, room-ledger CURRENT STATE freshness, git state, memory mirror, handoff freshness). Run at session START (right after `git pull`) and at session CLOSE (before the merge to main). Reports only — it never edits, fixes, or rewrites anything, in the repo or in the ledgers.
---

# Repo health check

A mechanical, read-only sanity check on the plumbing that keeps the tracker, the room
ledgers, git, memory, and the session handoff note in sync with each other and with
the manuscripts on disk. It never touches a file — it only reads and reports.

## 1. Run it

```
PYTHONPATH=src py -m writing_tools.repo_health
```

Add `--json` for a machine-readable dump, `--repo-root <path>` if not run from the repo
root, or `--memory-dir <path>` to point at a different live-memory folder than the
default (`$WRITING_MEMORY_DIR`, else `%USERPROFILE%\.claude\projects\D--Claude-Writing\memory`).

Exit code 0 = every check passed. Exit code 1 = at least one FLAG.

## 2. Reading the output

Six sections, one per check, each marked `[PASS]` or `[FLAG]`:

1. Tracker vs snapshot files — every path and MD5 the tracker cites actually exists and matches.
2. Tracker "Pass logged" claims vs the room ledgers — every claimed Pass has a matching heading.
3. Room-ledger CURRENT STATE table freshness — the table's snapshot list matches what's on disk.
4. Git state — uncommitted changes, commits not yet merged to main, branch divergence.
5. Memory mirror — the live auto-memory folder vs `docs/auto-memory-backup/`.
6. Handoff freshness — whether work was logged after the last "START HERE" note.

`[PASS]` means nothing to do. `[FLAG]` lines name the file and the line/entry/heading
at fault, in plain English — read those lines to the author verbatim; don't summarize
them into jargon.

## 3. The one thing the script can't check — the master Doc (manual step)

The script only ever looks at files already in the repo. It has no way to see the live
Google Doc, so this step is done by hand (via the Drive connector), every run:

1. Read the master Doc, **"Tbd D1 Take 2"** (id `12krCIEuFEv1HlkPbTV63aGOnGDmvmApeTVq9JJY7qk4`).
2. Compare its `modifiedTime` to the newest `_docpull_` date among the manuscript snapshots.
   If the Doc was modified after the newest pull → **FLAG: "pull owed."**
3. List the Doc's section headings (Prologue / Chapter N / Interlude N) and compare them
   against the current room ledger's CURRENT STATE table. Any section in the Doc with no
   row in the table → **FLAG: "pull owed."**

Report this alongside the script's six sections, under the same PASS/FLAG language.

## 4. Rules

- **Never auto-fix.** This is a checker, not an editor. It reports; a person decides what to
  do about a FLAG.
- **The ledger and tracker are append-only.** A correction is a NEW appended entry, never a
  rewrite of an old one — even to fix something this check flagged.
- **A FLAG at session close holds the merge.** Per `docs/WORKING_RULES.md` rule 9's guardrail
  (do not merge on a conflict or clearly unfinished/broken work): if any check FLAGs at close,
  do not squash-merge to main — say so in ONE line and stop there.
- **Report to the author in plain language, verdict first** (`docs/WORKING_RULES.md` rules 5,
  7, 12 — he is not a coder). Lead with PASS or FLAG overall, then the specifics; no codes, no
  stack traces, no "run this command yourself."
