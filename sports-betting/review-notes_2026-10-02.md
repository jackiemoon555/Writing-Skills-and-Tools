# Review Notes — Pipeline Docs (2026-10-02)

Claude's read of the two architecture docs in this folder. Short version first.

## TL;DR
1. **The architecture is sound.** It splits the work into free nflverse data, Gemini for heavy reading, and Claude for the final call.
2. **The verification tool checks sources, not claims.** This is the biggest gap in the research layer. See §2.
3. **Results tracking is the gap that matters most.** Without it, you can't tell whether the pipeline makes money. See §3.
4. Some of the text in the docs is out of date. That only matters if you rebuild from them. See §4.

---

## 1. What's solid
- **Free data first.** nflverse covers play-by-play, EPA, and public Next Gen Stats. Paying enterprise data prices would be the wrong move here.
- **Keeping Claude's context clean.** Feeding Claude a short verified summary instead of raw articles is the right call.
- **Having a verification step at all.** Most people don't. It catches stale, unreliable, and dead sources, which is the most obvious way this pipeline fails.

## 2. Verification tool: it checks the source, not the claim
Current behavior: it flags sources that are **dated, unreliable, or unobtainable**.

What it can miss: the source is fine, but Gemini misstated what it says. Examples:
- "Limited in practice" becomes "did not practice."
- A Wednesday injury report gets treated as Friday's.
- One beat writer's guess turns into "per reports."

All three pass a source-only check, and these are the claims most likely to move a bet.

**Cheap fix (no AI needed):**
- For any claim that would change a decision (injury status, snap share, weather, role change), have Gemini return the **exact quoted line** from the source.
- Have the tool check that the quote **appears on the page**. A plain text match is enough.
- If there's no match, flag the claim. Don't just flag the source.

## 3. Results tracking: not in either doc
Neither doc logs what happens after a bet. Without a log, you can't tell whether the pipeline finds an edge or just produces confident-sounding reads.

**Minimum log, one row per pick:**
| date | game | market/prop | line taken | closing line | stake | result | pipeline flagged anything? |

- **CLV (closing line value)** is the early signal. If you consistently beat the closing line, the edge is probably real, long before win/loss records can tell you.
- Review it after about 50–100 picks. Until then, results are mostly noise.

## 4. Doc fixes (only matters if you rebuild from these docs)
These are about the text, not your working code. If your scripts run, leave them alone.
- `nflfastR` and `nflreadr` are **R** packages, not Python. The Python options are `nfl_data_py` or `nflreadpy`. *Verify:* `nfl_data_py` may have been retired in favor of `nflreadpy`.
- `import_weekly_data` returns **weekly player stats**, not injury statuses. Injuries come from `import_injuries`.
- *Verify:* `google.generativeai` may have been replaced by the `google-genai` SDK.
- *Verify:* the `gemini-3.1-pro` model string. Check it against Google's current model list.
- "Zero Token Limits on Claude" overstates it. The pipeline **reduces** token use, it doesn't remove limits.

## 5. Legal / account risk: the doc overstates it
- **hiQ v. LinkedIn:** hiQ won on the CFAA question but **lost overall on breach of contract**. Scraping public data isn't a crime, but it can still breach a site's terms.
- **Underdog (logged in):** scraping breaks the ToS no matter what IP you use. Using your home IP lowers the chance you get **detected**. It doesn't stop Underdog from closing the account and **keeping the balance** if they catch it. Keep the balance there low.

---
*Not legal or financial advice. Items marked "Verify" weren't checked against live sources in this session.*
