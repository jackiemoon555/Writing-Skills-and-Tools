# Third-party review brief — THE ROOM (the writing-partnership system itself)

*Prepared 2026-08-25 per WORKING_RULES rule 8 (cross-vendor check on substantive tooling).
Target: not a manuscript, not one script — the SYSTEM. Paste the block below into GPT and
Gemini, one honest teardown each, bring the reports back. Blind read first — do not show them
this file's header or any Claude commentary.*

---

## Paste-ready brief (paste everything inside the fence as your first message)

```
You are reviewing the DESIGN OF A SYSTEM, not a piece of writing. I want a genuinely
independent, blunt teardown. Full disclosure: the system was co-designed by me and Claude, and
Claude wrote this description of it. Same-family review can't catch an assumption both models
share — that's why I'm bringing it to you, a different vendor. No cushions, no praise padding.
If something is good, one line, then spend your words on what's wrong.

WHAT THE SYSTEM IS (all the context you get):
I'm a new fiction writer (pen name Jack Moon), two projects in, first novella draft complete
and in revision. I have ADHD. I've built a writing-partnership system with an AI (Claude) whose
explicit goal is to make ME a better writer — NOT to produce cleaner manuscripts faster. Its
core design choices:

1. NO GHOST-WRITING, structurally enforced. The AI never writes or rewrites a sentence of
   mine — fiction, blog, anything. It critiques, names the craft rule on MY quoted sentence,
   and I make every fix. If I ask it for "the fix," it names what the fix must accomplish and
   refuses to supply the line.
2. TWO FEEDBACK MENUS. Drafting-stage reads cover story/craft only (corny, not-working,
   needs-more, pacing, dialogue, show-vs-tell, repetition) — grammar/typos/POV are deliberately
   ignored until a piece is declared "in revision," where a separate protocol runs one lens per
   pass (structure → POV → line/grammar → mechanics).
3. ACTIVE RECALL. In revision, the AI names a defect class ONCE on one instance, then I must
   find the remaining instances myself; it confirms or corrects. Goal: build my editorial eye,
   not my dependence.
4. CALIBRATION LOG. After each revision pass I'm supposed to report which notes landed and
   which were noise; the log tunes future reads to my taste.
5. RECORD DISCIPLINE. Every draft batch is snapshotted verbatim with a hash and word count;
   author rulings and canon go in an append-only ledger; settled rulings are never re-litigated
   unless I reopen them. An automated checker flags echoes/filler/adverbs silently into report
   files (never surfaced mid-draft).
6. INDEPENDENT READS. On request: a fresh-context blind read by a separate agent that sees
   ONLY the manuscript (no ledgers, no history). At milestones: cross-vendor blind reads
   (exactly like this one) reconciled on the rule "both outside vendors agree = signal;
   house-only = suspect house taste."
7. ASK-FIRST CONTRACT. The AI proposes any action touching my writing or its records and
   waits for my yes; only pure plumbing (backups, version control) is autonomous.
8. REGISTER. Blunt, no praise sandwiches, verdict in the first line, one ask per message
   (ADHD accommodation). Genuine strengths get one line at the end or nothing.

KNOWN FAILURE MODES ALREADY OBSERVED (be harder than these, not softer):
- The AI once wrote a stale, long-superseded plot fact into the canon ledger (caught by me).
  A "stale-content finder" tool is now planned.
- Fixes I claim verbally get marked closed before the master document is re-checked
  ("verify-on-word gap").
- I under-feed the calibration log (the which-notes-landed loop often goes unclosed).
- Tool-building is seductive: I have a history of parking meta-tools ("cockpit dashboard")
  because building the system can substitute for writing.

FIVE IMPROVEMENTS CURRENTLY PROPOSED (refute or extend them):
1. A stale/superseded-content detector for the system's own records.
2. Auto-diff each new manuscript snapshot against the previous to verify claimed fixes landed.
3. Habit-level fix for the calibration loop (not a tool — discipline).
4. Actually fire the idle fresh-context blind-read bench at block milestones.
5. Script the currently-manual motif counting (per-chapter counts of repeated signature words).

Structure your answer:
1. DESIGN SOUNDNESS — does this system actually serve its stated goal (writer improvement over
   manuscript polish)? Where does the design quietly optimize for the wrong thing?
2. FAILURE MODES WE HAVEN'T NAMED — what will break, drift, or self-deceive that the "known
   failure modes" list misses? Think: dependency creep despite active recall, taste
   monoculture, record rot, the AI's incentives vs. mine, motivation/ADHD interactions.
3. THE FIVE PROPOSALS — for each: worth it, redundant, or harmful? Rank what's missing that
   would beat all five.
4. THE HARD QUESTION — is there any evidence-based reason to believe a system like this trains
   a writer better than simply writing more and getting occasional human feedback? Answer
   honestly; if the whole apparatus is overhead, say so.
5. VERDICT — keep as-is, keep with named changes (prioritized), or simplify drastically. Be
   decisive.

Verify claims against the description before making them. Don't invent problems to seem
thorough; if a part is sound, say "sound" and move on. 600–1000 words, plain markdown, then stop.
```

---

## After the reads (house process — not part of the paste)
- Optional single follow-up per vendor: "Try to refute: [one specific claim it made]." Once, then done.
- Paste each report into `reports/the-room_thirdparty_2026-08-25.md` (or hand them to Claude in chat).
- Claude reconciles per rule 8: both vendors agree = signal → act; Claude-only positions neither
  vendor supports = suspect house bias → downweight; one-vendor-only = author's call. Claude must
  flag any finding where an outside read OVERRULED a call Claude defended — that reversal is the
  point of the check.
