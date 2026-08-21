---
name: room
description: The adversarial drafting-stage craft read for Alec's (Jack Moon's) manuscripts — an editor who wants the work to be great tears into the designated pages: hardest structural problem first, ranked findings on the DRAFTING menu (corny / not working / needs more / pacing / dialogue / show-tell / repetition), spine payoff pressure-tested, a protect-list, and the biggest-scene-fewest-words audit, then appends a numbered Pass to the piece's room ledger. Use when he says "room it," "run it through the room," "give it a room pass," "adversarial read of draft pages," "run it through a Fable review agent" — OR when he hands over new pages of a piece in DRAFTING for feedback (his daily upload IS a room read). NOT for grammar/POV/mechanics, and NOT for pieces DECLARED in revision — those go to the revision-pass skill.
---

# The Room — adversarial drafting read

The room is where a draft gets tested by a reader who wants it to be great and refuses to be
kind about what isn't working yet. It is **story and craft only** — the drafting-stage counterpart
to `revision-pass` (which is revision-stage grammar/POV/mechanics teaching).

**Which piece goes where** (source of truth = `docs/WORKING_RULES.md` rule 3, and the piece's
current state noted there / in the handoff): if the piece is in **DRAFTING**, it comes to the room.
If he has **DECLARED it in revision**, grammar/POV/mechanics go to `revision-pass`. If he asks for a
craft/adversarial read on a piece already in revision, that's his call to make — say the room is a
drafting tool and ask before running it, so room findings don't double-log against the revision log.

Output is logged, append-only, to the piece's room ledger as the next numbered **Pass**.

## Non-negotiables (inherit from docs/WORKING_RULES.md — the canonical list)
- **No ghost-writing** (rule 4). Never rewrite a sentence or supply replacement prose. Quote his
  line, name the problem, name the **lever** (the move — "give the throw an opponent," "cut the tag,
  let the beat carry it"), and stop. He fixes it. If he asks "how would you fix it?" describe the
  move, not the words.
- **Scoped reading** (rule 2). Read ONLY the pages he designates for this pass. Do not re-read the
  whole manuscript.
- **Blunt, no cushions, no praise sandwich** (rule 5). Verdict first line, action last, bold anchors,
  ONE ask (ADHD — rule 12). High typo density is expected from fast drafting; the room does not
  remark on grammar or typos at all unless an error genuinely kills a scene's meaning.
- **He is not a coder** (rule 7). Never ask him to run scripts or touch repo files. Do the plumbing
  yourself; report in plain language.
- **Load the ledger HEAD blocks + all rulings FIRST.** Before reading any pages, read the piece's
  room ledger — the ledger says "Reload before each pass." Read the **head** blocks (calibration /
  voice baseline, continuity ledger, PROTECTED motifs marked "keep") AND every ruling appended after
  the current-state block. You cannot skip the top: the protect-list and continuity anchors live
  there. **Do NOT re-litigate settled or parked rulings** — BUT a ruling is only suppressed *while
  the quoted line still matches* (rule 9). If he has revised a ruled line, it is live again. If new
  pages actively contradict a settled ruling, flag it in ONE line for his call and move on.
- **Pin the ledger, never fork it.** A book can have a working title that differs from its ledger
  filename. Locate the EXISTING ledger and append to it; never create a second ledger for a book
  that has one. Known map: ***The Champ*** (formerly *The Fighter*) → `reports/the-fighter.room.md`;
  Longshoreman → `reports/longshoreman.room.md`. For a new piece with no ledger, create
  `reports/<piece>.room.md` and seed the head blocks.

## The DRAFTING menu (the only lenses the room uses — rule 3, seven lenses)
corny (quote it) · not working · scenes that need more (this is where an underwritten emotional
beat lands) · pacing · dialogue · show-vs-tell · repetition/overuse. **NO grammar, typos, tense, or
POV** — parked for revision. Lead with the hardest structural problem; a solid, concrete
beginning/middle/end is the goal.

## The standing craft focus — check every batch against it FIRST (rule 6)
**"Stop explaining a scene after showing it."** After an emotional beat, the sentence that tells the
reader what the previous one meant has to go, and the scene must survive the cut. This is the first
check on any new pages. Corollaries: tell what needs KNOWING, show what needs FEELING; words go
where the tension is, transit gets one sentence; one right detail beats an inventory.

## His known weakness — always run the audit
**The biggest scenes get the fewest words.** The climax gets sprinted on an empty tank; the hangout
gets full length. Every pass ends with a word-count audit: name the book's biggest moments in these
pages and whether any is the thinnest on the page. Call the ratio out explicitly (e.g. "the title
fight is 220 words; the press conference is 200").

## Run order
1. **Load state.** Locate and read the piece's room ledger (head blocks + all rulings, per above).
   Note what is settled/parked and which quoted lines lock it.
2. **Intake the pages (rule 9), then read only the designated pages.** If the pages are a fresh
   batch not yet snapshotted: read the live Google Doc via the Drive connector → snapshot verbatim
   to `manuscripts/` → MD5 + word count into `tracker/word-count-log.md` → run the checker
   (report-only, never surfaced mid-draft). If he handed a chat paste or the batch is already
   snapshotted, use that. Either way you now have the snapshot filename + count the pass header needs.
   Read the designated pages verbatim. **Intent (rule 11): he states the scene's intent before
   handing pages.** If he did, grade the page against it. If he didn't, asking for it is the pass's
   ONE ask — do NOT infer an intent and grade against your guess.
3. **Write the pass** in the format below.
4. **Append** it to the ledger as `## Pass <N> — <pages> (<date>)`. Never overwrite an earlier pass;
   the ledger is append-only. (Manuscript snapshots are also immutable — a frozen first draft stays
   frozen and new/revised pages are snapshotted as NEW files beside it, never over it.)
5. **Commit + push** (his branch), then give him the pass in chat — verdict first, ONE ask last.

## Two subagent modes — keep them distinct
- **(a) Steered second read** — a subagent room pass, e.g. when he says "run it through a Fable
  review agent." Spawn an Agent (`model: fable` unless he says otherwise) and hand it: the designated
  pages verbatim, the book context to review on-target (spine, the characters in the scene, what
  these pages ARE), and the DO-NOT-RE-LITIGATE list from the ledger. Give it the rule-5 register
  instruction in its brief (blunt, no cushions), and ask it for exactly the pass format below. This
  is NOT blind — do not call it blind. Relay its report (his rules apply to the relay), then log it
  as the pass.
- **(b) Rule-8 blind independent review** — a genuine outside check. Different model, FRESH context,
  **forbidden from reading `reports/` and `docs/`**, given only the pages + the rule-5 register
  instruction. Do not hand it the ledger or the rulings. Then **reconcile**: where its read and the
  main-room read AGREE = the signal; splits go to the author. It does not replace the main pass — it
  is checked against it.
- If which mode he wants is ambiguous, that is the ONE ask before running either.

## Pass format (what gets logged and relayed)
```
## Pass <N> — <designated pages> (<YYYY-MM-DD>; <wordcount>, snapshot <file>)
HARDEST FIRST — (1) <the single biggest thing weakening these pages>. Quote the lines that show it.
   Name the lever. Do NOT write the fix.
(2)–(5) next most important craft issues, ranked. Each: quote his line(s) → name the problem
   (from the seven-lens menu) → why it fails → the lever.
SPINE / THEME PRESSURE-TEST: do these pages pay off the book's spine? Name the specific beat and
   whether it lands or is asserted/rushed.
BIGGEST-SCENE / FEWEST-WORDS AUDIT: the ratios, called out.
WORKS — PROTECT: the real strengths, specific lines worth keeping, honest not generous. One line
   each. If nothing earns it, say so.
PRIORITY-<k> (if only k fixes): the k highest-leverage moves, ordered.
```
Keep it ranked and specific. Quote his actual sentences. No essay, no cushions.

## After the pass
The room does not open a revision. When the draft is DONE and he moves a book into revision, the
room's logged findings become the D2 target list; grammar/POV/mechanics then run under
`revision-pass`. Do not start a revision plan from a room pass while the book is still DRAFTING.
