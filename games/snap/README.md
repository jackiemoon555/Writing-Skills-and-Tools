# games/snap/ — Marvel Snap weekly report + collection tracker

Opened 2026-09-19. Approved plan: `C:\Users\alec_\.claude\plans\hold-on-i-want-scalable-acorn.md`
(summary below). Standing file for his Snap state: `../marvel-snap.md` — read that first.

## What this does
- **Every Wednesday 9:00am** (the morning after Snap's Tuesday patches) a scheduled Claude run
  writes `reports/YYYY-MM-DD.md`: what changed in the patch · the top ranked decks with cube
  average and win rate · **decks he can build right now** · **decks one or two cards away** ·
  how his current decks stand. Ladder only, no draft. He can also just say "snap report."
- It knows what he owns by reading ONE file the PC version of Snap writes:
  `%USERPROFILE%\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod\CollectionState.json`.
  Only a derived card list is ever saved here. Raw game files are never copied or committed.

## The one thing Alec does
He plays on his phone, so the PC copy only learns about new cards when it's opened.
**Open Snap on the PC for a minute before Wednesday.** Every report prints how old the
collection file is, so a stale one is obvious.

## Rules for any session or scheduled run working here
- **Sources or silence.** Every card, deck, and stat comes from that run's fetched pages, with the
  link and date. Never from Claude's memory of the game — it's stale.
- A source that fails to load is reported as FAILED. Gaps are never filled in.
- Summarize; never copy articles. No advice to spend money.
- Unmatched card names are LISTED, never guessed. Fixes go in `name_overrides.json`.
- Pull first. Commit only `games/snap/` and `games/marvel-snap.md`. If the pull can't
  fast-forward or the tree has other changes, write the files and skip the commit.
- **Code here is written by a Sonnet/Haiku subagent from a written spec, code only. The main
  session writes no code** (author, 2026-09-19).

## Sources that worked when tested (2026-09-19)
- Patch notes (official): `https://marvelsnap.com/patch-notes-<month>-<day>-<year>/`
- Card win rates + sample size: `https://snap.fan/cards/tier-list/`
- Ranked decks, full lists, cube average, win rate: Marvel Snap Zone's weekly "Ranked Meta Tier
  List" article, found from `https://marvelsnapzone.com/tier-list/`
- Known NOT to load: `snap.untapped.gg` draft pages (script-rendered). Draft is out of scope.

## Build status
- [x] 1. (2026-09-19) Alec installs Snap from Steam on this PC, logs into his phone's account, opens it once
- [x] 2. (2026-09-19) Inspect the real layout of CollectionState.json (read-only) and write the spec from it
- [x] 3. (2026-09-19; reader verified; ALEC CONFIRMED: the Zombie deck list read from the file is his, and he does NOT own Ultron — matches the file. In-app card counter not located; spot-check accepted instead) Sonnet subagent writes `tools/read_collection.py` (code only); main session runs it;
        card count checked against the number the game shows
- [~] 4. (2026-09-19; report written: reports/2026-09-19.md; his used/noise feedback pending) First report built by hand in-session; he says what was useful and what was noise
- [x] 5. (2026-09-19) **ON DEMAND ONLY — his final call: "don't worry about a weekly check in, I'll call for it manually around patch notes."** The scheduled task `snap-weekly-report` exists but is PAUSED (disabled); its one test run stalled on a first-run permission prompt and was stopped. Its saved prompt (`C:SERSLEC_.CLAUDESCHEDULED-TASKSSNAP-WEEKLY-REPORTSKILL.MD`) IS THE RECIPE FOR A MANUAL RUN
- [ ] 6. Cross-vendor review brief for the script offered (rule 8; not a gate)

## Step 1 notes — cross-platform carry-over (checked 2026-09-19; sources are older articles, verify in-game)
- Snap HAS cross-progression: one account, same collection and rank on phone and Steam, once the
  account is LINKED (Settings cog → Link Account).
- **iPhone caveat:** players have reported that an Apple-ID-only account can't sign in on Steam.
  Safest order: on the PHONE first, link the account to a **Google** login; THEN install on the
  PC and sign in with that same Google login.
- **Don't play on the PC before signing in** — launching fresh can start a brand-new guest
  account, and then the collection file would describe the wrong account. The check: the rank
  and card count on the PC match the phone.
- Signing in is Alec's step. Claude never enters credentials.

## Verified file layout (inspected 2026-09-19, read-only; the reader depends on exactly this)
`CollectionState.json` is ~660 KB and starts with a UTF-8 byte-order mark. Under `ServerState`:
- `CardOwnership.Dao.S[]` — one row per OWNED card: `C` (card id), `B` (base owned), `V` (variant
  indexes). **This is the source of truth.** 123 rows on 2026-09-19.
- `Cards[]` — his card COPIES (variants included). Used only as a cross-check; its distinct ids
  matched the ownership table exactly (123 / 123, zero differences).
- `Decks[]` — 17 saved decks, each with `Name` and its own `Cards[]`. **Trap:** the first
  seventeen `"Cards"` arrays in the file belong to decks, not the collection.
- `CardDefStats.Stats{}` — ~555 cards he has SEEN. **Not ownership.** Never use it for that.
- Several saved decks are team-up/precon lists holding cards he does NOT own; the reader reports
  those under each deck's `missing`.
The reader exits 3 and writes nothing if any of these paths move, so a game update that changes
the layout fails loudly instead of producing a wrong collection.

## How the reader was built (his rule, 2026-09-19)
Main session wrote the SPEC from the verified layout; a **Sonnet subagent wrote the code, code
only** (one file, no git, no docs, never ran it on his data); main session reviewed it (no
network imports, two writes only, no account fields), ran it, and checked: 123 cards · 17 decks ·
integrity OK · byte-identical on re-run · exit 2 on a missing file · no id strings in the output.

## Lessons from the first hand-built report (2026-09-19) — for the scheduled run's prompt
- The fetch summarizer MISLABELED a change (called Blink 5/8 → 5/7 a "buff"). **Always report the
  numbers and judge buff/nerf from them, never from a label.**
- Name mismatches are real: the game says `DrDoom`/`MrFantastic`/`MrNegative`/`MrSinister`/`Ronan`;
  sites spell them out. Fixed in `name_overrides.json`. After matching, ALWAYS scan the "missing"
  list against his ids for near-matches before calling a card unowned.
- Base cards and their variant-named cards are DIFFERENT cards (`JaneFoster` ≠ "Jane Foster
  Fractured Frontier"). Never merge them.
- Deck matching was done with a throwaway shell loop. For the weekly run it should be a second
  small script (`tools/match_decks.py`: decks in, owned/missing out) — **to be written by a
  Sonnet/Haiku subagent from a spec, code only**, same as the reader.
- The most useful single finding was cross-deck card frequency ("which unowned cards gate the
  meta"). Keep that section.
- **Rules interactions: never from Claude's memory either.** 2026-09-19: Claude believed
  Jubilee-added cards don't trigger On Reveal; Alec said they do; the source agreed with Alec.
  When he states a rule from play, check it, and expect him to be right.
- Local game files contain NO card text (verified). Text always comes from the sites.

## Local card TEXT — found (2026-09-19, Sonnet subagent, read-only dig; corrects the note above)
The install is in his SECOND Steam library: `D:\SteamLibrary\steamapps\common\MARVEL SNAP`
(8.7 GB). English card ability text IS there:
`SNAP_Data/StreamingAssets/aa/StandaloneWindows64/localization-string-tables-english(en)_assets_all.bundle`
(~249 KB, a UnityFS container whose text block is stored uncompressed). Plain tools pull out
whole sentences but only in fragments — stray length bytes break some lines — so a complete
card-text lookup would need a small careful parser (NO download required). Also readable:
`SNAP_Data/StreamingAssets/aa/catalog.bin` (47 MB) lists every card's internal name — a full
card roster. NOT BUILT. If wanted, it is a Saturday job for a Sonnet/Haiku subagent from a spec
(code only). Until then, card text comes from the sites. Earlier line saying "local files
contain NO card text" was true only of the AppData state folder.

## Tools (both Sonnet-written from specs, code only; main session reviewed and ran them)
- `tools/read_collection.py` — his owned cards + saved decks → `collection.json` / `collection.md`.
- `tools/match_decks.py DECKS.json` — ranked decks vs. his collection → Markdown: table, buildable,
  closest, most-common unowned cards, possible spelling mismatches. Verified 2026-09-19 against a
  hand-match of 15 decks: identical results; byte-identical on re-run; exit 2 on a missing file.
- **Always run them as `py -X utf8 …`** on this PC — without the flag, dashes and dots in the
  output come out garbled.
- Weekly deck inputs are kept as `reports/decks-YYYY-MM-DD.json`.
- `tools/read_card_text.py` (Sonnet-written, 2026-09-19) — unpacks the game's English string
  table from the local install (pure-Python LZ4; no downloads) → 13,039 strings, written to
  `local/card_text.json` (**gitignored — the game's text is never committed**). Verified: exact
  current ability wording comes out (e.g. "On Reveal: Add the top card of your deck to this
  location."). **KNOWN GAP: the file has no key names, so text can't be matched to a CARD NAME.**
  Use it to search by wording: `py -X utf8 games/snap/tools/read_card_text.py --lookup "last card you played"`.
  Linking names to text needs the key table / card definitions from another bundle — not found yet.
- `tools/card_lookup.py` (Sonnet-written, 2026-09-19, second dig) — **card NAME → exact current
  ability text, from his own install, no network.** Found the real link (never a guess): key
  names live in `…/localization-assets-shared_assets_assets/data/localization/tables/card/cardshareddata.asset.bundle`
  (`Card_Name_<Key>` / `Card_Desc_<Key>` → int64 ids) and the same ids sit beside each English
  string in the string-table bundle. 756 cards linked, 1 unresolved (Husk). Verified against five
  cards fetched from the web the same night: identical text.
  Use: `py -X utf8 games/snap/tools/card_lookup.py --name "Wong"`. Output → `local/card_lookup.json`
  (gitignored). **Gaps:** cost and power are NOT in these files (reported as null — get numbers
  from the sites); some texts keep placeholders like `{card.AddedPower}`.
  **Bonus:** each entry's `key` is the game's own card id (`MrNegative`) beside its display name
  ("Mister Negative") — an authoritative id→name map that could replace the hand-kept
  `name_overrides.json`. Not wired in yet.
- **For "what does this card do" questions: use card_lookup first, the web only for cost/power
  and for anything the lookup can't resolve.** Saves fetches.

## HOW A REPORT HAPPENS NOW (final, 2026-09-19): he asks for it
No schedule. When he says **"snap report"** (usually right after patch notes), the session:
1. pulls the repo, runs `py -X utf8 games/snap/tools/read_collection.py` (and reminds him to open
   Snap on the PC first if the collection file is more than a week old);
2. hands the fetching to ONE Sonnet subagent (patch notes, balance update, the newest ranked
   tier-list article saved as `reports/decks-YYYY-MM-DD.json`, card win rates) — main session
   orchestrates, writes no code, does no bulk reading;
3. runs `py -X utf8 games/snap/tools/match_decks.py reports/decks-YYYY-MM-DD.json`;
4. answers card-text questions from `tools/card_lookup.py` first, the web only for cost/power;
5. writes `reports/YYYY-MM-DD.md` (verdict first line, action last), updates
   `../marvel-snap.md`, commits only `games/`.
Do NOT re-enable the schedule or suggest one unless he asks.
- **COST + POWER are now local too (his idea, 2026-09-19): "if the numbers don't change until
  patch notes, fill the gaps once so there's no need to look every time."** `card_stats.json`
  (553 released cards, one bulk request to Marvel Snap Zone's card endpoint; Sonnet-gathered,
  nothing from memory) is merged into `card_lookup.py` by exact normalized name. Passed the
  freshness test (Blink 5/7 after the 09-10 nerf) and a nine-card spot check.
  **REFRESH RULE: numbers change ONLY on patch notes and on the smaller balance updates — so
  re-gather `card_stats.json` whenever he calls a "snap report" (that run already reads both),
  and never otherwise.** A broken or missing stats file never breaks text lookup.
- So `py -X utf8 games/snap/tools/card_lookup.py --name "Blink"` now answers the WHOLE question
  (name · cost · power · exact text) from his PC with no web fetch. Known leftovers: some texts
  keep a `{card.…}` placeholder where a number goes.
- Lookup quirks seen 2026-09-19: **Rogue** returns a flavor quote instead of her ability (her
  `Card_Desc` id points at the wrong string, or her real text lives under another key) — verify
  Rogue on the web. Keyword DEFINITIONS (Quickdraw, Empowered, Judge) were not found by simple
  search of the string table; do not explain those keywords from memory.
