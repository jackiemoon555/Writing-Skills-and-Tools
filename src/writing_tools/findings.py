"""Shared data types and text helpers used across the analysis passes.

Every analysis pass (spelling, style, grammar, ...) reports its results as a list
of :class:`Finding` objects. Keeping a single shared shape means the report
writer never has to know which pass produced a finding.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterator

# A "word" for our purposes: letters, apostrophes and hyphens inside the token.
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*")


@dataclass(frozen=True)
class Finding:
    """A single flagged item for the writer to review.

    Nothing here changes the manuscript; a finding only points at something and
    explains why it was flagged. The writer decides what (if anything) to do.
    """

    category: str  # e.g. "spelling", "echo", "filter-word"
    message: str  # human-readable description of what was flagged
    line: int = 0  # 1-based line number (0 = not line-specific)
    column: int = 0  # 1-based column number (0 = not column-specific)
    context: str = ""  # a short snippet of surrounding text
    suggestion: str = ""  # optional hint (never an automatic rewrite)
    severity: str = "info"  # "info" | "suggestion" | "warning"
    source: str = ""  # which file/chapter this came from

    def location(self) -> str:
        """Return a compact ``file:line:col`` style location string."""
        parts = []
        if self.source:
            parts.append(self.source)
        if self.line:
            parts.append(str(self.line))
            if self.column:
                parts.append(str(self.column))
        return ":".join(parts)


@dataclass
class WordToken:
    """A word plus where it sits in the source text."""

    text: str
    start: int  # character offset into the source string
    line: int  # 1-based
    column: int  # 1-based


@dataclass
class LineIndex:
    """Maps character offsets in a string to (line, column) positions."""

    text: str
    _line_starts: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        starts = [0]
        for i, ch in enumerate(self.text):
            if ch == "\n":
                starts.append(i + 1)
        self._line_starts = starts

    def position(self, offset: int) -> tuple[int, int]:
        """Return the 1-based (line, column) for a character ``offset``."""
        # Binary search for the last line start <= offset.
        lo, hi = 0, len(self._line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self._line_starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        line = lo + 1
        column = offset - self._line_starts[lo] + 1
        return line, column

    def line_text(self, line: int) -> str:
        """Return the text of a 1-based ``line`` (without the trailing newline)."""
        if line < 1 or line > len(self._line_starts):
            return ""
        start = self._line_starts[line - 1]
        end = self.text.find("\n", start)
        if end == -1:
            end = len(self.text)
        return self.text[start:end]


def iter_words(text: str) -> Iterator[WordToken]:
    """Yield every word in ``text`` with its offset, line and column."""
    index = LineIndex(text)
    for match in _WORD_RE.finditer(text):
        line, column = index.position(match.start())
        yield WordToken(text=match.group(0), start=match.start(), line=line, column=column)


def normalize_word(word: str) -> str:
    """Lower-case a word and normalize curly apostrophes for comparison."""
    return word.lower().replace("’", "'")


def snippet(text: str, offset: int, width: int = 40) -> str:
    """Return a one-line snippet of ``text`` centered on ``offset``."""
    start = max(0, offset - width)
    end = min(len(text), offset + width)
    fragment = text[start:end].replace("\n", " ").strip()
    prefix = "…" if start > 0 else ""
    suffix = "…" if end < len(text) else ""
    return f"{prefix}{fragment}{suffix}"
