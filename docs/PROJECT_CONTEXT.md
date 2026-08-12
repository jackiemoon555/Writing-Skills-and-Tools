# Project Context — Handoff for a New Session

**Upload this file at the start of a new Claude session to get fully caught up.**
Last updated: 2026-08-11

---

## Who I am & the big-picture goal

I'm writing **novels and novellas** and self-publishing them on **Amazon KDP**
(Kindle Direct Publishing). My philosophy:

- **Not focused on profit or virality.** The goal is to consistently *ship*
  products and improve with each project. Getting reps in is the strategy.
- Money along the way is a **bonus**. The ultimate goal is that, with enough
  books / a big enough backlist, I can **transition out of my day job**.
- Each book compounds — the body of work is the engine, not any single title.
- **Production cadence — aspirational standard (set 2026-08-12): ~one
  novella/novel per month.** A north star to aim at, **not a hard quota** — missing
  it in a given month is fine; it just sets the bar. **Genre-agnostic** — write what
  I feel and blend it into a story (as I'm doing with *The Fighter*). "Stephen King
  it" — high volume, write daily, don't wait on inspiration or lock to a genre.
  (Daily target: 2,000/day now → 5,000/day; note King's own quota is ~2,000/day.)

## Hard rule for Claude: **no prose writing**

I write **all my own prose.** Claude must **never write or rewrite my fiction.**
Claude's job is to **analyze, check, critique, organize, and assist** — flag
things and explain why, and I decide what to change. Feedback, not ghost-writing.

## My working preferences

- **Do tasks one at a time, sequentially** — no parallel/batched agents.
- **Be mindful of usage limits** — don't run expensive background fan-outs.
- **Moving away from Notion** (not a fan).

## My daily workflow

1. Write in **Reedsy** (works at home and at my work computer — not blocked there).
2. End of day: **export a `.docx` from Reedsy.**
3. Copy it into **Google Docs** — this is my **source of truth / cross-device backup.**
4. Share the `.docx` (or point Claude to the Google Doc) → Claude runs the
   self-editing passes and returns a report + updates my word tracker.

Reedsy also handles **EPUB / print-PDF export for free**, which likely covers most
of the KDP formatting stage.

---

## The repo (everything lives here)

- **GitHub:** https://github.com/jackiemoon555/Writing-Skills-and-Tools (private)
- **Working branch:** `claude/new-project-repository-ceesk0`
- **Open draft PR:** #1 — https://github.com/jackiemoon555/Writing-Skills-and-Tools/pull/1

### What's built: a self-editing toolkit (Python)

Reads `.txt` / `.md` / `.docx` (built-in docx reader, no dependency) and reports:
- **Spelling** with a **custom dictionary** (invented names aren't flagged)
- **Echoes** (overused distinctive words)
- **Filter words** (saw, felt, noticed…)
- **Filler words** (very, just, really, suddenly…)
- **Adverbs** (-ly)
- Output as **Markdown or HTML reports** (chapter/line/context for each flag)

Run it:
```bash
pip install -e ".[dev]"        # includes pyspellchecker
writing-tools manuscript.docx --dictionary dictionaries/the-fighter.txt --report review.html
writing-tools chapter.md --list-unknown     # find candidate custom-dictionary words
```
33 tests pass. Everything analyzes/reports only — never rewrites prose.

### Key files
- `src/writing_tools/` — the toolkit (loaders, spelling, style, report, cli…)
- `dictionaries/the-fighter.txt` — whitelist of intentional names/dialect for the
  current project
- `tracker/word-count-log.md` — the daily word-count tracker (see below)
- `reports/` — generated review reports

---

## Current project: *The Champ* (novella)

*Working title **The Champ** (chosen 2026-08-12); formerly **The Fighter**. Same
book — the `.docx` files are still named `the-fighter`.*

- **Genre/voice:** first-person, present-tense, boxing/MMA. Punchy, short sentences.
- **Goal:** ~30,000 words (soft target).
- **Status as of 2026-08-12: 5,841 words (~19.5%).**
- **Heartbeat motif:** "Thump. Thump." repeats intentionally (~47×) — that's on
  purpose, not an echo to fix.

### Outstanding items on the manuscript
- **3 real typos to fix:** `enroute` → "en route", `inbetween` → "in between",
  `mosied` → "moseyed".
- Style items to *consider* (not required): trim some of `like` (×28), `just`
  (×18), `still` (×19), `that` (×40); a few filter-word swaps for immediacy.

### Revision ideas (scenes to add)
- **Add press-conference scenes to a couple of the early chapters** to show more
  of Chuck's bravado. Two of them:
  1. **In the past — before the title fight** (the first fight, vs the Russian
     champ that opens Ch1 and is lost in Ch2). A flashback press conference.
  2. **Before the second fight** (vs Rodriguez, Ch8–9). Note: the current draft
     already *references* this presser in passing — "the slick talking,
     well-tailored man that was at the press conference" (Ch9) — so this scene
     would dramatize a moment the book currently only alludes to.
  - Purpose: showcase Chuck's arrogance/showmanship (the "bravado" the UFC "loved"
    him for, per Ch7) on the page, before the losses hollow it out — sharpening the
    contrast with the broken man he becomes.
  - Noted 2026-08-11.
- **Physicalize Chuck's emotional damage (post-first-draft).** Add more scenes where
  an emotional blow lands as a literal strike — a truth as a punch, a loss as a kick,
  shame as a body shot. The draft already does this once: "The truth coming across as
  a punch to the liver" + grabbing his ribs (Ch10). Extend the device across the book
  so his inner life is rendered in fight-language. Noted 2026-08-12.
- **Nicole interlude — flesh her out (in progress 2026-08-12).** Give Nicole her own
  POV interlude so she's understood, not a villain and not "woman as scenery."
  Directly answers the Test Audience flag that women readers are the book's neglected
  audience (Nicole currently has no interiority). Author's intent: humanize her,
  give understanding to her choices.

### Open structural decisions (undecided — for later)
- **Interlude POV scope.** *Interlude 1* is John / "Johnny Law", third-person past,
  ending on **"Was it worth it?"** OPEN QUESTION: keep the interludes focused
  **solely on John**, or **expand them into a recurring device** across other
  successful characters (e.g. **Rob**) who each slowly realize the cost of their
  success. The unifying thread is that same "was it worth it?" question — the
  interludes would become a *chorus on the price of winning*, counterpointing
  Chuck's first-person collapse. Decide as the story shakes out. Noted 2026-08-11.
  **Update 2026-08-12: leaning toward expanding** — a Nicole interlude is planned,
  widening the interludes beyond John.

## Word-count tracker (rules)

- **Daily minimum: 750 words.**
- Tracked in `tracker/word-count-log.md`: date, words written that day, cumulative
  total, and whether the 750 goal was met.
- Daily words = new manuscript total − previous total.
- **Cumulative baseline: 4,012 words on 2026-08-11.**

---

## Frozen backlog (to resume)

**Research (paused; do sequentially, economically):**
1. Open-source pipeline tools — already found: prose linters (proselint, Vale,
   LanguageTool, write-good, textlint), novel writers (novelWriter, Manuskript),
   formatting (Pandoc + pandoc-novel, Sigil, Calibre). *(Reedsy may cover
   formatting.)*
2. **Amazon KDP mechanics** — royalties (35% vs 70%), KDP Select/Kindle Unlimited
   exclusivity, ISBN, pricing, trim sizes. **← resume research here.**
3. Articles / academics / accomplished writers using **Claude Code** and how (found
   dedicated fiction-writing Claude Code skills; some sources were proxy-blocked).

**Marketing (deferred — after the first draft):** nail down a *marketing approach*
+ *budget*. Keep it **low/no-cost and sustainable** (back-matter "also by" page,
mailing list, KDP keywords/categories, cross-promo) — no big spend, profit isn't
the near-term aim. Claude helps with research/analysis; I write the copy.

**Feature backlog for the toolkit:**
- Dialogue-punctuation checker (fiction-specific)
- Continuity / style-sheet tracker (catch "Katherine" vs "Catherine" drift)
- Readability metrics (Flesch–Kincaid), sentence-rhythm graphs
- Passive-voice / run-on detection
- Per-chapter dashboards
- EPUB / KDP-prep validation

---

## Available MCP integrations (this account)

github, Google Drive, Google Docs (via Drive), Gmail, Google Calendar. *(Also
present but not relevant: FMP, Indeed, Kiwi, Clinical Trials, Economic Index.
Notion is being phased out.)*

## Suggested next steps

1. Fix the 3 typos in *The Fighter*.
2. Keep writing toward 30k (750+/day); share each day's `.docx` for a report +
   tracker update.
3. When ready, resume the KDP-mechanics research.
4. After the first draft: editor prep, then formatting, then KDP, then marketing.
