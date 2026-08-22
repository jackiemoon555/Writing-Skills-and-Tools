---
name: project_writing_repo_home
description: D:\Claude\Writing IS the local clone of jackiemoon555/Writing-Skills-and-Tools — read docs/SESSION_HANDOFF.md first every session; how to pull/push
metadata: 
  node_type: memory
  type: project
  originSessionId: a7293d7a-e885-4524-b0e1-0f8747a98121
  modified: 2026-08-22T15:40:30.484Z
---

`D:\Claude\Writing` is a git clone (made 2026-08-16) of the private GitHub repo
`jackiemoon555/Writing-Skills-and-Tools` — the standalone home of Alec's (pen name **Jack Moon**)
writing project. **Start every session by reading `docs/SESSION_HANDOFF.md` and `docs/WORKING_RULES.md`** — it is the
summary/index; `reports/`, `tracker/`, `docs/`, `manuscripts/` are the verbatim sources of truth.
The repo archives its legacy "notes to self" under `docs/archive-notes/` (renamed from
`docs/memory/` on 2026-08-22; deprecated — canonical rules live in `docs/WORKING_RULES.md`). The
live auto-memory namespace is git-backed up under `docs/auto-memory-backup/` (a snapshot refreshed
at handoff — never edit the mirror; edit the namespace).

**Why:** the handoff says writing sessions must run from this folder with their own memory
namespace, divorced from the sports-betting work; a fresh session here otherwise has no idea
where the handoff is (this one had to dig it out of the UFC-Bets namespace).

**How to apply:** `git pull` at session start (Alec also edits via PRs on GitHub — repo was
updated the same day it was cloned). Before `git push`, run
`"$LOCALAPPDATA/gh-portable/bin/gh.exe" auth setup-git` (gh is portable, not on PATH; auth'd as
jackiemoon555) or push hangs on a credential prompt. Do NOT run `git config` for identity —
flag it instead. Loose older writing files still sit in `D:\Claude\` root (forgotten_*.md/txt,
the-champ_outline.md, self-pub-playbook.md, the-fighter.docx, the-champ_budget.xlsx) — some
duplicate repo files; not moved, Alec's call.

**Manuscript source of truth (2026-08-18):** Google Docs — "The Champ — MASTER" (Drive file id
`1GJXagFpiiLhOweM9RO5ei3wciN4V06I4C1NDDs3KaO4`), readable live via the Drive connector; Reedsy retired as
master. He writes in Apple Notes on the phone → pastes to chat → pastes into the Doc → verifies at night.
Intake = read the Doc, snapshot to `manuscripts/`, count/MD5, checker silent. Git identity is set (commits as
Alec) — just commit + push.
