"""Spell checking with a custom dictionary.

Novels are full of words no general dictionary knows — invented character and
place names, coined terms, deliberate misspellings in dialogue. The whole point
of a *custom dictionary* is that you add those words once and they stop being
flagged, so the real typos stand out.

Backends, tried in order:

1. ``pyspellchecker`` (if installed) — a pure-Python checker that ships its own
   word-frequency data and can offer correction suggestions. ``pip install
   pyspellchecker`` to enable it.
2. A word-list file (one word per line), e.g. the system dictionary at
   ``/usr/share/dict/words`` when present.

Whichever backend is used, the custom dictionary is always layered on top: any
word you add there is treated as correctly spelled.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .findings import Finding, iter_words, normalize_word, snippet

DEFAULT_WORDLIST_PATHS = [
    Path("/usr/share/dict/words"),
    Path("/usr/dict/words"),
]


def load_custom_dictionary(path: str | Path) -> set[str]:
    """Load a custom dictionary file (one word per line; ``#`` comments allowed)."""
    path = Path(path)
    words: set[str] = set()
    if not path.exists():
        return words
    for raw in path.read_text(encoding="utf-8").splitlines():
        word = raw.strip()
        if word and not word.startswith("#"):
            words.add(normalize_word(word))
    return words


def _load_wordlist_file() -> set[str] | None:
    for candidate in DEFAULT_WORDLIST_PATHS:
        if candidate.exists():
            words = set()
            for raw in candidate.read_text(encoding="utf-8", errors="ignore").splitlines():
                word = raw.strip()
                if word:
                    words.add(normalize_word(word))
            return words
    return None


class SpellChecker:
    """Flags words not found in a dictionary or the custom word list.

    Parameters
    ----------
    custom_words:
        Words to always treat as correct (e.g. character names).
    known_words:
        An explicit set of correctly-spelled words. If given, this is the
        dictionary used (handy for tests and offline use). If omitted, a backend
        is auto-selected.
    min_length:
        Words shorter than this are never flagged (avoids noise from initials).
    """

    def __init__(
        self,
        custom_words: Iterable[str] = (),
        *,
        known_words: Iterable[str] | None = None,
        min_length: int = 3,
    ) -> None:
        self.custom = {normalize_word(w) for w in custom_words}
        self.min_length = min_length
        self._backend = None  # a pyspellchecker instance, if available
        self._known: set[str] | None = None

        if known_words is not None:
            self._known = {normalize_word(w) for w in known_words}
            return

        # Try pyspellchecker first for real suggestions.
        try:  # pragma: no cover - depends on optional install
            from spellchecker import SpellChecker as _PySpell

            self._backend = _PySpell()
        except Exception:  # pragma: no cover - falls through to wordlist
            self._backend = None
            self._known = _load_wordlist_file()

    @property
    def backend_name(self) -> str:
        if self._backend is not None:
            return "pyspellchecker"
        if self._known is not None:
            return "wordlist"
        return "none"

    def is_available(self) -> bool:
        """Return ``True`` if some dictionary backend is usable."""
        return self._backend is not None or self._known is not None

    def add_words(self, words: Iterable[str]) -> None:
        """Add more words to the custom dictionary at runtime."""
        self.custom.update(normalize_word(w) for w in words)

    def _is_known(self, word: str) -> bool:
        if word in self.custom:
            return True
        if self._backend is not None:  # pragma: no cover - optional backend
            return word in self._backend
        if self._known is not None:
            return word in self._known
        return True  # no backend: don't flag anything

    def _suggest(self, word: str) -> str:
        if self._backend is not None:  # pragma: no cover - optional backend
            correction = self._backend.correction(word)
            if correction and correction != word:
                return correction
        return ""

    def check(self, text: str, *, source: str = "") -> list[Finding]:
        """Return a :class:`Finding` for every word not found in the dictionary."""
        if not self.is_available():
            return []

        findings: list[Finding] = []
        seen_unknown: dict[str, int] = {}
        for token in iter_words(text):
            word = normalize_word(token.text)
            # Skip short words, numbers-with-letters, and all-caps acronyms.
            core = word.strip("'-")
            if len(core) < self.min_length:
                continue
            if token.text.isupper() and len(token.text) <= 5:
                continue
            if self._is_known(core):
                continue

            seen_unknown[core] = seen_unknown.get(core, 0) + 1
            suggestion = self._suggest(core)
            findings.append(
                Finding(
                    category="spelling",
                    message=f"'{token.text}' is not in the dictionary",
                    line=token.line,
                    column=token.column,
                    context=snippet(text, token.start),
                    suggestion=(f"did you mean '{suggestion}'?" if suggestion else ""),
                    severity="warning",
                    source=source,
                )
            )
        return findings

    def unknown_word_summary(self, text: str) -> dict[str, int]:
        """Return unknown words mapped to how many times each appears.

        Useful for building up a custom dictionary: eyeball the list, then move the
        real names into your custom dictionary file.
        """
        counts: dict[str, int] = {}
        for finding in self.check(text):
            word = finding.message.split("'")[1]
            key = normalize_word(word).strip("'-")
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
