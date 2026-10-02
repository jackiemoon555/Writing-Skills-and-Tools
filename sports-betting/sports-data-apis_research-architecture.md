# Sports Data Sourcing & Scraping Architecture

## 1. Data Source Matrix & Feasibility

| Data Provider | Official API Access | Estimated Cost | Feasibility / Best Workaround |
| :--- | :--- | :--- | :--- |
| **Underdog Fantasy** | Prohibited (ToS) | N/A | **Claude Desktop Local Browser Scrape.** Uses local residential IP & logged-in session to bypass Cloudflare. |
| **Pro Football Reference** | None | Free / $8/mo (Stathead) | **`nflfastR` Python Package.** Free open-source play-by-play, EPA, and roster data back to 1999. |
| **PFF (Pro Football Focus)** | Enterprise B2B Only | ~$200/yr (Consumer) | **Manual CSV Export.** Export PFF Premium Stats 2.0 tables directly into Gemini's 1M+ context window. |
| **NFL Next Gen Stats** | Enterprise (Sportradar) | $5,000–$20,000+/yr | **`nflreadr` Python Package.** Pulls public Next Gen Stats (separation, time-to-throw, speed) for free. |

---

## 2. Risk & Compliance Analysis: Direct Scraping vs. APIs

### Scraping Legality vs. ToS Enforcement
* **Federal Law (*hiQ v. LinkedIn*):** Scraping publicly available data (unauthenticated lines, public statistics) is legal under U.S. law and does not violate the Computer Fraud and Abuse Act (CFAA).
* **Platform Terms of Service (ToS):** Scraping behind an account login wall (e.g., your personal Underdog account) violates platform agreements. 
* **Account Enforcement Risks:** Running automated headless Python scripts against logged-in sports betting accounts carries a high risk of IP blacklisting, account flagging, or account termination.

### Scraping Architecture Comparison

```
+-----------------------------------------------------------------------+
|                         OPTION 1: LOCAL BROWSER                       |
|  [Underdog Account] <---> [Residential IP] <---> [Claude Desktop]    |
|  * Lowest risk of bans. Bypasses Cloudflare using real human session. |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
|                       OPTION 2: OPEN SOURCE DATA                      |
|  [nflverse / nflfastR] ---> [Clean Parquet/CSV] ---> [Gemini Pro]     |
|  * 100% legal, zero anti-bot risk, free official play-by-play data.    |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
|                    OPTION 3: AUTOMATED SCRIPT (LOGGED IN)             |
|  [Python Script] ---> [Datacenter IP] ---> [Cloudflare Block/Ban]     |
|  * HIGH RISK. Triggers anti-bot detection; risks account termination. |
+-----------------------------------------------------------------------+
```

---

## 3. Free Open-Source Setup (`nflverse` / Python)

To bypass expensive enterprise sports data subscriptions ($10,000+/year), use the `nflverse` library in Python to pull official NFL play-by-play, Expected Points Added (EPA), and Next Gen Stats directly into clean files for Gemini.

### Installation
```bash
pip install pandas nfl_data_py
```

### Data Retrieval Script
```python
import nfl_data_py as nfl
import pandas as pd

# Load 2024/2025 play-by-play data with EPA metrics
pbp_data = nfl.import_pbp_data([2024])

# Load Next Gen Stats (Passing, Rushing, Receiving)
ngs_passing = nfl.import_ngs_data(stat_type='passing', years=[2024])

# Load Weekly Roster and Injury Statuses
weekly_data = nfl.import_weekly_data([2024])

# Filter and save to CSV for Gemini intake
pbp_data[['game_id', 'home_team', 'away_team', 'posteam', 'epa', 'success']].to_csv('nfl_epa_summary.csv', index=False)
ngs_passing.to_csv('ngs_passing_summary.csv', index=False)

print("Data exported successfully for Gemini Pro context load.")
```

---

## 4. Recommended Multi-Model Pipeline

1. **Extraction:**
   * Run the `nflverse` Python script for raw statistical baselines and EPA data.
   * Use **Claude Desktop** locally to grab live Underdog props/lines from your logged-in browser session.
2. **Analysis (Gemini Pro):**
   * Upload raw `nflverse` CSVs, PFF exported sheets, and injury reports directly into **Gemini Pro**.
   * Run qualitative web searches to verify travel schedules, weather, and coach interviews.
3. **Execution (Claude Max):**
   * Feed Gemini's condensed 300-word qualitative summary into **Claude Max**.
   * Make final strategic bet sizing and market mismatch evaluations without burning token limits.