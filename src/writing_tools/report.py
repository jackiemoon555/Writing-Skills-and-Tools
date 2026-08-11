"""Turn a list of :class:`Finding` objects into a readable report.

Two formats are supported: Markdown (great for reading in an editor or on GitHub)
and a self-contained HTML page (nice for skimming in a browser). Neither format
changes your manuscript; a report is just a checklist you work through.
"""

from __future__ import annotations

import html
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from .findings import Finding

# Friendly names + display order for the categories the passes produce.
CATEGORY_LABELS = {
    "spelling": "Spelling",
    "echo": "Echoes (repeated words)",
    "filter-word": "Filter words",
    "filler-word": "Filler words",
    "adverb": "Adverbs (-ly)",
    "grammar": "Grammar & mechanics",
}


def summarize(findings: Iterable[Finding]) -> Counter:
    """Return a Counter of findings per category."""
    return Counter(f.category for f in findings)


def _group_by_category(findings: Iterable[Finding]) -> dict[str, list[Finding]]:
    grouped: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        grouped[finding.category].append(finding)
    return grouped


def _ordered_categories(grouped: dict[str, list[Finding]]) -> list[str]:
    known = [c for c in CATEGORY_LABELS if c in grouped]
    extra = [c for c in grouped if c not in CATEGORY_LABELS]
    return known + sorted(extra)


def to_markdown(findings: list[Finding], *, title: str = "Manuscript review") -> str:
    """Render findings as a Markdown report."""
    grouped = _group_by_category(findings)
    counts = summarize(findings)

    lines = [f"# {title}", ""]
    if not findings:
        lines.append("No issues flagged. ✅")
        return "\n".join(lines) + "\n"

    lines.append(f"**{len(findings)} items flagged** across {len(grouped)} categories.")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("| --- | ---: |")
    for category in _ordered_categories(grouped):
        label = CATEGORY_LABELS.get(category, category)
        lines.append(f"| {label} | {counts[category]} |")
    lines.append("")

    for category in _ordered_categories(grouped):
        label = CATEGORY_LABELS.get(category, category)
        items = grouped[category]
        lines.append(f"## {label} ({len(items)})")
        lines.append("")
        for f in items:
            loc = f.location() or "—"
            detail = f.message
            if f.suggestion:
                detail += f" — {f.suggestion}"
            lines.append(f"- **{loc}** · {detail}")
            if f.context:
                lines.append(f"  > {f.context}")
        lines.append("")

    return "\n".join(lines) + "\n"


_HTML_STYLE = """
:root { color-scheme: light dark; }
body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem auto;
       max-width: 900px; padding: 0 1rem; line-height: 1.5; }
h1 { border-bottom: 2px solid #8884; padding-bottom: .3rem; }
table { border-collapse: collapse; margin: 1rem 0; }
th, td { border: 1px solid #8884; padding: .3rem .7rem; text-align: left; }
td.num { text-align: right; }
.finding { margin: .4rem 0; padding: .4rem .6rem; border-left: 3px solid #8886;
           background: #8881; border-radius: 3px; }
.loc { font-family: ui-monospace, monospace; font-size: .85em; opacity: .8; }
.context { font-style: italic; opacity: .8; margin-top: .2rem; }
.suggestion { opacity: .9; }
""".strip()


def to_html(findings: list[Finding], *, title: str = "Manuscript review") -> str:
    """Render findings as a self-contained HTML page."""
    grouped = _group_by_category(findings)
    counts = summarize(findings)
    esc = html.escape

    parts = [
        "<!doctype html>",
        '<html lang="en"><head><meta charset="utf-8">',
        f"<title>{esc(title)}</title>",
        f"<style>{_HTML_STYLE}</style>",
        "</head><body>",
        f"<h1>{esc(title)}</h1>",
    ]

    if not findings:
        parts.append("<p>No issues flagged. ✅</p></body></html>")
        return "\n".join(parts)

    parts.append(
        f"<p><strong>{len(findings)} items flagged</strong> "
        f"across {len(grouped)} categories.</p>"
    )
    parts.append("<table><tr><th>Category</th><th>Count</th></tr>")
    for category in _ordered_categories(grouped):
        label = CATEGORY_LABELS.get(category, category)
        parts.append(f'<tr><td>{esc(label)}</td><td class="num">{counts[category]}</td></tr>')
    parts.append("</table>")

    for category in _ordered_categories(grouped):
        label = CATEGORY_LABELS.get(category, category)
        items = grouped[category]
        parts.append(f"<h2>{esc(label)} ({len(items)})</h2>")
        for f in items:
            loc = esc(f.location() or "—")
            block = [f'<div class="finding"><span class="loc">{loc}</span> — {esc(f.message)}']
            if f.suggestion:
                block.append(f'<span class="suggestion"> ({esc(f.suggestion)})</span>')
            if f.context:
                block.append(f'<div class="context">{esc(f.context)}</div>')
            block.append("</div>")
            parts.append("".join(block))

    parts.append("</body></html>")
    return "\n".join(parts)


def write_report(
    findings: list[Finding], path: str | Path, *, title: str = "Manuscript review"
) -> Path:
    """Write a report to ``path``; format is chosen from the file extension."""
    path = Path(path)
    if path.suffix.lower() in {".html", ".htm"}:
        content = to_html(findings, title=title)
    else:
        content = to_markdown(findings, title=title)
    path.write_text(content, encoding="utf-8")
    return path
