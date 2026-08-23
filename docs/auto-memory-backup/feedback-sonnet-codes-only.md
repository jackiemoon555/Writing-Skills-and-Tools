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
