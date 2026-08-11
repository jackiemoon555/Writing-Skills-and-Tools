"""Prose-tightening passes: echoes, filter words, filler words and adverbs.

These are the self-editing passes fiction writers run before sending pages to an
editor. Each one only *reports* — it points at a word and says why it might be
worth a second look. You decide whether to change anything.

Word lists are conservative defaults; pass your own to any function to tune them.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from .findings import Finding, iter_words, normalize_word, snippet

# Words so common that repetition is expected and not worth flagging.
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "at",
    "for", "with", "as", "by", "from", "into", "onto", "up", "down", "out",
    "over", "under", "is", "was", "were", "are", "am", "be", "been", "being",
    "it", "its", "he", "she", "they", "them", "his", "her", "their", "him",
    "i", "you", "we", "me", "my", "your", "our", "us", "this", "that", "these",
    "those", "there", "here", "not", "no", "so", "then", "than", "too", "s",
    "had", "has", "have", "do", "did", "does", "will", "would", "could",
    "should", "can", "may", "might", "must", "who", "what", "when", "where",
    "which", "while", "all", "any", "some", "one", "said",
}

# "Filter" words distance the reader from the point-of-view character. Fiction
# self-editing guides commonly suggest checking each use.
FILTER_WORDS = {
    "saw", "see", "seen", "watched", "noticed", "realized", "realised",
    "wondered", "thought", "felt", "feel", "knew", "heard", "seemed",
    "decided", "considered", "watched", "looked", "sounded", "appeared",
    "remembered", "imagined", "believed", "supposed", "understood",
}

# Filler / crutch words that usually add nothing.
FILLER_WORDS = {
    "very", "really", "just", "quite", "rather", "somewhat", "actually",
    "literally", "basically", "simply", "totally", "suddenly", "definitely",
    "certainly", "probably", "perhaps", "maybe", "somehow", "almost",
    "nearly", "even", "still", "only", "that", "then", "began", "started",
}


def find_echoes(
    text: str,
    *,
    min_count: int = 4,
    stopwords: Iterable[str] = STOPWORDS,
    min_length: int = 4,
    source: str = "",
) -> list[Finding]:
    """Flag distinctive words that repeat often ("echoes").

    Stopwords and very short words are ignored. Only one finding per echoed word
    (on its first appearance) is returned, with the total count in the message.
    """
    stop = {normalize_word(w) for w in stopwords}
    counts: Counter[str] = Counter()
    first_token = {}

    for token in iter_words(text):
        word = normalize_word(token.text).strip("'-")
        if len(word) < min_length or word in stop:
            continue
        counts[word] += 1
        if word not in first_token:
            first_token[word] = token

    findings: list[Finding] = []
    for word, count in counts.items():
        if count >= min_count:
            token = first_token[word]
            findings.append(
                Finding(
                    category="echo",
                    message=f"'{word}' appears {count} times",
                    line=token.line,
                    column=token.column,
                    context=snippet(text, token.start),
                    suggestion="consider varying word choice if these cluster together",
                    severity="suggestion",
                    source=source,
                )
            )
    findings.sort(key=lambda f: -int(f.message.split()[-2]))
    return findings


def _flag_wordset(
    text: str, wordset: Iterable[str], category: str, message_verb: str, source: str
) -> list[Finding]:
    targets = {normalize_word(w) for w in wordset}
    findings: list[Finding] = []
    for token in iter_words(text):
        word = normalize_word(token.text).strip("'-")
        if word in targets:
            findings.append(
                Finding(
                    category=category,
                    message=f"{message_verb}: '{token.text}'",
                    line=token.line,
                    column=token.column,
                    context=snippet(text, token.start),
                    severity="suggestion",
                    source=source,
                )
            )
    return findings


def find_filter_words(
    text: str, *, words: Iterable[str] = FILTER_WORDS, source: str = ""
) -> list[Finding]:
    """Flag filter words (saw, felt, noticed, ...) that can weaken POV immediacy."""
    return _flag_wordset(text, words, "filter-word", "filter word", source)


def find_filler_words(
    text: str, *, words: Iterable[str] = FILLER_WORDS, source: str = ""
) -> list[Finding]:
    """Flag filler / crutch words (very, really, just, suddenly, ...)."""
    return _flag_wordset(text, words, "filler-word", "filler word", source)


def find_adverbs(text: str, *, min_length: int = 5, source: str = "") -> list[Finding]:
    """Flag ``-ly`` adverbs so you can judge whether each earns its place.

    This is a heuristic: some ``-ly`` words aren't adverbs (family, reply). It errs
    toward flagging; you're the filter.
    """
    # A short allow-list of common non-adverb -ly words to cut obvious noise.
    not_adverbs = {
        "family", "reply", "supply", "apply", "rely", "ally", "belly", "bully",
        "early", "only", "ugly", "holy", "italy", "lily", "rally", "jelly",
    }
    findings: list[Finding] = []
    for token in iter_words(text):
        word = normalize_word(token.text).strip("'-")
        if len(word) >= min_length and word.endswith("ly") and word not in not_adverbs:
            findings.append(
                Finding(
                    category="adverb",
                    message=f"adverb: '{token.text}'",
                    line=token.line,
                    column=token.column,
                    context=snippet(text, token.start),
                    suggestion="a stronger verb may do the work instead",
                    severity="suggestion",
                    source=source,
                )
            )
    return findings


def run_style_passes(text: str, *, source: str = "") -> list[Finding]:
    """Run every style pass and return the combined findings."""
    findings: list[Finding] = []
    findings += find_echoes(text, source=source)
    findings += find_filter_words(text, source=source)
    findings += find_filler_words(text, source=source)
    findings += find_adverbs(text, source=source)
    return findings
