---
name: room
description: The adversarial drafting-stage craft read for Alec's (Jack Moon's) manuscripts — an editor who wants the work to be great tears into the designated pages: hardest structural problem first, ranked findings on the DRAFTING menu (corny / not working / needs more / pacing / dialogue / show-tell / repetition), spine payoff pressure-tested, a protect-list, and the biggest-scene-fewest-words audit, then appends a numbered Pass to the piece's room ledger. The Room is EXPLICITLY invoked — run it when he says "room it," "run it through the room," "give it a room pass," "adversarial read of draft pages," or "run it through a Fable review agent." Do NOT infer a Room run from the mere arrival of new pages or a generic "is this good?" — those get an ordinary read unless he asks for the room. NOT for grammar/POV/mechanics, and NOT for pieces DECLARED in revision — those go to the revision-pass skill.
---

# The Room — adversarial drafting read

The room is where a draft gets tested by a reader who wants it to be great and refuses to be
kind about what isn't working yet. It is **story and craft only** — the drafting-stage counterpart
to `revision-pass` (which is revision-stage grammar/POV/mechanics teaching).

**Which piece goes where** (source of truth = `docs/WORKING_RULES.md` rule 3, and the piece's
current state noted there / in the handoff). Piece state controls routing: if the piece is in
**DRAFTING**, it comes to the room; if he has **DECLARED it in revision**, grammar/POV/mechanics go
to `revision-pass`. An explicit "room it" can override the state — but only run a drafting-stage
craft read on revision material after confirming that's what he wants, so room findings don't
double-log against the revision log.

**Mixed request** — if one message asks for both craft and mechanics ("fix the POV here, but also
tell me if the scene works"), split the work: the room handles story/craft, `revision-pass` handles
grammar/POV/mechanics. Never let one skill silently absorb the other's scope.

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
- **Load the ledger HEAD blocks first, plus the rulings that bear on these pages.** Before reading
  any pages, read the piece's room ledger (it says "Reload before each pass"). The **head** blocks
  are mandatory every time — calibration / voice baseline, continuity ledger, PROTECTED motifs
  marked "keep" — you cannot skip the top; the protect-list and continuity anchors live there. Then
  read the rulings that touch the submitted pages, characters, and threads. As the ledger grows you
  need not re-digest every historical ruling verbatim, but never skip one that bears on what he just
  handed you. **Do NOT re-litigate settled or parked rulings** — with one unlock: a ruling is
  suppressed while the underlying decision still holds. If he has **materially** reworked the ruled
  line (changed what it does, not just polished a word or punctuation), it is live again; a cosmetic
  edit to a still-settled line does NOT reopen it. If new pages actively contradict a settled ruling,
  flag it in ONE line for his call and move on.
- **Pin the ledger, never fork it; positively identify the piece before creating one.** A book can
  have a working title that differs from its ledger filename. Locate the EXISTING ledger and append
  to it; never create a second ledger for a book that has one. Known map: ***The Champ*** (formerly
  *The Fighter*) → `reports/the-fighter.room.md`; Longshoreman → `reports/longshoreman.room.md`. Only
  create `reports/<piece>.room.md` for a piece you can positively confirm has no ledger yet — if the
  identity is ambiguous (possible working-title/rename collision), ASK before creating anything.

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
gets full length. Every pass ends with a word-count audit: name the **most narratively consequential
beats** in the submitted pages — the highest-stakes turns, not the longest or loudest — and whether
any is the thinnest on the page. Call the ratio out explicitly (e.g. "the title fight is 220 words;
the press conference is 200").

## Run order
The craft read is the deliverable. **Bookkeeping (intake, logging, commit) is best-effort and must
never block the read** — if the Drive connector is down or a script fails, still deliver the pass on
the pages you have, and note what bookkeeping is owed.

Before running, resolve any **blocking clarification** — a question the pass can't safely proceed
without: which piece/ledger this is (if ambiguous), steered vs blind subagent (if he asked for a
subagent and it's unclear which), or the piece's state (if unclear). These are separate from, and
come before, the pass's single **editorial ask** at the end.

1. **Load state.** Locate and read the piece's room ledger (head blocks + relevant rulings, per
   above). Note what is settled/parked and which decisions are locked.
2. **Intake the pages (rule 9, best-effort), then read only the designated pages.** If the pages are
   a fresh batch not yet snapshotted and the tools are available: read the live Google Doc via the
   Drive connector → snapshot verbatim to `manuscripts/` → MD5 + word count into
   `tracker/word-count-log.md` → run the checker (report-only, never surfaced mid-draft). If he
   handed a chat paste, the batch is already snapshotted, or the connector is unavailable, use what
   you have and log the count if you can. Read the designated pages verbatim. **Intent (rule 11): he
   states the scene's intent before handing pages.** If he did, grade the page against it. If he
   didn't, asking for it is the pass's editorial ONE ask — do NOT infer an intent and grade against
   your guess.
3. **Write the pass** in the format below.
4. **Append** it to the ledger. Determine the next Pass number by reading the ledger's highest
   existing `## Pass N` **immediately before appending** (never trust a number observed earlier) and
   append as `## Pass <N+1> — <pages> (<date>)`. Never overwrite or duplicate an earlier pass; the
   ledger is append-only. (Manuscript snapshots are also immutable — a frozen first draft stays
   frozen and new/revised pages are snapshotted as NEW files beside it, never over it.)
5. **Commit + push** if the project workflow authorizes it (rule 9: commit + push each session), then
   give him the pass in chat — verdict first, editorial ONE ask last. A commit/push failure does not
   invalidate the pass already delivered.

## Two subagent modes — keep them distinct
- **(a) Steered second read** — a subagent room pass, e.g. when he says "run it through a Fable
  review agent." Spawn an Agent (`model: fable` unless he says otherwise) and hand it: the designated
  pages verbatim, the book context to review on-target (spine, the characters in the scene, what
  these pages ARE), and the DO-NOT-RE-LITIGATE list from the ledger. Give it the rule-5 register
  instruction in its brief (blunt, no cushions), and ask it for exactly the pass format below. This
  is NOT blind — do not call it blind. Relay its report (his rules apply to the relay), then log it
  as the pass.
- **(b) Rule-8 blind independent review** — a genuine outside check, **author-initiated** (run it
  when he asks for a blind/independent read, not automatically). The operative property of "blind" is
  not "fresh context" (which isn't a real guarantee) but this, which is testable: **the reviewer must
  not see the main-room pass, the ledger rulings, the protect-list, the continuity notes, or any
  `reports/`/`docs/` content before it produces its own read.** Give it a different model, only the
  pages + the rule-5 register instruction, and nothing that leaks the room's conclusions or the
  project's prior rulings. Then **reconcile**: where its read and the main-room read AGREE = the
  signal; splits go to the author. It does not replace the main pass — it is checked against it.
- If which mode he wants is ambiguous, resolve it as a blocking clarification before running either.

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
PRIORITY-<k> (OPTIONAL — include when the pass has many findings and he'd benefit from a shortlist):
   the k highest-leverage moves, ordered.
```
Mandatory sections: HARDEST FIRST, the ranked findings, SPINE/THEME PRESSURE-TEST, the audit, and
WORKS-PROTECT. PRIORITY-k is optional. Keep it ranked and specific. Quote his actual sentences. No
essay, no cushions.

## After the pass
The room does not open a revision. When the draft is DONE and he moves a book into revision, the
room's logged findings become the D2 target list; grammar/POV/mechanics then run under
`revision-pass`. Do not start a revision plan from a room pass while the book is still DRAFTING.
