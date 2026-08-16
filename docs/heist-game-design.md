# Heist Game — Design Ledger (working)

**Project:** untitled text-first mobile heist game, set in the Five Families world
(the untitled fantasy trilogy's setting — see `docs/memory/project_fantasy_trilogy.md`).
Vault entry: `docs/game-ideas.md`. Design session logged 2026-08-16.

**STATUS: VAULT / DESIGN-ON-PAPER ONLY.** No development until the book pipeline allows.

---

## North stars / comps

- **Darkest Dungeon** (author-named primary inspiration): roster management, classes,
  psychological cost as a mechanic, base upgrades, a final mission everything builds to.
- **GTA V / GTA Online heists:** setup jobs feed the main job.
- **Text-first lane (production reality):** 80 Days / Sorcery! / A Dark Room / Reigns —
  writing IS the production value; 1–2 person teams shipped these; tooling = Ink/Twine-class.
  Rule of the lane: text games live on SYSTEMS responding to play, not story with buttons.

## Core loop (DECIDED: option 2 — run of jobs + crew management)

Plan → pick crew → run setup jobs → execute the main job → fallout/recovery → repeat,
under an overarching story that ends in ONE FINAL JOB.

## The three meters (DECIDED — each answers a different audience)

- **Preparedness — the TARGET.** Job-specific: how much do we know/control going in?
  Earned through SETUP JOBS, not bought off a menu (GTA insight): schematics stolen,
  servants bribed, security lured out and destroyed. Every point of prep has fiction
  attached = every point of prep is a scene (text-first advantage).
- **Heat — the STATE (cops).** In-job + short-term: procedural, impersonal escalation
  ladder (local PD → state → the Agency as the endgame response no one wants). Cools
  with time and bribes. Heat is RULES.
- **Notoriety — the WORLD reacting to you.** Campaign-level, PER-FAMILY not global.
  Works like a REVIEW SYSTEM (author's framing): higher rating → better contracts,
  better fences, elite recruits. Fame is the reward AND the poison (Jack Moon thesis:
  make the player WANT it — the flashy job over the smart one). Two faces that rise
  together: legend in the underworld (opportunity) + infamy with the families (hunted).

**Free tension:** prep costs time; time is how heat cools and notoriety festers. The
careful play and the fast play are both wrong sometimes (DD's "managed disaster" ethos).

## The legality fork (DECIDED — the world-native rule)

Every target has a **public face and a secret face**. Police respond ONLY when the
robbed thing was legal/public. Hit a family's illegal operation or secret and there is
NO heat — they can't report what officially doesn't exist — but the family responds
personally and privately: **enforcers, vendetta, better security**. Cops = arrest;
enforcers = you disappear. Players learn to fear silence: a loud public job can be
SAFER than a quiet one the family noticed.

**Third loot type — SECRETS** (beyond money/relics): sellable, spendable to suppress a
vendetta, or held as blackmail. Endgame currency = what you know about the families.

## Windows (DECIDED — promoted to core system)

Setup jobs open **time-limited world states**. Example (author's): lure out a target's
security force and destroy it → the target is naked NOW, hardened LATER. The window
creates the campaign clock and the signature agony: the door is open but the setup
crew is bloody, stressed, and hot. Send them back in? Send the B-team? Let it close?

## Classes (DECIDED — loud/stealth specialist split)

Each class splits into **two specialists: one for loud missions, one for stealth**.
Author's example: warrior class → a fighter (loud) vs. a distraction specialist
(stealth-support). The two wings form a RELAY TEAM: the loud wing opens windows the
stealth wing walks through; setup jobs exhaust one wing so main jobs rotate to the
other — roster depth becomes necessary organically (DD rest/stress cycle).

- Craft rule: the stealth specialist is never "the worse one" — excellent at a
  DIFFERENT VERB (the one who can empty a garrison is a virtuoso/performer, not a
  lesser warrior). Every class must be someone's favorite.
- World-native class candidate: **the Branded** — disowned scion of a family; strongest
  kit in the game, but the brand is a tracker (using gifts spikes heat; that family's
  vendetta response is personal). High power, radioactive (the Abomination slot).

## Psychological meter (proposed, on-brand — name TBD: Nerve/Composure)

The DD-stress equivalent, but it's THE MASK: pressure builds mid-job; a break is
in-character (the Face's charm curdles to pathological lying, the Branded acts like
the aristocrat they swore they weren't). Between jobs, coping (drink, gambling, worse)
relieves the meter but plants campaign fallout — **the coping is the self-destruction**
(Chuck DNA). This is the mechanic that makes it a Jack Moon game, not a DD reskin.

## Failure & punishment (DECIDED: losing has real punishments)

- **Review system cuts both ways:** botched jobs tank the rating → worse contracts,
  worse fences, recruits won't sign. Economy punishment; doesn't end the run.
- **Personal losses by WHO caught them:** cops → arrested (recoverable: bail or a
  jailbreak mission = free content); enforcers → gone (the permadeath lane);
  broken/abandoned → **flipped** — they talk, and past jobs come back on you.
- **The comeback loop (lean in — it's Chuck's arc):** clawing the rating back means
  taking small humbling jobs after being the hot crew. The fall and the way back,
  as gameplay.

## Campaign spine (DECIDED)

An **overarching story ending in ONE LAST JOB** — the hardest mission in the game;
under-prepped = you lose. The final job **reads the campaign ledger**: it is shaped by
how you influenced the world — which families hate you, which secrets you hold, who
flipped or died, which windows you opened or wasted. The last mission grades your
CHOICES, not your stats.

- Craft flags: (1) telegraph readiness honestly (narrator/fence refuses to bless an
  under-prepped final job) — an earned loss is DD, an ambush loss is a refund;
  (2) author's ending signature = no clean wins — consider endings that vary by ledger
  even in VICTORY: what did it cost, who walks out. The draw-not-a-win, playable.

**Low-prep viability (DECIDED 2026-08-16):** the final job must be beatable with
minimal prep by min-maxers / tactical players. Rule: **prep buys certainty; skill pays
the markup.** NO hard gates — every prep item has an in-mission alternative that costs
live resources at a steep markup (no ward-key → the Cracker forces it at huge heat +
Nerve cost; security not burned down → a virtuoso distraction can still move them).
Prep = converting hidden information to known; a cold run is an information problem
only system-mastery can solve. Balance note: the markup must be STEEP — a cold clear
should feel like a draw won on heart (barely, bleeding, down a crew member), or prep
retroactively feels pointless. Free prestige artifact: "the cold run" as the
community's badge-of-honor challenge (DD torchless equivalent).

## Setting (DECIDED: NYC) + home base

- **NYC — already canon:** the trilogy puts the legacies through NYU and hides the
  Hall of Heirs there. The game is set in the world's CAPITAL; every district, black
  market, and undercity block invented for the game is worldbuilding the trilogy
  inherits. Map idea: districts as family territory (per-family notoriety made
  geographic).
- **Home base (DECIDED): a "dark" area of the city, upgradeable** (DD Hamlet).
  World-native meaning of dark = OUTSIDE THE FAMILIES' LIGHT — old wards, erased
  records, a block that officially doesn't exist. The base is lore, not just menus.
  Upgrade candidates: infirmary (bodies), bar/den (Nerve relief + vice fallout),
  war room (prep efficiency), workshop (gear), forger, fence's back room (contracts/
  review system). Spicy option (use sparingly): maxed vendetta sends enforcers
  LOOKING for the base.

## Open questions

1. **The story + the final target.** What is the last job, and what's the overarching
   story about? (Candidates on the table: the Hall of Heirs; taking down one family;
   the secrets-loot assembling one truth someone will kill to keep buried.)
2. **The narrator/patron (the Ancestor slot).** Who talks to the player and assembles
   the crew? A text-first game needs this voice; DD's narrator was half its identity.
3. Crew size per mission (DD's 4?).
4. Endings matrix: how many, keyed to which ledger states.
5. Engine/scope: pure interactive fiction (Ink/Twine) vs. light-UI mobile app.
6. Timeline vs. the trilogy: independent/underworld-level (no spoiler coupling) was
   flagged as safest — confirm.
7. Cross-media canon rule (from vault entry): ONE canon; the trilogy's ledger is the
   source of truth.
