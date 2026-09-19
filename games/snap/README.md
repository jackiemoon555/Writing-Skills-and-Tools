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
- [ ] 1. Alec installs Snap from Steam on this PC, logs into his phone's account, opens it once
- [ ] 2. Inspect the real layout of CollectionState.json (read-only) and write the spec from it
- [ ] 3. Sonnet subagent writes `tools/read_collection.py` (code only); main session runs it;
        card count checked against the number the game shows
- [ ] 4. First report built by hand in-session; he says what was useful and what was noise
- [ ] 5. Scheduled task `snap-weekly-report` created and test-run once
- [ ] 6. Cross-vendor review brief for the script offered (rule 8; not a gate)
