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
- [ ] 5. Scheduled task `snap-weekly-report` created and test-run once
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
