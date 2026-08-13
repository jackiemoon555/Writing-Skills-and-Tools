"""Detection of common literary elements.

Simple, heuristic implementations meant as building blocks. They favor being
easy to read and extend over linguistic completeness.
"""

from __future__ import annotations

import re

_WORD_RE = re.compile(r"[A-Za-z']+")
_SIMILE_RE = re.compile(r"\b(?:as\s+\w+\s+as\s+[\w']+|like\s+(?:a|an|the)\s+[\w']+)\b", re.IGNORECASE)


def _first_letter(word: str) -> str:
    return word[0].lower() if word else ""


def find_alliteration(text: str, min_run: int = 2) -> list[list[str]]:
    """Return runs of consecutive words that share a starting letter.

    Only runs of at least ``min_run`` words are returned. Comparison is
    case-insensitive and ignores non-alphabetic tokens.
    """
    words = _WORD_RE.findall(text)
    runs: list[list[str]] = []
    current: list[str] = []

    for word in words:
        if current and _first_letter(word) == _first_letter(current[-1]):
            current.append(word)
        else:
            if len(current) >= min_run:
                runs.append(current)
            current = [word]

    if len(current) >= min_run:
        runs.append(current)

    return runs


def find_similes(text: str) -> list[str]:
    """Return phrases that look like similes (``as ... as ...`` or ``like a ...``)."""
    return [m.group(0) for m in _SIMILE_RE.finditer(text)]


def find_repeated_words(text: str, min_count: int = 3) -> dict[str, int]:
    """Return words appearing at least ``min_count`` times, mapped to their counts."""
    counts: dict[str, int] = {}
    for word in _WORD_RE.findall(text.lower()):
        counts[word] = counts.get(word, 0) + 1
    return {word: n for word, n in counts.items() if n >= min_count}
