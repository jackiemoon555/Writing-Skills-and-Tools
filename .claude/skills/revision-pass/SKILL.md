---
name: revision-pass
description: Teaching-mode revision protocol for Alec's (Jack Moon's) manuscripts — one lens per pass (structure → POV → line/grammar → mechanics), name the rule on HIS sentence, he fixes it, never rewrite. Use whenever he asks for a revision read, line edit, grammar pass, POV audit, structure pass, or "make it clean" on designated pages of a piece he has DECLARED in revision (currently Longshoreman Ep1–2; The Champ only after its draft is done — it is in DRAFTING).
---

# Revision Pass — teaching mode

Alec's self-named weakness is **grammar and literary structure**. The purpose of a revision pass
is to make his manuscript as clean as *he* can make it AND to make him better at the technical
side — not to hand him fixed prose. Ceiling = "no error he didn't know about."

## Non-negotiables (inherit from docs/WORKING_RULES.md — the canonical list)
- **No ghost-writing.** Never rewrite a sentence, paragraph, or line of dialogue. Quote his words,
  name the problem, name the rule, let him fix it. If he asks "how would you fix it?" — describe
  the *move* (e.g. "cut the tag and let the action beat carry it"), not the words.
- **Scoped reading.** Read ONLY the pages he designates for THIS pass. Do not re-read the whole
  manuscript, do not re-raise issues already game-planned in the room ledger.
- **One lens per pass.** Never mix. If a line-pass surfaces a structural problem, log it in ONE
  line for the structure pass and keep going.
- **He is not a coder.** Never ask him to run scripts or touch repo files. Run the toolkit
  yourself; report results in plain language.
- **Blunt, calibrated.** No flattery padding, no catastrophizing typos. High typo density is
  expected from fast drafting; never remark on the density itself.

## The four passes, in order

### 1. Structure pass (chapter / scene level)
Question for every scene: **"What does this scene DO?"** (advance plot / reveal character / turn
the emotional state / plant or pay a motif). A scene that does none → flag. Also: summary where
scene is needed (and vice versa), scene order, chapter break placement, interlude timing, whether
the chapter's last line turns the page. Output: one bullet per scene — what it does now, what it
should do, gap. Ask him the "what does it do" question before answering it where useful.

### 2. POV / voice pass
The Champ rule: **Chuck = 1st person; everyone else = 3rd person.** Flag every slip. Also flag
head-hopping, narrative distance jumps, tense wobble, and character-voice bleed (Rob/Carl/Lisa
sounding like Chuck). Output: location + the sentence + which rule.

### 3. Line / grammar pass (teaching core)
For each flag: **quote his sentence → name the rule in plain words → say why it costs the reader
→ stop.** He fixes it. Track repeat offenders; after the third instance of the same rule, say so
("this is the third dangling modifier — pattern") so it becomes a habit-fix, not a line-fix.
Priority order (Browne & King / Strunk & White vocabulary — he's reading both):
1. Filter words / narrative distance (`saw, felt, noticed, realized, watched`)
2. Telling after showing / "resist the urge to explain" (R.U.E.)
3. Dialogue mechanics: tags, beats, adverb tags, punctuation of dialogue
4. Sentence-level grammar: comma splices, dangling/misplaced modifiers, agreement, tense
5. Echoes / repeated distinctive words, filler (`very, really, just, suddenly`), -ly adverbs
6. Punctuation the reader hears: em-dash vs. comma vs. period; semicolons in fiction
Run the repo toolkit (`python -m writing_tools` on the export — spelling w/ custom dictionary,
echoes, filter, filler, adverbs) FIRST and fold its hits in; don't hand-hunt what a script finds.

### 4. Mechanics pass (last)
Typos, spelling (custom dictionary: `dictionaries/the-fighter.txt`), formatting, chapter
headings, consistent names/places (Kingsville, Miami, the nickname drop in Ch21), timeline
markers. Pure list; no discussion needed.

## Output format (every pass)
```
PASS: <structure|pov|line|mechanics>   PAGES: <what he designated>
1. [Ch/para] "<his sentence or phrase>" — <rule, plain words> — <why it costs the reader>
...
PATTERNS: <rules hit 3+ times>
PARKED FOR OTHER PASSES: <one line each>
```
Keep it a list. No essay. No praise sandwich — if something is genuinely good, ONE line at the
end, specific ("the Ch29 last line lands because…"), or nothing.

## Feed the calibration loop
After each pass, ask him which notes he used and which were noise, and log the answer in
`reports/<book>_revision-log.md` (create if missing). That log is what tunes future passes —
read it before starting any new pass on the same book.

## Reading list he's agreed to (reference, not homework to nag about)
- Browne & King, *Self-Editing for Fiction Writers* — line-level bible
- Strunk & White, *The Elements of Style* — grammar essentials
