# MEMORY SYSTEM — architecture, health & improvement backlog

*The single home for how this project's memory is organized and where it's headed. Pointed to from
`SESSION_HANDOFF.md`. When the memory system changes, update it HERE.*

---

## Where memory lives (the layers)

1. **Auto-memory namespace** — `C:\Users\alec_\.claude\projects\D--Claude-Writing\memory\`
   (`MEMORY.md` index + fact files). Loads automatically each session. **Machine-local, outside git.**
   Backed up into the repo at `docs/auto-memory-backup/` (a snapshot, refreshed at handoff).
2. **Repo canonical** — `docs/`: `WORKING_RULES.md` (THE rules), `ROOM_CORE.md` (distillation),
   `SESSION_HANDOFF.md` (orientation/state), `PROJECT_CONTEXT.md` (older catch-up).
3. **Archived notes** — `docs/archive-notes/` (was `docs/memory/`, renamed 2026-08-22): legacy
   "notes to self." **Deprecated / history only** — superseded by `WORKING_RULES.md`.
4. **Working ledgers** — `reports/` (room ledgers) + `tracker/` (word-count log, comps, reading).

**Precedence:** `WORKING_RULES.md` wins. `ROOM_CORE.md` distills it; everything else defers. If two
places disagree, the rules page is right and the other is stale.

---

## Health check

**Strengths**
- Survives a cold start — a fresh session (new model, wiped auto-memory) rebuilds from
  `SESSION_HANDOFF.md` → `WORKING_RULES.md`. Nothing load-bearing dies with the chat.
- Declared single source of truth with an explicit tiebreaker (prevents drift → ambiguity).
- Clean separation of concerns; versioned in git (diffable, dated, with commit-message rationale).

**Weaknesses (open ones tracked in the backlog below)**
- Redundancy across layers → **drift** (the recurring failure; e.g. a hard-coded rule count).
- `SESSION_HANDOFF.md` is append-only and **bloating** — current state buried under dated history.
- Manual sync burden — each change must be propagated by hand across layers.

---

## Improvement backlog

### ✅ Done (2026-08-22)
1. **Fixed live drift** — removed the hard-coded rule count from the auto-memory index; count now
   lives only in `WORKING_RULES.md`.
2. **Killed the naming collision** — `docs/memory/` → `docs/archive-notes/`; all refs updated;
   folder flagged deprecated.
3. **Backed up the auto-memory** — `docs/auto-memory-backup/` git-tracks the one layer outside
   version control; refresh step written into `WORKING_RULES.md` rule 9.

### ⬜ Remaining (priority order)
4. **Compact the handoff (biggest).** Split `SESSION_HANDOFF.md` into a short **STATE** block
   (rewritten each session) + a frozen **ARCHIVE** (dated addenda, never edited). ~1 dedicated pass.
5. **One-home rule, enforced.** Audit for any fact stated in two places; make one the home, the rest
   pointers. Ongoing hygiene; a first sweep catches the next drift early.
6. **Timestamp volatile facts.** Any memory citing a specific file/path/number gets a "last-verified"
   date, so a session re-checks before asserting. Cheapest next win. (Auto-memory already injects age
   warnings — extend the habit to repo docs.)
7. **Scheduled consolidation pass.** Weekly / at each reset, one session reconciles layers, prunes
   stale entries, rolls up the handoff. The `anthropic-skills:consolidate-memory` skill fits this.

### 🤔 Worth considering
8. **Automate the mirror refresh.** Today the auto-memory→repo copy relies on a session remembering
   (rule 9). A Stop hook would do it every session automatically. Trade-off: harness config
   (`settings.json`) — a bit of plumbing.
9. **Prune-on-encode.** When a fact graduates into a rule or into code, DELETE it from memory instead
   of leaving a duplicate. Prevents accretion — the slow way memory systems rot.

---

## The governing principle

Every fix above is one of two moves:
- **Reduce forks** — one authored home per fact; everything else is a pointer; prune duplicates.
- **Date what rots** — timestamp any claim about a specific file, path, or number.

The system doesn't need new machinery. It needs those two habits, run regularly. A memory system's
real enemy isn't forgetting — it's **stale confidence**: a note that's wrong but stated plainly gets
trusted. Fewer sources, dated when volatile.

*Established 2026-08-22.*
