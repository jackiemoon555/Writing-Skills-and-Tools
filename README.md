# Writing-Skills-and-Tools

A self-editing toolkit for novelists and novella writers. It connects grammar,
spelling, and literary-analysis passes so you can catch as much as possible
**before** sending your manuscript to an editor.

**Guiding principle: these tools *analyze and report* — they never write or
rewrite your prose.** Every pass flags something and explains why; you decide
what (if anything) to change. The words stay yours.

## What it does today

- **Reads your manuscript** from `.txt`, `.md`, or `.docx` (the `.docx` reader is
  built in — no extra install needed). Point it at a single chapter or a whole
  folder of chapters.
- **Spell check with a custom dictionary** — add your invented character and
  place names once and they stop being flagged, so real typos stand out.
- **Prose-tightening passes:**
  - **Echoes** — distinctive words that repeat too often
  - **Filter words** — `saw`, `felt`, `noticed`, ... that distance the reader from POV
  - **Filler words** — `very`, `really`, `just`, `suddenly`, ...
  - **Adverbs** — `-ly` words to judge whether each earns its place
- **Readable reports** — get a Markdown or HTML report listing every flag with its
  chapter, line, column, and a snippet of context.

## Install

```bash
python -m venv .venv
source .venv/bin/activate

# core toolkit + real spell checking + dev tools
pip install -e ".[dev]"

# or just the toolkit with spell checking
pip install -e ".[spell]"
```

Spell checking uses [`pyspellchecker`](https://github.com/barrust/pyspellchecker)
when installed (it also gives correction suggestions). Without it, the toolkit
falls back to a system word list if one is present, and all the other passes work
regardless.

## Quick start

```bash
# summary printed to the terminal
writing-tools examples/chapter-01.md

# full HTML report
writing-tools examples/chapter-01.md --report review.html

# a whole folder of chapters, using your custom dictionary
writing-tools manuscript/ --dictionary examples/custom_dictionary.txt --report review.md

# only run the spelling pass
writing-tools chapter-01.docx --passes spelling --report typos.md

# list unknown words (to help build your custom dictionary)
writing-tools chapter-01.md --list-unknown
```

You can also run it as a module: `python -m writing_tools ...`.

### Building your custom dictionary

1. Run `writing-tools your-chapter.md --list-unknown` to see unrecognized words
   with counts.
2. Copy the real names/terms (not the typos!) into a dictionary file — one word
   per line. See [`examples/custom_dictionary.txt`](examples/custom_dictionary.txt).
3. Pass it with `--dictionary path/to/custom_dictionary.txt` on future runs.

## Use it from Python

```python
from writing_tools.loaders import load_document
from writing_tools.style import run_style_passes
from writing_tools.spelling import SpellChecker
from writing_tools.report import write_report

doc = load_document("chapter-01.docx")

findings = run_style_passes(doc.text, source=doc.name)
findings += SpellChecker(custom_words=["Zyrelle"]).check(doc.text, source=doc.name)

write_report(findings, "review.html", title="Chapter 1 review")
```

## Project layout

```
Writing-Skills-and-Tools/
├── src/writing_tools/
│   ├── __init__.py
│   ├── cli.py          # command-line entry point (writing-tools ...)
│   ├── loaders.py      # load .txt / .md / .docx (built-in docx reader)
│   ├── findings.py     # shared Finding type + text/offset helpers
│   ├── spelling.py     # spell check + custom dictionary
│   ├── style.py        # echoes, filter words, filler words, adverbs
│   ├── grammar.py      # mechanics helpers (counts, capitalization, spacing)
│   ├── literary.py     # alliteration / simile / repetition heuristics
│   └── report.py       # Markdown + HTML reports
├── examples/
│   ├── chapter-01.md
│   └── custom_dictionary.txt
├── tests/
├── pyproject.toml
└── README.md
```

## Roadmap

A **roadmap** is just a list of planned features — a menu of what could come next.

- [x] Load `.txt` / `.md` / `.docx`
- [x] Spell check with a custom dictionary
- [x] Echoes, filter words, filler words, adverbs
- [x] Markdown + HTML reports
- [ ] Dialogue-punctuation checker (fiction-specific)
- [ ] Continuity / style-sheet tracker (catch "Katherine" vs "Catherine" drift)
- [ ] Readability metrics (Flesch–Kincaid) and sentence-rhythm graphs per scene
- [ ] Passive-voice and run-on detection
- [ ] Per-chapter dashboards for a full manuscript
- [ ] EPUB / print-prep validation for Amazon KDP

## License

MIT — see [LICENSE](LICENSE).
