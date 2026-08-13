"""Grammar and mechanics helpers.

These are intentionally small, dependency-free starting points. As the project
grows, richer checks (spell-checking, part-of-speech tagging, etc.) can be layered
on top of this module.
"""

from __future__ import annotations

import re

_WORD_RE = re.compile(r"\b[\w']+\b")
_SENTENCE_RE = re.compile(r"[.!?]+")


def word_count(text: str) -> int:
    """Return the number of words in ``text``."""
    return len(_WORD_RE.findall(text))


def sentence_count(text: str) -> int:
    """Return the number of sentences in ``text``.

    Sentences are approximated by counting runs of terminal punctuation
    (``.``, ``!``, ``?``) that are followed by other content.
    """
    stripped = text.strip()
    if not stripped:
        return 0
    sentences = [s for s in _SENTENCE_RE.split(stripped) if s.strip()]
    return len(sentences)


def average_sentence_length(text: str) -> float:
    """Return the average number of words per sentence (0.0 if no sentences)."""
    sentences = sentence_count(text)
    if sentences == 0:
        return 0.0
    return round(word_count(text) / sentences, 2)


def find_double_spaces(text: str) -> list[int]:
    """Return the start indices of any run of two or more spaces."""
    return [m.start() for m in re.finditer(r" {2,}", text)]


def find_uncapitalized_sentences(text: str) -> list[str]:
    """Return sentences that do not begin with a capital letter."""
    offenders: list[str] = []
    for raw in re.split(r"(?<=[.!?])\s+", text.strip()):
        sentence = raw.strip()
        if sentence and sentence[0].isalpha() and not sentence[0].isupper():
            offenders.append(sentence)
    return offenders
