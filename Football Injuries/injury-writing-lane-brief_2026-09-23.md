# Writing lane brief: injury analysis backed by the medical literature

Written 2026-09-23 for Alec's writing pipeline. Status: idea, not started. Everything here comes from one day of trial runs (three pieces produced, listed below) and Alec's read of the market. Nothing has been published or tested with readers.

## The idea in one paragraph
Sports injury commentary for the betting/fantasy audience is mostly (a) a credentialed person's opinion from video, or (b) a proprietary time-lost database. What is rare is a structured piece that, for one injury or one player, lays out the possible routes, cites the peer-reviewed evidence on every line, and ends with an explicit list of what the literature does NOT establish. The structure is the product: it is honest, repeatable without a medical license, and it reads differently from a hot take.

## What already exists (from memory, NOT verified - check before citing any of this)
People working the injury-analysis lane: David Chao (ProFootballDoc), Jesse Morse, Edwin Porras (Fantasy Points), Deepak Chona (SportsMedAnalytics), Will Carroll (Under the Knife), Jeff Stotts (In Street Clothes; injury database), Stephania Bell (ESPN). Mostly doctors/PTs; mostly opinion or database, rarely citation-per-line with a stated-gaps section. Before pursuing: read a month of each and confirm whether the structured, cited format really is absent. "I haven't come across it" is the current basis.

## The format (the three samples follow it)
1. Header: what the piece covers; a standing disclaimer that literature describes populations and says nothing about a specific player's severity.
2. Numbered sections, each a question a bettor actually asks (timeline, recurrence, performance after return, what practice tags mean, mechanism, gaps).
3. Every factual bullet ends with a citation: first author, journal, year, PMID or DOI. News gets outlet + date + URL, quoted not paraphrased.
4. "NOT FOUND in searched literature" written where the answer is empty. An honest empty section is a finding.
5. Closing section, always: (a) documented facts, (b) what the literature says about the injury type in general, (c) what nobody has established.
6. References list; one line on how the search was done (queries, results screened).
7. Body length 1,200-1,800 words.

## Samples produced 2026-09-23 (in this project)
- `research/injury_types/hamstring.md` - injury-type sheet. 29 PubMed sources. Headline: NFL mean 2.4 wks lost, 33% re-injure, recent strain RR 4.8, about half of returning pros show suppressed high-speed running; no NFL production study exists; injury-report tags map to nothing clinical.
- `research/injury_types/elbow_dislocation.md` - injury-type sheet with a "playing through it" focus. 23 sources. Headline: NFL median 19-23 days, 76% return same season, mechanism is arm-out landing; NOTHING published on off-arm injury and throwing, on performance while playing through it, or per-hit re-injury odds. The empty sections are the point.
- `research/case_studies/cooper_kupp.md` - player case study. Dated injury timeline 2022-2025 with quotes, season lines cross-checked on three stat pages, literature per injury type, three-list closing. The one record observation: targets fell 191 -> 70 while yards per catch did not; nobody has separated injury from age from scheme.
Three citations per sheet were spot-checked against PubMed by the orchestrator and matched.

## Method (repeatable)
- Literature: PubMed (indexes every sports-medicine journal that matters) via the PubMed MCP tools; Consensus as a second pass for "what does the literature say" questions; open-access full text via journal page when abstracts lack the number. Google Scholar (manual) for grey literature. NFL Health & Safety releases for league-level counts.
- Reporting: team sites, NFL.com, ESPN, beat writers; quote with date and URL. Pro-Football-Reference and footballdb block automated fetches (HTTP 403); use ESPN/NFL.com stat pages and cross-check.
- Data: nflverse via `pull_data.py` for snaps, targets, per-game lines, injury-report practice status (2025 has `injuries.parquet` with practice status; note the "resting player" code).
- Worker pattern: one Sonnet subagent per piece with the questions fixed in advance; orchestrator verifies 3+ PMIDs directly before accepting. Cost per piece so far: roughly 200-280K subagent tokens, 6-9 minutes.

## Guardrails (non-negotiable if this is published)
- No diagnosis of a named player beyond what the team reported. The literature is about populations; the player's grade/severity is UNKNOWN unless stated by the team.
- No probabilities invented from the literature ("60% to play"). Report the study's rate and its population; stop there.
- Not medical advice; say so.
- Sample sizes stated every time (Chang's NFL elbow series is 62 injuries; Whiteley is 15 players).
- Where a source is from memory, label it and verify before publication.
- Never reproduce large passages of a paper; quote briefly with attribution, and always include the DOI link.

## Backlog of pieces that would follow naturally
- Injury-type sheets for what shows up on a weekly board: concussion return-to-play (Murray this week), oblique (Penix, Tua), MCL (Dart), AC joint, turf toe, Lisfranc, ACL year-two performance, Achilles return (position-specific).
- "Playing through it" series: what the literature says about competing injured, by injury type, with the empty sections shown.
- Case studies in the Kupp format: players whose careers turned on an injury or on playing through one; the targets-vs-yards-per-catch observation is a reusable lens (did usage change or did the player).
- A standing explainer: why injury-report tags (Q/D/limited/DNP) carry no clinical information (Jenkins 2024 gives the NFL distribution: 38% DNP / 33% limited / 28% full).

## Open questions before committing
- Audience and channel (newsletter, site, thread format?) - UNKNOWN.
- Credibility without a clinical credential: the citation-per-line format is the answer, but whether readers accept it is untested.
- Cadence: injury-type sheets are evergreen; player pieces are timely and expire. The mix matters.
- Whether the "what nobody has established" section sells or bores. It is the honest part; it is also the least exciting.
- Legal review of naming players alongside injury literature, before anything goes public.

## Tie-in to the betting project
Reads that come from a sheet go into `reads_log.csv` with the sheet as the basis and get graded like any other read. After a few weeks that will show whether literature-based reads hit at a different rate than scheme/usage reads. If they do not add anything, that is worth knowing before writing about it.
