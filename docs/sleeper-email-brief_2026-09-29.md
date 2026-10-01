# Brief — email to Sleeper about API / automated use (from the Research Tool session, 2026-09-29)

**Division of labor (Alec, 2026-09-29):** "I write and outline, you edit." Alec writes the outline and the email himself. This session edits. Confirm with him how far editing goes. This room's standing rule is to analyze and report without rewriting prose, and his hard rule is no ghostwriting. He has asked for edits on this email specifically.

## Facts to work from (verified 2026-09-29)

- **Send to:** `support@sleeper.app`. This is the address on Sleeper's [General Contact Information](https://support.sleeper.com/en/articles/8017487-general-contact-information) page. A search summary wrongly said sleeper.com, so use .app. For commercial licensing, the API docs say to "reach out to us directly."
- **The API docs** ([docs.sleeper.com](https://docs.sleeper.com/)): "a read-only HTTP API that is free to use for non-commercial purposes." "No API Token is necessary." Stay "under 1000 API calls per minute." The players file is meant to be fetched "once per day at most."
- **The Terms of Use** ([General Terms of Use](https://support.sleeper.com/en/articles/5486620-general-terms-of-use), "Last Updated: August 27, 2026"):
  - **§11.1:** you agree not to "Access, query, extract, or receive any data or content from the Services through any automated means, bot, script, spider, robot, and/or other technology ... without the express written consent of Sleeper."
  - **§11.3:** no third party may retrieve data "through any account, credential, or authentication mechanism belonging to a user" without a written agreement. "A user's provision of credentials, tokens, or authorization to a third-party does not constitute authorization from Sleeper."
  - **§2.9:** "Approved Integration Partners" have a written agreement with Sleeper. No public list was found.
- **Sleeper's only public API statement found** is a 2018 blog post: "We have opened up our API and provided detailed documentation so that 3rd party sites and developers can integrate with Sleeper..." ([blog, 2018-07-30](https://sleeper.com/blog/sleeper-fantasy-platform---season-2/)). There's no public comment on the 2026 terms.

## What Alec wants to find out (topics only; the wording is his)

- [Whether personal, non-commercial, low-volume use of the documented read-only endpoints by his own script counts as permitted, or needs written consent under §11.1]
- [Whether an AI assistant or connector reading his own league on his behalf is treated as a "third party" under §11.3, if it uses only his public username and no credentials]
- [What volume or frequency Sleeper considers acceptable, for example a daily player-status check within the docs' once-a-day guidance]
- [Whether Sleeper offers a sanctioned route, like an Approved Integration Partner program or a developer agreement]
- [Optional: his use case in a sentence, meaning his own leagues, injury tracking and read-only]

## Why it matters

A written yes would count as the "express written consent" §11.1 asks for. It would unblock a small read-only Sleeper tool on the Research Tool build list, which sits behind that project's security audit.

Full report: `D:\Claude\Research Tool\chat sessions\reports\Sleeper fantasy API and connectors.md`, with its `.verified.md`.
