# Auto-memory backup (git-tracked snapshot — NOT the live copy)

**This is a backup, not the source of truth.** The LIVE auto-memory namespace is:
`C:\Users\alec_\.claude\projects\D--Claude-Writing\memory\` — outside this repo, machine-local,
loaded automatically each session. That namespace is the only memory layer with no git history and
no off-site copy, so it is mirrored here so a dead machine loses nothing.

## Rules
- **Read/edit the LIVE namespace, never these files.** Edits here do nothing — they are not loaded.
- **Refresh at handoff:** copy `…\memory\*.md` → this folder, then commit (part of the handoff
  routine, WORKING_RULES.md rule 9). This snapshot is only as fresh as the last handoff.
- Safe to commit: these notes carry instructions and project facts only — no secrets, no work
  address (see `user_work_email_private.md`, which records the rule, not the address).

*Established 2026-08-22.*
