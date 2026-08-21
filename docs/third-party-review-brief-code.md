# Third-party review brief — GPT + Gemini as an independent check on CODING / TOOLING work

*Drafted 2026-08-21. Purpose: the same discipline as the manuscript brief, aimed at CODE and TOOLING
— skills, scripts, repo automation, config, any non-trivial logic Claude builds in this repo. Claude
writes it and a second Claude model (Fable) checks it; same-family review can't catch an assumption
both models share. A different vendor can. Author's rule: it's a quality check, not a co-author.*

## When this runs (author, 2026-08-21)
- **Substantive / reusable coding work** gets a cross-vendor pass: a new or materially changed skill,
  a script or tool, repo automation (hooks/CI), or non-trivial logic. Trivial edits (a typo fix, a
  one-line tweak, a rename) skip it.
- It is **prepared-and-offered, not a hard gate.** Claude generates the paste-ready brief below at
  the right moment and hands it over; the author runs GPT + Gemini when he wants and brings the
  reports back. Work is never blocked waiting on the paste — the brief is a deliverable, the run is
  his call. (He can widen this to "everything" or tighten it any time — his dial.)
- Flow: Claude builds → Claude/Fable self-review → **Claude produces this brief** → author pastes
  into GPT and Gemini → Claude reconciles.

## The note (read before pasting)
It's not your engineer; it's a stranger you're paying for one honest teardown. Front-load everything
in the first message, hand it the artifact, take the report, leave. No relationship, no iteration.
If it starts agreeing with everything or rewriting the whole thing from scratch — that's the answer;
close the tab and use what was useful.

## Paste-ready brief (fill the brackets; paste the artifact AFTER this text)
```
You are reviewing [a skill file / a script / a tool / a config] for a solo project. I want a
genuinely independent, blunt teardown. Full disclosure so you know why: this was written by Claude
and reviewed by a second Claude model. Same-family review can't catch a wrong assumption both models
share — that's why I'm bringing it to you, a different vendor. No cushions, no praise padding. If
it's good, say so in one line and spend your words on what's wrong.

WHAT IT IS (all the context you get): [2–4 sentences: what the artifact does, when it runs, what it
is deliberately NOT for, and any sibling tool it must stay separate from.]

THE RULES / CONTRACT IT MUST HONOR (condensed): [paste the house rules or spec the artifact is
supposed to obey — the shorter the better; if none, say "none, judge it on its own logic."]

[OPTIONAL — a measured signal, if you have one: e.g. "an automated triggering test showed X." Ask
the reviewer to weigh in on whether your interpretation of that result is right.]

Structure your answer:
1. FAITHFULNESS / CORRECTNESS — does it do what it claims, completely? Anything it silently drops,
   contradicts, or gets subtly wrong versus the contract above?
2. SEPARATION / SCOPE — does it overlap, collide with, or leave a gap against any sibling tool or
   its own stated boundaries?
3. FOOTGUNS — anything that would make a future run misbehave, produce the wrong output, corrupt
   state, assume infrastructure that may be absent, or fail silently.
4. VERDICT — ship as-is, ship with named edits (list them, prioritized), or rework. Be decisive.

Verify each claim against the actual text before making it. Don't invent problems to seem thorough;
if a section is fine, say "fine" and move on.

THE ARTIFACT (verbatim):
[paste]
```

## Reconcile (where the answers go)
Paste each report into `reports/<artifact>_thirdparty_<date>.md` (or keep them in-session for a
one-off). Claude reconciles under WORKING_RULES rule 8:
- **GPT + Gemini agree (and/or a measured result agrees)** = the real signal → act on it.
- **Claude/Fable-only** (neither vendor raised it) = suspect house bias → hold or downweight.
- **One-vendor-only** = the author's call.
Claude states plainly which findings are signal, which are noise, and — importantly — flags where the
outside read **overruled a call Claude defended.** That reversal is the whole point of the check.

## What NOT to do
- Don't feed it the repo, the handoff, or Claude's own review before its blind read.
- Don't let it rewrite the whole artifact; take the diagnosis, not the ghost-written replacement.
- Don't iterate more than once. Blind read → (optional) single "try to refute X" → done.
