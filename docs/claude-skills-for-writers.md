# Claude Skills — a report for a writer, not a coder

*Written 2026-08-16 for Alec / Jack Moon. Source: Claude Code docs (code.claude.com/docs/en/skills) plus the skills actually installed in this repo. Plain language; you never have to write one — Claude does — but you should know what they are, because two of them are already running your editing.*

## What a skill is, in one sentence
A **skill** is a saved set of instructions — a recipe — that Claude loads when a task matches it. It lives as a small text file (`SKILL.md`) in a folder, and it can be invoked by you (`/name`) or picked up automatically by Claude when the situation fits its description.

Think of it as a laminated card on the editor's desk: *"When he hands you pages in revision, do it THIS way."* The card doesn't do the work; it makes the work consistent.

## Why it matters for you
You have a process — scoped reading, story-first mid-draft, no ghost-writing, teaching-mode grammar in revision, one lens per pass, dual review on request. Before today that process lived in prose in the handoff and in my memory. Prose gets paraphrased; memory gets lost between sessions. A skill is the process **written down as an enforceable recipe that every future session — and every agent — follows identically.** That's the difference between "Claude usually does it my way" and "it can't not."

## The two skills already running for you
| Skill | What it does | How you trigger it |
|---|---|---|
| **`revision-pass`** (built today, lives in your repo at `.claude/skills/revision-pass/`) | Teaching-mode revision: one lens per pass (structure → POV → line/grammar → mechanics); quotes *your* sentence, names the rule, you fix it; never rewrites; logs which notes landed | "Revision pass, line lens, Ep 2" — or Claude picks it up when you ask for a line edit on something in revision |
| **`novel-writing-room`** — *The Adversarial Read* (installed on your machine) | The room: adversaries hunt defects with quoted evidence, craft masters name what a fix requires, test-audience readers react; cut-never-invent; keeps a per-manuscript ledger (`*.room.md`) | "Run the room on Ch27–29" |

Both were used tonight. The room produced the Ep 1/Ep 2 findings; the revision-pass produced the teaching reports.

## What a skill is made of (so the jargon stops being fog)
- A **name** and a one-paragraph **description** — the description is what lets Claude know *when* to reach for it ("use whenever he asks for a revision read, line edit, POV audit…").
- The **body**: the actual instructions, checklists, output format, do-nots. Your revision-pass body is ~120 lines of rules you agreed to.
- Optional **supporting files** in the same folder — reference material the skill can point at (the room ships sample passages with answer keys, for instance).
- Optional switches: *only you can invoke it* (for things with side effects), *only Claude can invoke it* (background knowledge), *run it in a separate agent*, *pre-approve certain tools*.

## Where skills live — and why yours are in the repo
- **Personal** (`~/.claude/skills/`): follows *you* across every project on this machine. The room lives here.
- **Project** (`.claude/skills/` inside a repo): travels *with the repo* — anyone (or any cloud/scheduled session) that opens the repo gets it. Your revision-pass lives here on purpose: it's part of the writing project, not part of the machine.
- **Plugins**: bundles of skills published by others (e.g. the `superlearn` research plugin you looked at). Installable when a real need appears.

## Skills vs. agents vs. memory vs. the handoff — one table
| Thing | What it is | Analogy |
|---|---|---|
| **Handoff doc** | Facts + status, read at session start | The case file |
| **Memory** | Small notes about you and how to work with you | The editor's Post-its |
| **Skill** | A repeatable *procedure* | The laminated recipe card |
| **Agent** | A separate Claude worker that can be handed a skill | The contractor |

Rule of thumb from the docs, and it's right: *a fact goes in the handoff or memory; a procedure becomes a skill.* When a section of the handoff turns into "step 1, step 2, step 3," it's a skill waiting to be written.

## Skills that would be worth building for you (later, not tonight)
1. **`room-read`** wrapper — one command that runs the Adversarial Read *with your standing rules pre-loaded* (scoped pages only, mid-draft menu vs. revision menu, cruel-constructive, no re-raising ruled items). Right now I apply those by hand each time.
2. **`comp-week`** — the Friday routine: pull the Reedsy prompt, check Furious Fiction / NYC Midnight windows, surface the deadline calendar, log the entry. Procedure → skill.
3. **`manuscript-intake`** — what to do every time you hand over a `.docx`: MD5, snapshot to `manuscripts/`, word count into the log, run the checker, note chapter range. I did all of that by hand tonight; it's a checklist, therefore a skill.
4. **`submission-format`** — turn a finished piece into standard manuscript format (Shunn) `.docx` for competitions. Formatting your words, never writing them.

## What you do
Nothing. You'll notice skills as consistency: the same read shape every time, the same report format, the same rules obeyed by a fresh session that has never met you. If a skill ever does something you don't want, say so — the fix is a line in a text file, and it sticks.

## One caution
A skill is only as good as its rules, and its rules are yours. The revision-pass skill encodes *today's* agreements (grammar in revision only, cruel-constructive, hardest first). When your process changes, the skill has to change with it — otherwise it enforces yesterday. Tell me when a rule moves and I'll move the card.
