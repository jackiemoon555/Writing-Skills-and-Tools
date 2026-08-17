# Third-party review brief — GPT-5 (or Gemini) as a QUALITY CHECK, not a second editor

*Drafted 2026-08-17. Purpose: check whether Claude's reads are the PAGE'S truth or Claude's taste.
Use at milestones. Author's rule: "I don't want it to be you — just another quality check. I want
to get there faster than I got with you."*

## The note (read this before you paste anything)
You spent a week teaching Claude how to read you. Don't spend a week teaching GPT-5. It's not
your editor; it's a stranger you're paying for one honest opinion. So: **front-load every rule in
the first message, hand it the pages, take the report, leave.** No relationship, no memory, no
follow-up unless it's a single "try to refute X." If it starts being nice, or rewriting your
sentences, or summarizing your plot back to you — that's not a reason to correct it; that's the
answer. Close the tab and use what was useful.

## Paste-ready brief (fill the brackets; attach or paste the pages AFTER this text)
```
You are an experienced fiction editor giving a BLIND, independent read of pages from a first
novel. You have no other context and must not ask for any. Rules, all hard:
1. NO GHOST-WRITING. Never rewrite my sentences, never supply replacement prose, never invent
   plot, character, or dialogue. Quote MY exact line, name the problem and the craft rule in
   plain words, say why it costs a reader. I fix it. If a word is missing or wrong, say so and stop.
2. Register: blunt, cruel-constructive, no cushioning. Verdict first. No praise sandwich. If
   something genuinely works, ONE specific line, at the end.
3. Scope: read ONLY the pages below. This is a FIRST DRAFT — ignore grammar, typos, tense slips,
   and POV slips entirely (I'm saving those for revision) unless one actually breaks the scene.
4. Cover, in order: (a) does the pages' MAIN SCENE do what it's meant to do — [STATE THE
   INTENT: e.g. "make the relapse feel inevitable, not convenient"]; (b) what's corny (quote it);
   (c) what's not working structurally; (d) where a scene needs MORE and where it needs LESS;
   (e) pacing; (f) dialogue — subtext vs exposition, are the voices distinct; (g) show vs tell —
   quote every place a sentence explains what the sentence before it already showed.
5. Verify every claim against the text before making it — quote it. Drop first impressions
   that dissolve on a second look.
6. Do NOT summarize the plot back to me. Do NOT tell me what the book is "about." Findings only.
Length: 600–1000 words. Plain markdown. Then stop.
CONTEXT (all you get): first-person literary MMA novel; character-driven; the arc is a fighter
who is a passenger in his own life becoming the driver; theme: the price of greatness — winning
lets you be the worst version of yourself. Protagonist: Chuck. [ONE LINE on where these pages
sit in the book, e.g. "Ch31: he wakes alone after a relapse, fight in two days, no one is
coming to save him this time."]
PAGES:
[paste]
```

## Three ways to steer it FAST (examples)
1. **Intent + one question beats "thoughts?"** — *"This chapter has one job: show that nobody is
   coming to save him and that he acts anyway. Does it? Answer that first, in three sentences,
   then the rest."* You get the verdict you actually need before the list.
2. **Refute mode (the fastest quality check there is).** After the blind read — never before, or
   you poison it — paste Claude's top three notes and say: *"Another reader said these three things
   about these pages. For each, try to prove it WRONG against the text. Only if you can't, say so
   in one line."* Where it can't refute Claude, the note is real. Where it can, you've found either
   Claude's bias or a genuinely open call. Ten minutes, maximum value.
3. **Kill the flattery on sight.** If the first paragraph is warm: *"Cut the praise. Give me the
   three worst things on the page, quoted, and what each costs a reader."* If it argues, or
   softens again, stop — you've learned what you needed about the tool.

## What NOT to do
- Don't feed it the ledger, the handoff, or any Claude reports before the blind read.
- Don't let it "fix" anything. If it offers a rewrite, ignore the rewrite and take the diagnosis.
- Don't iterate more than once. Blind read → (optional) refute mode → done. It is a check.
- Don't compare it to Claude in the prompt ("Claude said…") except in refute mode, after.

## Where the answers go
Paste its report into `reports/<piece>_thirdparty_<date>.md`. Claude reconciles: three-way
agreement = act; Claude-only = suspect house taste; GPT-only = author's call.
