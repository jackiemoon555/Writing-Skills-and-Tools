# Claude Agents — a report for a writer, not a coder

*Written 2026-08-16 for Alec / Jack Moon. Source: Claude Code docs (code.claude.com/docs/en/sub-agents) plus how agents were actually used in this repo. Plain language; no setup required from you — Claude runs all of this.*

## What an agent is, in one sentence
An **agent** (the docs call it a *subagent*) is a second Claude that the main Claude spins up to do one job in its **own separate conversation**, then hands back only the result. It does not see your chat history. It starts blank, gets a task, works, and returns a report.

Think of it as the main session hiring a contractor. The contractor gets a brief, not the whole office.

## Why that matters for you specifically
Three reasons, all of which you've already used today without calling them "agents":

1. **Blindness = honesty.** When I ran the "independent review" of Ep 1/Ep 2, and the "potential as a writer" read, those were agents. They could not see my notes, so they couldn't agree with me by accident. Where a blind reader and I land on the same page, that's signal, not echo. This is the mechanism behind your standing dual-review (Opus + Fable) — two agents, two models, no contact.
2. **Different model = different taste.** An agent can run on a different Claude model than the main session (Opus vs. Fable vs. Sonnet). Same house, different reader. It's the cheapest way to break "house taste" short of a human.
3. **Keeps your main session clean.** An agent can read a whole 16k-word manuscript, a dozen reports, and every checker file — and your conversation with me only receives the verdict. The mess stays in the contractor's office.

## What an agent can and can't do
- **Can:** read files you point it at, search the web, run the toolkit, write files if allowed, use a specific model, be told exactly which tools it may touch, be resumed later ("continue that review, now look at Ch22").
- **Can't:** see your conversation with me (unless deliberately "forked" to inherit it), remember across sessions on its own, or override the rules it's given. If I tell an agent "no ghost-writing, quote his lines, land cruel-constructive," that's the whole world it lives in.
- **Guardrails you should know exist:** each agent gets its own tool permissions (e.g. read-only), and file edits it makes still go through the same permission gates as mine.

## The three flavors you'll actually encounter
| Flavor | What it is | When it's used for you |
|---|---|---|
| **General-purpose** | A blank Claude with full tools, given a brief | Independent reads; research sweeps; "go read all four projects and tell me his range" |
| **Built-in read-only** (Explore / Plan) | Fast searchers that can't change anything | Finding where a motif appears across the manuscript; mapping the repo |
| **Custom** (a saved agent file) | A named agent with a fixed personality, tools, model — reusable | e.g. a saved "blind-reader" agent: Opus, read-only, no access to `reports/`, told to land cruel-constructive. Not built yet; easy to build |

## How this fits with skills (the other report)
- A **skill** is a *recipe* — instructions that load into whichever Claude is working (main session or an agent).
- An **agent** is a *worker* — a separate Claude that can be handed a skill.
- Your `revision-pass` protocol is a skill. When I want a *blind* run of it, I hand the skill to an agent. Recipe + worker.

## What I'd build for you (when it's worth it — not tonight)
1. **`blind-reader` agent** — Opus, read-only, forbidden from `reports/` and `docs/`, standing instructions: no ghost-writing, quote exact lines, cruel-constructive, verdict first. One word from you ("blind read Ch31–33") and it runs identically every time.
2. **`continuity-attacker` agent** — reads a designated chapter *and* the room ledger's continuity section, reports only proven contradictions with quotes from both places. The thing that caught Tone's wound.
3. Optionally, a cross-vendor read (GPT/Gemini) at milestones — that's not an agent, it's a different company; you'd paste the pages. Same purpose: break house taste.

## What you do
Nothing technical. You say "run an independent read of X" or "get a second opinion on the ending" and I choose the agent, the model, and the brief. If you ever want to see the brief I gave an agent, ask — it's plain English and it's the only thing that shapes what comes back.

## Costs, honestly
An agent read of a 16k manuscript is a real chunk of tokens (the potential-assessment agent read ~45k words of your material). Fine at milestones; wasteful for "read this paragraph." Rule of thumb: agents for whole-unit judgments, the main session for back-and-forth.
