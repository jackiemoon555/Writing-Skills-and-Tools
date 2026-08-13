"""Load manuscript text from ``.txt``, ``.md`` and ``.docx`` files.

The ``.docx`` reader is built in (it just unzips the file and reads the paragraph
text out of the XML), so there is no third-party dependency to install. It is not
a full Word parser — it extracts readable paragraph text, which is exactly what
the analysis passes need.
"""

from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

_W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

TEXT_SUFFIXES = {".txt", ".md", ".markdown", ".text"}
DOCX_SUFFIXES = {".docx"}
SUPPORTED_SUFFIXES = TEXT_SUFFIXES | DOCX_SUFFIXES


@dataclass
class Document:
    """A loaded manuscript (or chapter)."""

    name: str  # display name, usually the file name
    text: str  # the full plain-text content
    path: Path | None = None


def _read_docx(path: Path) -> str:
    """Extract paragraph text from a ``.docx`` file without external libraries."""
    with zipfile.ZipFile(path) as zf:
        with zf.open("word/document.xml") as handle:
            tree = ElementTree.parse(handle)

    paragraphs: list[str] = []
    for para in tree.iter(f"{_W_NS}p"):
        runs = [node.text or "" for node in para.iter(f"{_W_NS}t")]
        paragraphs.append("".join(runs))
    return "\n\n".join(paragraphs)


def _strip_markdown(text: str) -> str:
    """Lightly strip Markdown syntax so prose passes don't flag markup.

    This is deliberately conservative: it removes heading markers, emphasis
    characters and inline-code backticks, but leaves the words untouched.
    """
    lines = []
    for line in text.splitlines():
        stripped = re.sub(r"^\s{0,3}#{1,6}\s+", "", line)  # headings
        stripped = re.sub(r"^\s{0,3}>\s?", "", stripped)  # block quotes
        lines.append(stripped)
    joined = "\n".join(lines)
    joined = re.sub(r"[*_]{1,3}(.+?)[*_]{1,3}", r"\1", joined)  # bold/italic
    joined = re.sub(r"`([^`]*)`", r"\1", joined)  # inline code
    return joined


def load_document(path: str | Path, *, strip_markdown: bool = True) -> Document:
    """Load a single manuscript file into a :class:`Document`.

    Raises ``FileNotFoundError`` if the file is missing and ``ValueError`` for
    unsupported file types.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No such file: {path}")

    suffix = path.suffix.lower()
    if suffix in DOCX_SUFFIXES:
        text = _read_docx(path)
    elif suffix in TEXT_SUFFIXES:
        text = path.read_text(encoding="utf-8")
        if strip_markdown and suffix in {".md", ".markdown"}:
            text = _strip_markdown(text)
    else:
        raise ValueError(
            f"Unsupported file type '{suffix}'. Supported: {sorted(SUPPORTED_SUFFIXES)}"
        )

    return Document(name=path.name, text=text, path=path)


def load_documents(paths: list[str | Path], **kwargs) -> list[Document]:
    """Load several files, skipping unsupported ones. Useful for a chapter folder."""
    documents: list[Document] = []
    for path in paths:
        p = Path(path)
        if p.suffix.lower() in SUPPORTED_SUFFIXES:
            documents.append(load_document(p, **kwargs))
    return documents


def iter_manuscript_files(folder: str | Path) -> list[Path]:
    """Return supported manuscript files in ``folder``, sorted by name."""
    folder = Path(folder)
    return sorted(
        p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES
    )
