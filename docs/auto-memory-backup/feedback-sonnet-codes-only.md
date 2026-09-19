---
name: feedback-sonnet-codes-only
description: "Delegate all coding to Sonnet, configured to ONLY code with minimal reasoning (author, 2026-08-23)"
metadata:
  type: feedback
---

Author instruction (2026-08-23): any coding work gets handed to a Sonnet subagent, and Sonnet
should ONLY code — no extended thinking/deliberation (set low reasoning effort, instruct it to
implement directly without analysis preamble).

**Why:** he wants the premium model (Fable) on writing/critique judgment and cheap fast execution
on plumbing; thinking tokens on mechanical code are waste.

**How to apply:** Agent tool with model: "sonnet", effort low, prompt framed as direct
implementation spec (exact files, exact behavior), not open-ended problem solving. Fable designs
the spec; Sonnet types it.

**BROADENED (author, 2026-09-19): "I really only want you to orchestrate, use sonnet/haiku for
any token intensive work."** Not just code. The main session (Fable) plans, writes specs, makes
judgment calls, reviews results, and does small repo plumbing. Anything token-heavy goes to a
Sonnet or Haiku subagent: digging through large folders or files, bulk web fetching and
extraction, long searches, matching big lists, log spelunking. He also said, the same day: the
main session writes NO code itself, and a code subagent builds code ONLY (one named file, no git,
no docs, never runs it on his data).

**Why (this instance):** Fable burned a slow blind search across an 8.7 GB game install in the
main session; he stopped it. Usage limits tightened after 2026-08-31 ([[project-usage-rollback-aug31]]).

**How to apply:** before any multi-step dig or bulk extraction, ask "is this orchestration or
labor?" Labor → Agent tool, model sonnet (or haiku for simple extraction), a bounded read-only
brief with hard limits and a short report-back format; run it in the background and keep
talking to him. The WRITING lane is the exception that stays with Fable: reading his pages and
writing room passes is judgment, not labor.
