# games/bazaar/ — The Bazaar item lookup (local, no web)

Opened 2026-09-27 (gaming session). His ask: "can you find them in the game files instead of
parsing Mobalytics?" — yes for TEXT, no for ART. Same rules as `../snap/README.md`: sources or
silence; code written by a Sonnet subagent from a spec, code only; the main session reviews and
runs it; nothing from Claude's memory of the game.

## What it does
`py -X utf8 games/bazaar/tools/item_lookup.py --name "Apothecary"` → hero · size · starting
tier · tags · per-tier cooldown and numbers · tooltip text with the numbers filled in
(`Regen 6 > 12 > 18`) · every enchantment's text. All from the game's own data on this PC.

Other flags: `--hero Mak`, `--size Large`, `--tag Weapon`, `--text regen` (filters AND together),
`--keyword Charge` (the game's keyword glossary), `--list-heroes`, `--raw` (dump the item's
JSON), `--json` (machine output), `--cards PATH` / `--tooltips PATH` (override the source).
Read-only: it never writes anywhere, and it opens the database in read-only, lock-free mode so
it is safe while the game is running.

## Where the data lives (surveyed 2026-09-27, read-only)
- The game is installed through the **Tempo Launcher**, not Steam:
  `%APPDATA%\Tempo Launcher - Beta\game\buildx64\` (Unity 6000.3, Addressables).
- **Live item data = `%USERPROFILE%\AppData\LocalLow\Tempo Storm\The Bazaar\prod\cache\GameData.db`**
  (SQLite; table `cards`, one JSON blob per record; 1,408 items on 09-27). The game re-syncs
  it from Tempo's server on launch. **The tool reads this.**
- `prod\cache\cards.json` beside it is a STALE leftover (dated 2026-04-10; Apothecary still
  had the pre-patch text). The first version of the tool read it and was wrong — caught in
  review because the numbers disagreed with Mobalytics. Never use it unless asked.
- `GameData.db.zip` is the last download. If it is newer than the `.db`, the tool prints a
  WARNING — the numbers may lag the latest patch. When that warning shows and a number matters,
  he reads it in game.
- Keyword glossary (Charge, Haste, etc.) = the `tooltips` table in the same database.

## Art — NOT built, on purpose
Item images are compressed Unity texture bundles behind an Addressables catalog, streamed from
Tempo's CDN and only partly cached on the PC (`LocalLow\Unity\Tempo Storm_The Bazaar\`, 4.6 GB,
hash-named). Getting pixels out needs a Unity asset library plus a reverse-engineered catalog
parser, and coverage would still be partial. Not worth it. **For pictures: the Mobalytics item
database in the browser pane** (`mobalytics.gg/the-bazaar/database/items-and-enchantments`; the
lower of its two search boxes is the live one). **Never open bazaardb.gg — it crashes the app.**

## The loop now
He names or describes an item → the tool gives hero/size/tier numbers/text from his own files
→ Mobalytics only when a picture is needed to confirm an ID. Debriefs stay post-run only.

## Known gaps (tool author's own list, verified by the main session 2026-09-27)
- A few placeholders stay raw when the value depends on the player's runtime state (e.g.
  Farmer's Market's `{aura.1}` sell-value line; the Pyg's Gym family). Printed untouched, never
  guessed.
- Time values are stored in milliseconds in the data; the tool converts the known time
  attributes to seconds. One deliberate outlier in the data: Yetarian Club's 99-second freeze.
- A placeholder hero `Hero8` exists in the data (187 items) — unreleased content; ignore.

## Verified 2026-09-27
Apothecary (Mak, Large, 5 s, Regen/Burn/Poison 6 > 12 > 18, "When you Haste, Slow or Freeze,
Charge this 1 second(s)", Shielded/Mossy text) = identical to the Mobalytics page the same
afternoon. Outlands Terror (Karnok, Large, 200 > 400 > 800 Damage, "Cooldown reduced by 3
seconds" while Enraged) renders correctly. Missing file → exit 2; bad schema → exit 3.
