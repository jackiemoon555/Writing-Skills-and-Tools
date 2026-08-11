"""Command-line entry point: analyze a manuscript and write a report.

Examples
--------
Analyze one chapter and write an HTML report::

    python -m writing_tools chapter-01.docx --report review.html

Analyze a folder of chapters with a custom dictionary::

    python -m writing_tools manuscript/ --dictionary names.txt --report review.md

List the unknown words in a file (to help build your custom dictionary)::

    python -m writing_tools chapter-01.md --list-unknown
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .findings import Finding
from .loaders import iter_manuscript_files, load_document
from .report import summarize, write_report
from .spelling import SpellChecker, load_custom_dictionary
from .style import run_style_passes

PASS_CHOICES = ["spelling", "style", "all"]


def _gather_paths(target: Path) -> list[Path]:
    if target.is_dir():
        return iter_manuscript_files(target)
    return [target]


def analyze_path(
    target: Path,
    *,
    passes: str = "all",
    custom_words: set[str] | None = None,
) -> list[Finding]:
    """Run the requested passes over a file or folder and return all findings."""
    custom_words = custom_words or set()
    checker = None
    if passes in ("spelling", "all"):
        checker = SpellChecker(custom_words=custom_words)

    findings: list[Finding] = []
    for path in _gather_paths(target):
        doc = load_document(path)
        if checker is not None and checker.is_available():
            findings += checker.check(doc.text, source=doc.name)
        if passes in ("style", "all"):
            findings += run_style_passes(doc.text, source=doc.name)
    return findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="writing_tools",
        description="Self-editing passes for manuscripts (.txt/.md/.docx). Reports only — never rewrites.",
    )
    parser.add_argument("target", help="a manuscript file or a folder of chapters")
    parser.add_argument(
        "--passes",
        choices=PASS_CHOICES,
        default="all",
        help="which passes to run (default: all)",
    )
    parser.add_argument(
        "--dictionary",
        "-d",
        help="path to a custom dictionary file (one word per line)",
    )
    parser.add_argument(
        "--report",
        "-r",
        help="write a report to this path (.md or .html); otherwise prints a summary",
    )
    parser.add_argument(
        "--list-unknown",
        action="store_true",
        help="list unknown words with counts (helps build a custom dictionary) and exit",
    )
    parser.add_argument("--version", action="version", version=f"writing_tools {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    target = Path(args.target)
    if not target.exists():
        print(f"error: no such file or folder: {target}", file=sys.stderr)
        return 2

    custom_words: set[str] = set()
    if args.dictionary:
        custom_words = load_custom_dictionary(args.dictionary)

    if args.list_unknown:
        checker = SpellChecker(custom_words=custom_words)
        if not checker.is_available():
            print(
                "No spelling backend available. Install one with:\n"
                "    pip install pyspellchecker",
                file=sys.stderr,
            )
            return 1
        combined: dict[str, int] = {}
        for path in _gather_paths(target):
            doc = load_document(path)
            for word, count in checker.unknown_word_summary(doc.text).items():
                combined[word] = combined.get(word, 0) + count
        for word, count in sorted(combined.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"{count:>5}  {word}")
        return 0

    findings = analyze_path(target, passes=args.passes, custom_words=custom_words)

    if args.report:
        out = write_report(findings, args.report, title=f"Review: {target.name}")
        print(f"Wrote {len(findings)} findings to {out}")
    else:
        counts = summarize(findings)
        if not findings:
            print("No issues flagged. ✅")
        else:
            print(f"{len(findings)} items flagged:")
            for category, count in counts.most_common():
                print(f"  {category:>14}: {count}")
            print("\nRun with --report review.html for the full list.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
