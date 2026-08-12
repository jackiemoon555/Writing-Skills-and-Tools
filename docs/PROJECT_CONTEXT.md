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
- **Production cadence — HARD COMMIT (updated 2026-08-12): ≥ one novella/novel per
  month, more as the process refines.** Not slowing down until the backlist reaches
  career-viability — then reassess. (Upgraded from the earlier "aspirational, not a
  quota" framing — the author has committed.) **Genre-agnostic** — write what I feel
  and blend it into a story. "Stephen King it" — high volume, write daily, don't wait
  on inspiration or lock to a genre. (Daily target: 2,000/day now → 5,000/day; King's
  own quota ~2,000/day.) **Keep the commit sane:** the monthly bar is a *drafting*
  cadence (start/finish a draft each month); full pipeline-to-publish (revision +
  editor) may trail — measure by drafts completed, not only titles published, so the
  bar stays real and can't quietly become a failure metric.
- **Tentative 2026–27 roadmap (NOT fully committed — set 2026-08-12):** finish out 2026 with a
  **novella per remaining month** (*The Champ* is the current one; then ~one/month through
  December), then **start the first NOVEL in January 2027.** Novellas first to build reps +
  backlist + craft on shorter stakes; the novel comes once the reps make it feel small.
  Provisional — revisit as it goes. Wildcard: if *The Champ* defies the odds (viral / TV-film
  deal), all bets are off and the plan changes.

- **Production pipeline (per book):** first draft → **revision (may take a few passes)** →
  editor → publish (KDP). **Guardrail (author, 2026-08-12): the revision phase is where books
  die — do NOT let it stall, kill momentum, or let the project die there.** Bias toward
  finishing and shipping over endless polishing: "good enough to publish, improve on the next
  book" beats a perfect draft that never ships. When the draft is done, set a *bounded* revision
  plan (a fixed number of passes + a stop rule) so revision has a finish line. Matches the
  reps/backlist strategy.

- **Publishing path — DECIDED (2026-08-12): self-publish via KDP, backlist-first.** Explored
  the traditional / literary-agent / small-press routes and set them aside — too many hurdles,
  too slow, novella-unfriendly, and out of line with the high-cadence, ship-no-matter-what
  strategy. Plan: **build the backlist and let opportunity (agents, publishers, audio, film)
  come to *him*** off a proven, selling catalog — with leverage, not from a slush pile. Revisit
  trad only from a position of strength (a full novel + real sales), and only if it appeals then.
  *Claude: don't re-raise the trad/agent route unless the author asks.*
- **Publishing/marketing/editor reference:** `docs/self-pub-playbook.md` (compiled 2026-08-12;
  revisit post-revision + once an editor is found). Contains editor costs, launch plan, *The
  Champ* positioning (package as comeback/men's-fiction, NOT literary or romance), and one open
  strategic decision: **genre-agnostic vs. read-through** (a genre-agnostic catalog has ~zero
  read-through, which weakens the backlist engine — mitigations: cluster genres, pen-name lanes,
  or connected books).

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
- **Core theme (the "roots" act, Ch14+):** Coach vs Dad is deliberate — **Coach
  (the chosen "second father") left; Dad (the real one) never did.** The act is
  Chuck reconnecting with his roots: where he went wrong, how much changed, and the
  realization that the people truly there for him (Dad, and Lisa) never left — he
  just couldn't see it. Lisa voices it: "I never left you, you left me."
- **Two selves / two beginnings (deliberate):** the **Miami gym + Coach** = birth of
  **"The Chosen"** (persona/false self); **Dad's Texas gym** = birth of **Chucky
  Miles** (the real man). Both are called "where it all began" *on purpose* — one per
  self, not a continuity error.
- **No villains (authorial stance, 2026-08-12):** leaning into *"there are really no
  villains — just everyone going through something all at once."* Applies across the
  cast — Coach isn't a cruel antagonist, Nicole isn't a villain, Rob/Johnny get
  humanized via interludes. **Review implication for Claude:** support *humanizing*
  characters and finding the "what are they going through" behind each choice; never
  push toward making anyone more villainous or "louder."

### Pen name / author identity
- **All books ship under the pen name: JACK MOON.** This is the brand — consistent across the
  whole catalog, the Amazon Author Central page, and the mailing list, from *The Champ* forward
  (per Fable's "the catalog is the brand" point).
- The author is **keeping his real identity private for now** — working a day job, and wants the
  option to surprise people if he "makes it." It's a name he's carried since boyhood; those
  closest to him will know, and understand the journey.
- Practical note: pen names are also the tool for **genre lanes later** (additional names per
  genre if he ever wants to separate read-through lanes) — but Jack Moon is home base.

### Genesis / inspiration
- The idea was kicked around in different scenarios for a while before it took off. **Partly
  drawn from events in the author's own life** (the lived-experience element is likely why the
  emotional core — the fall's shame, the father, the rebuild — reads as *true* in reviews).
- Set in motion by two real fighters as archetypal poles: **Adrien Broner** (prodigious talent
  undone by ego / very public self-destruction — the "Chosen"/fall pole) and **Dustin Poirier**
  (hardscrabble roots, humility, the beloved comeback + resilience — the roots/climb-back pole).
  Chuck *starts* as Broner and has to *become* Poirier. Note: Poirier won an **interim** title
  and is a legend whose legacy was never the undisputed belt — which independently mirrors the
  book's own ending (interim belt + the draw; "it was never about the belt").
- This real-world + lived grounding, plus the author's genuine fight-world knowledge, is the
  book's **authenticity edge** — the thing a non-fighter novelist couldn't fake.

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
  2. **Two mirrored Rodriguez press conferences — same podium, two different men:**
     - **First fight (Act I): the FACADE.** Chuck performs "The Chosen" while falling
       apart inside. New chapter or fold into Ch7–8. Also makes the 45-sec blowout land
       (not just for fight fans) and shows his asshole side / the false self.
     - **Rematch (Act III): the REDEMPTION.** The rebuilt, real Chuck — written as part
       of the Act III draft.
     Together they stamp the **two selves** (The Chosen → Chucky Miles) onto the same
     setting, so the change is *shown*, not told.
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
- **Add more to Vlad early (post-first-draft).** Flesh out the champion / first
  opponent in the opening act so the eventual Vlad rematch carries real weight.
- **Add more to Chuck's asshole side (post-first-draft).** The draft doesn't yet land
  *how bad* he'd become — how he pushed everyone away (intentionally or not) before
  the crash. Show the arrogance and the damage pre-fall so the redemption is earned.
- **Prelude? (open idea).** More build-up to the first fight instead of dropping
  straight into fight night — as a **prelude BEFORE the current Ch1 intro** (keep the
  intro; author likes it). Not committed.

### Open structural decisions (undecided — for later)
- **Interlude POV scope.** *Interlude 1* is John / "Johnny Law", third-person past,
  ending on **"Was it worth it?"** OPEN QUESTION: keep the interludes focused
  **solely on John**, or **expand them into a recurring device** across other
  successful characters (e.g. **Rob**) who each slowly realize the cost of their
  success. The unifying thread is that same "was it worth it?" question — the
  interludes would become a *chorus on the price of winning*, counterpointing
  Chuck's first-person collapse. Decide as the story shakes out. Noted 2026-08-11.
  **DECIDED 2026-08-12: ensemble chorus.** Planned interlude roster —
  **John** (done, Interlude 1) → **Nicole** → **Rob** → a **final Coach** interlude.
  Each humanizes a character "going through something," so the interludes are the
  no-villains stance made structural: a human perspective on the complexity of
  relationships, counterpointing Chuck's first-person view of who wronged/left him.
  **Placement:** the final **Coach** interlude sits **immediately before the final
  chapter.**
- **Planned climax (2026-08-12):** the **final chapter is Chuck vs Johnny Law** — the
  two mirrors collide (mentor vs protégé; the man who took Nicole *and* the belt). The
  two "was it worth it?" men fight for real. The last Coach interlude is the beat that
  sets it up.
- **Act III fight ladder (decided):** **Rodriguez rematch → Vlad rematch → John
  showdown** (comeback → avenge the true-origin loss → the personal climax).
- **Ending tone (decided): hopeful / redemptive, NOT doom-and-gloom.** John & Chuck
  reconcile; most of the cast lands in a good place.
- **Climax result (decided): ambiguous / a DRAW** — winner unrevealed or drawn. It was
  never about the fight; the bout IS the reconciliation of two men who can't express
  themselves (pays off Interlude 1). Keep it subtext/action, never stated. Then an
  **epilogue** resolves the people (Lisa, Dad, Nicole, Rob, belt, sobriety) — where they
  landed, NOT what it all meant.
- **Full working outline:** `D:\Claude\the-champ_outline.md` (also backed up in the
  repo at `reports/the-champ_outline.md`).

## Word-count tracker (rules)

- **Daily minimum: 1,000 words/day** (raised from 750 on 2026-08-12; built to be hit every
  day regardless of motivation, split across two sessions — work downtime + home).
- Tracked in `tracker/word-count-log.md`: date, words written that day, cumulative
  total, and whether the 1,000 goal was met.
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
2. Keep writing toward the full draft (1,000+/day floor); share each day's `.docx` for a report +
   tracker update.
3. When ready, resume the KDP-mechanics research.
4. After the first draft: editor prep, then formatting, then KDP, then marketing.
