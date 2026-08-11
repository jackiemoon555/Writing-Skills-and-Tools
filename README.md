# Writing-Skills-and-Tools

Connecting tools and skills for writing — grammar, literary elements, style, and more.

The goal of this project is to bring together a collection of composable Python
utilities that help analyze and improve writing: checking grammar, surfacing
literary elements (metaphor, alliteration, etc.), measuring readability, and
tying these skills together behind a simple, consistent interface.

## Status

Early scaffold. The modules below are starting points meant to grow.

## Layout

```
Writing-Skills-and-Tools/
├── src/
│   └── writing_tools/
│       ├── __init__.py       # package entry point
│       ├── grammar.py        # grammar / mechanics helpers
│       └── literary.py       # literary-element detection
├── tests/
│   └── test_grammar.py
├── pyproject.toml
└── README.md
```

## Getting started

```bash
# create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# install the package in editable mode with dev tools
pip install -e ".[dev]"

# run the tests
pytest
```

## Usage

```python
from writing_tools import grammar, literary

text = "The wild wind whipped the waves. It was as loud as thunder."

print(grammar.word_count(text))          # -> 12
print(grammar.sentence_count(text))      # -> 2
print(literary.find_alliteration(text))  # -> [['wild', 'wind', 'whipped']]
print(literary.find_similes(text))       # -> ['as loud as thunder']
```

## Roadmap

- [ ] Grammar / mechanics checks (spacing, capitalization, common errors)
- [ ] Readability metrics (Flesch–Kincaid, etc.)
- [ ] Literary-element detection (metaphor, simile, alliteration, personification)
- [ ] Style suggestions (passive voice, weak words, sentence variety)
- [ ] A unified `analyze()` entry point that runs the full toolkit

## License

MIT — see [LICENSE](LICENSE).
