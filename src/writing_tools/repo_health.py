"""Read-only repo health check for the manuscript-tracking repo.

Six checks, one section each, PASS or FLAG:

  1. Tracker <-> snapshot files      (tracker/word-count-log.md vs manuscripts/)
  2. Tracker "Pass logged" claims    (tracker entries vs the named room ledger)
  3. Current-state head freshness    (reports/*.room.md CURRENT STATE tables vs manuscripts/)
  4. Git state                       (uncommitted changes, unmerged commits, branch divergence)
  5. Memory mirror                   (live ~/.claude memory dir vs docs/auto-memory-backup/)
  6. Handoff freshness               (SESSION_HANDOFF.md "START HERE" dates vs tracker dates)

This script NEVER writes to any file. It only reads the repo and reports. Every
FLAG names the file and the line/entry/heading that triggered it, in plain
English -- no jargon, no codes. Run with ``--json`` for a machine-readable dump.

Usage
-----
    PYTHONPATH=src py -m writing_tools.repo_health [--repo-root PATH] [--memory-dir PATH] [--json]

Exit code is 0 if every check PASSed, 1 if any check FLAGged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Editable mapping: snapshot filename prefix -> the room ledger that logs its
# passes. Used by check 2 when a tracker entry doesn't name its ledger
# directly. Verified against the repo on 2026-09-26; adjust if filenames move.
# ---------------------------------------------------------------------------
SNAPSHOT_PREFIX_TO_LEDGER = {
    "task-force-cryptid": "reports/task-force-cryptid.room.md",
    "black-market-therapist": "reports/warm-up-series.room.md",
    "the-champ": "reports/the-fighter.room.md",
    "longshoreman": "reports/longshoreman.room.md",
}

SECTION_KEY_RE = re.compile(r"_(prologue|ch\d+|interlude\d+)", re.IGNORECASE)
DATE_IN_NAME_RE = re.compile(r"_(\d{4}-\d{2}-\d{2})")
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
MD5_RE = re.compile(r"\b[0-9a-fA-F]{32}\b")
BACKTICKED_MANUSCRIPT_RE = re.compile(r"`(manuscripts/[^`]+)`")
BACKTICKED_LEDGER_RE = re.compile(r"`(reports/[^`]+\.room\.md)`")
BACKTICKED_ANY_RE = re.compile(r"`([^`]+)`")
ENTRY_START_RE = re.compile(r"^-\s+\*\*", re.MULTILINE)
PASS_LOGGED_RE = re.compile(r"Pass\s+(\d+[a-zA-Z]?)\s+logged")

SNAPSHOT_EXTENSIONS = (".txt", ".docx", ".md")
INLINE_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
MIN_SNAPSHOT_STEM_LEN = 8  # a bare filename or ellipsis suffix shorter than this is too generic to trust


def _looks_like_snapshot_name(candidate: str) -> str | None:
    """Return the matched extension if ``candidate`` looks like a real snapshot filename.

    Requires an extension we recognize, a stem of at least ``MIN_SNAPSHOT_STEM_LEN``
    characters, and a YYYY-MM-DD date somewhere in it -- so a bare mention of a file
    type (like `` `.docx` `` used generically in prose) does NOT qualify.
    """
    lower = candidate.lower()
    for ext in SNAPSHOT_EXTENSIONS:
        if lower.endswith(ext):
            stem = candidate[: -len(ext)]
            if len(stem) >= MIN_SNAPSHOT_STEM_LEN and INLINE_DATE_RE.search(stem):
                return ext
    return None


def extract_manuscript_refs(text: str, manuscripts_dir: Path | None = None) -> list[str]:
    """Return the basenames of every snapshot file backticked in ``text``.

    Three forms are recognized:
      1. A fully-qualified ``manuscripts/...`` path -- always accepted.
      2. An ellipsis shorthand (`` `…_ch2_..._2026-09-21.txt` `` or `` `..._foo.txt` ``) used
         when a file was already named in full earlier in the same bullet -- resolved by
         suffix match against ``manuscripts_dir``, and ONLY accepted if exactly one file
         in the directory ends with that suffix (an ambiguous or no-match suffix resolves
         to nothing, so it can't silently paper over a real gap).
      3. A bare backticked filename that looks like a real snapshot name -- a stem of at
         least 8 characters containing a YYYY-MM-DD date, ending in .txt/.docx/.md --
         resolved by an exact basename match against ``manuscripts_dir``. A generic
         mention like `` `.docx` `` (no stem, no date) does NOT qualify.
    Forms 2 and 3 are skipped (return nothing for that token) if ``manuscripts_dir`` isn't
    supplied or doesn't exist -- callers that care about them must pass it.
    """
    refs: list[str] = []
    available = None
    if manuscripts_dir is not None and manuscripts_dir.is_dir():
        available = [p.name for p in manuscripts_dir.glob("*") if p.is_file()]

    for raw in BACKTICKED_ANY_RE.findall(text):
        if raw.startswith("manuscripts/"):
            refs.append(Path(raw).name)
            continue

        if raw.startswith("…") or raw.startswith("..."):
            suffix = raw.lstrip("…").lstrip(".")
            if not suffix or len(suffix) < MIN_SNAPSHOT_STEM_LEN:
                continue
            if not any(suffix.lower().endswith(ext) for ext in SNAPSHOT_EXTENSIONS):
                continue
            if available is None:
                continue
            matches = [name for name in available if name.endswith(suffix)]
            if len(matches) == 1:
                refs.append(matches[0])
            continue

        if "/" in raw:
            continue  # some other kind of path (e.g. reports/...) -- not a bare snapshot filename
        if _looks_like_snapshot_name(raw) is None:
            continue
        if available is not None and raw in available:
            refs.append(raw)

    return refs


@dataclass
class Section:
    """One check's result."""

    name: str
    status: str = "PASS"  # "PASS" or "FLAG"
    flags: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)  # informational, doesn't affect status

    def flag(self, message: str) -> None:
        self.flags.append(message)
        self.status = "FLAG"

    def note(self, message: str) -> None:
        self.notes.append(message)

    def render(self) -> str:
        lines = [f"[{self.status}] {self.name}"]
        for n in self.notes:
            lines.append(f"    note: {n}")
        for f in self.flags:
            lines.append(f"    FLAG: {f}")
        if self.status == "PASS" and not self.notes:
            lines.append("    (nothing to report)")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {"name": self.name, "status": self.status, "flags": self.flags, "notes": self.notes}


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _md5_variants(path: Path) -> set[str]:
    """Return the raw-bytes MD5 and the LF-normalized MD5 (CRLF -> LF), lowercase.

    git autocrlf can give a working-copy file CRLF line endings while the MD5
    logged in the tracker was computed on the LF bytes the author saw in the
    Doc (or vice versa) -- accept either.
    """
    raw = path.read_bytes()
    lf = raw.replace(b"\r\n", b"\n")
    return {hashlib.md5(raw).hexdigest().lower(), hashlib.md5(lf).hexdigest().lower()}


def split_tracker_entries(text: str) -> list[tuple[int, str]]:
    """Split the tracker into top-level ``- **`` bullet entries.

    Returns a list of (1-based start line number, entry text) -- an entry runs
    from one top-level bullet up to (but not including) the next one.
    """
    starts = [m.start() for m in ENTRY_START_RE.finditer(text)]
    entries = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        line_no = text.count("\n", 0, start) + 1
        entries.append((line_no, text[start:end]))
    return entries


# ---------------------------------------------------------------------------
# Check 1: tracker <-> snapshot files
# ---------------------------------------------------------------------------


def check_tracker_snapshots(repo_root: Path) -> Section:
    section = Section("1. Tracker <-> snapshot files (tracker/word-count-log.md vs manuscripts/)")
    tracker_path = repo_root / "tracker" / "word-count-log.md"
    text = _read_text(tracker_path)
    if text is None:
        section.flag(f"can't read {tracker_path}")
        return section

    manuscripts_dir = repo_root / "manuscripts"
    entries = split_tracker_entries(text)
    checked = 0
    skipped = 0

    for line_no, entry in entries:
        names = extract_manuscript_refs(entry, manuscripts_dir)
        if not names:
            skipped += 1
            continue
        checked += 1

        accepted_md5s: set[str] = set()
        for name in names:
            full = manuscripts_dir / name
            if not full.exists():
                section.flag(
                    f"tracker/word-count-log.md line {line_no}: cites `{name}`, "
                    "but that file does not exist in manuscripts/"
                )
                continue
            accepted_md5s |= _md5_variants(full)

        entry_md5s = {m.lower() for m in MD5_RE.findall(entry)}
        for md5 in entry_md5s:
            if md5 not in accepted_md5s:
                section.flag(
                    f"tracker/word-count-log.md line {line_no}: MD5 {md5} matches none of "
                    f"this entry's cited files ({', '.join(names) or 'none'}) -- on raw bytes "
                    "or CRLF-normalized bytes"
                )

    section.note(f"{checked} entries checked (cite at least one manuscripts/ path); {skipped} older entries skipped (no cited path, predate the convention)")
    return section


# ---------------------------------------------------------------------------
# Check 2: tracker "Pass logged" claims <-> room ledgers
# ---------------------------------------------------------------------------


def _entry_ledger(entry: str, repo_root: Path) -> tuple[Path | None, str]:
    """Resolve which room ledger an entry's Pass claims belong to.

    Returns (ledger_path_or_None, description_for_messages).
    """
    named = BACKTICKED_LEDGER_RE.findall(entry)
    if named:
        rel = named[0]
        return repo_root / rel, rel

    names = extract_manuscript_refs(entry, repo_root / "manuscripts")
    if names:
        filename = names[0]
        prefix = filename.split("_", 1)[0]
        if prefix in SNAPSHOT_PREFIX_TO_LEDGER:
            rel = SNAPSHOT_PREFIX_TO_LEDGER[prefix]
            return repo_root / rel, rel
        return None, f"(unrecognized snapshot prefix '{prefix}')"

    return None, "(no snapshot path or ledger named in this entry)"


def check_pass_claims(repo_root: Path) -> Section:
    section = Section('2. Tracker "Pass logged" claims <-> room ledgers')
    tracker_path = repo_root / "tracker" / "word-count-log.md"
    text = _read_text(tracker_path)
    if text is None:
        section.flag(f"can't read {tracker_path}")
        return section

    entries = split_tracker_entries(text)
    claims_checked = 0
    ledger_cache: dict[Path, list[str]] = {}

    for line_no, entry in entries:
        stripped = entry.replace("*", "")
        claim_ids = PASS_LOGGED_RE.findall(stripped)
        if not claim_ids:
            continue

        ledger_path, ledger_desc = _entry_ledger(entry, repo_root)
        if ledger_path is None:
            for pass_id in claim_ids:
                section.flag(
                    f"tracker/word-count-log.md line {line_no}: claims 'Pass {pass_id} logged' "
                    f"but can't tell which ledger {ledger_desc}"
                )
            continue

        if not ledger_path.exists():
            for pass_id in claim_ids:
                section.flag(
                    f"tracker/word-count-log.md line {line_no}: claims 'Pass {pass_id} logged' "
                    f"in {ledger_desc}, but that ledger file does not exist"
                )
            continue

        if ledger_path not in ledger_cache:
            ledger_text = _read_text(ledger_path) or ""
            heading_lines = [ln for ln in ledger_text.splitlines() if ln.lstrip().startswith("#")]
            ledger_cache[ledger_path] = heading_lines
        heading_lines = ledger_cache[ledger_path]

        for pass_id in claim_ids:
            claims_checked += 1
            pattern = re.compile(r"Pass\s+" + re.escape(pass_id) + r"(?![0-9A-Za-z])")
            if not any(pattern.search(h) for h in heading_lines):
                section.flag(
                    f"tracker/word-count-log.md line {line_no}: claims 'Pass {pass_id} logged' "
                    f"in {ledger_desc}, but no heading there matches 'Pass {pass_id}'"
                )

    section.note(f"{claims_checked} 'Pass logged' claims checked")
    return section


# ---------------------------------------------------------------------------
# Check 3: current-state head block freshness
# ---------------------------------------------------------------------------


def _section_key(filename: str) -> str | None:
    m = SECTION_KEY_RE.search(filename)
    if not m:
        return None
    key = m.group(1).lower()
    m2 = re.match(r"(ch|interlude)(\d+)", key)
    if m2:
        return m2.group(1) + m2.group(2)
    return key


def _date_in_name(filename: str) -> str | None:
    dates = DATE_IN_NAME_RE.findall(filename)
    return dates[-1] if dates else None


def _find_current_state_table(ledger_text: str) -> list[str]:
    """Return the markdown table rows (as raw lines) under a 'CURRENT STATE' heading, if any."""
    lines = ledger_text.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#") and "CURRENT STATE" in line.upper():
            rows = []
            for line2 in lines[i + 1 :]:
                s = line2.strip()
                if s.startswith("|"):
                    rows.append(line2)
                elif rows:
                    break
            return rows
    return []


def check_current_state_freshness(repo_root: Path) -> Section:
    section = Section("3. Current-state head block freshness (reports/*.room.md)")
    reports_dir = repo_root / "reports"
    ledgers = sorted(reports_dir.glob("*.room.md")) if reports_dir.is_dir() else []
    manuscripts_dir = repo_root / "manuscripts"
    all_snapshots = [p.name for p in manuscripts_dir.glob("*")] if manuscripts_dir.is_dir() else []

    any_table = False
    for ledger in ledgers:
        text = _read_text(ledger) or ""
        rows = _find_current_state_table(text)
        if not rows:
            continue
        any_table = True

        table_filenames: list[str] = []
        for row in rows:
            for name in extract_manuscript_refs(row, manuscripts_dir):
                if name not in table_filenames:
                    table_filenames.append(name)

        # book prefix for this ledger, to scope "snapshots that exist but have no row"
        book_prefixes = {fn.split("_", 1)[0] for fn in table_filenames if "_" in fn}

        section_to_table_files: dict[str, list[str]] = {}
        for fn in table_filenames:
            if not (manuscripts_dir / fn).exists():
                section.flag(f"{ledger.name}: CURRENT STATE table names `{fn}`, but it's missing from manuscripts/")
                continue
            key = _section_key(fn)
            if key:
                section_to_table_files.setdefault(key, []).append(fn)

        # newer-snapshot-for-same-section check
        for key, table_files in section_to_table_files.items():
            candidates = [fn for fn in all_snapshots if _section_key(fn) == key]
            table_dates = [d for d in (_date_in_name(fn) for fn in table_files) if d]
            newest_table_date = max(table_dates) if table_dates else None
            for fn in candidates:
                d = _date_in_name(fn)
                if d and newest_table_date and d > newest_table_date and fn not in table_files:
                    section.flag(
                        f"{ledger.name}: CURRENT STATE table's '{key}' row is stale -- "
                        f"`{fn}` ({d}) is newer than the table's listed snapshot(s) ({', '.join(table_files)})"
                    )

        # sections with snapshots but no table row
        book_snapshots_by_key: dict[str, list[str]] = {}
        for fn in all_snapshots:
            prefix = fn.split("_", 1)[0]
            if prefix not in book_prefixes:
                continue
            key = _section_key(fn)
            if key:
                book_snapshots_by_key.setdefault(key, []).append(fn)

        for key, snaps in book_snapshots_by_key.items():
            if key not in section_to_table_files:
                section.flag(
                    f"{ledger.name}: manuscripts/ has snapshot(s) for section '{key}' "
                    f"({', '.join(sorted(snaps))}) but the CURRENT STATE table has no row for it"
                )

    if not any_table:
        section.note("no ledger currently has a CURRENT STATE table with snapshot filenames")
    return section


# ---------------------------------------------------------------------------
# Check 4: git state
# ---------------------------------------------------------------------------


def _run_git(repo_root: Path, args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args], cwd=repo_root, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def check_git_state(repo_root: Path) -> Section:
    section = Section("4. Git state (branch, uncommitted changes, unmerged commits)")

    rc, branch, err = _run_git(repo_root, ["rev-parse", "--abbrev-ref", "HEAD"])
    if rc != 0:
        section.flag(f"can't determine current branch: {err or 'unknown git error'}")
        return section
    if branch == "HEAD":
        section.flag("repo is in detached HEAD state -- not on any branch")
    else:
        section.note(f"current branch: {branch}")

    rc, status_out, err = _run_git(repo_root, ["status", "--porcelain"])
    if rc != 0:
        section.flag(f"'git status' failed: {err or 'unknown git error'}")
    elif status_out:
        n = len(status_out.splitlines())
        section.flag(f"{n} uncommitted change(s) in the working tree ('git status --porcelain' is not clean)")

    rc, _, _ = _run_git(repo_root, ["rev-parse", "--verify", "origin/main"])
    has_origin_main = rc == 0
    if not has_origin_main:
        section.note("origin/main not found locally -- skipping unmerged-commit checks (no network fetch performed)")
        return section

    if branch != "HEAD":
        rc, counts, err = _run_git(repo_root, ["rev-list", "--left-right", "--count", f"{branch}...origin/main"])
        if rc == 0 and counts:
            parts = counts.split()
            if len(parts) == 2:
                ahead, behind = parts
                if ahead != "0":
                    # SHAs can differ while content is identical under a squash/cherry-pick
                    # workflow -- compare trees before flagging "not merged."
                    rc_h, tree_head, _ = _run_git(repo_root, ["rev-parse", "HEAD^{tree}"])
                    rc_m, tree_main, _ = _run_git(repo_root, ["rev-parse", "origin/main^{tree}"])
                    if rc_h == 0 and rc_m == 0 and tree_head == tree_main:
                        section.note(
                            f"{ahead} commit(s) on '{branch}' not in origin/main by SHA, but content "
                            "is identical to origin/main (commits differ by SHA -- squash/cherry-pick workflow)"
                        )
                    else:
                        rc_d, changed_files, _ = _run_git(
                            repo_root, ["diff", "--name-only", "origin/main", "HEAD"]
                        )
                        files_desc = changed_files.replace("\n", ", ") if rc_d == 0 and changed_files else "(couldn't list changed files)"
                        section.flag(
                            f"{ahead} commit(s) on '{branch}' not in origin/main -- not merged to main yet. "
                            f"Changed files vs origin/main: {files_desc}"
                        )
                if behind != "0":
                    section.note(f"origin/main has {behind} commit(s) not on '{branch}' (branch is behind)")
        else:
            section.note(f"couldn't compare '{branch}' to origin/main: {err}")

    rc, _, _ = _run_git(repo_root, ["rev-parse", "--verify", "main"])
    if rc == 0:
        rc2, counts2, err2 = _run_git(repo_root, ["rev-list", "--left-right", "--count", "main...origin/main"])
        if rc2 == 0 and counts2:
            parts = counts2.split()
            if len(parts) == 2 and (parts[0] != "0" or parts[1] != "0"):
                section.flag(
                    f"local main and origin/main have diverged: {parts[0]} commit(s) only on local main, "
                    f"{parts[1]} only on origin/main"
                )
    else:
        section.note("no local 'main' branch found")

    return section


# ---------------------------------------------------------------------------
# Check 5: memory mirror
# ---------------------------------------------------------------------------


def _default_memory_dir() -> Path:
    userprofile = os.environ.get("USERPROFILE") or str(Path.home())
    return Path(userprofile) / ".claude" / "projects" / "D--Claude-Writing" / "memory"


# Editable: mirror-only files that are expected and never flagged (e.g. the mirror's
# own explainer doc, which has no live counterpart by design).
MIRROR_ONLY_IGNORE = {"README.md"}


def check_memory_mirror(
    repo_root: Path, memory_dir: Path | None, ignore_mirror_only: set[str] | None = None
) -> Section:
    section = Section("5. Memory mirror (live ~/.claude memory vs docs/auto-memory-backup/)")

    if memory_dir is None:
        env_override = os.environ.get("WRITING_MEMORY_DIR")
        memory_dir = Path(env_override) if env_override else _default_memory_dir()

    if not memory_dir.is_dir():
        section.note(f"skipped -- live memory dir not found ({memory_dir})")
        return section

    mirror_dir = repo_root / "docs" / "auto-memory-backup"
    if not mirror_dir.is_dir():
        section.flag(f"live memory dir exists ({memory_dir}) but {mirror_dir} does not")
        return section

    live_files = {p.name: p for p in memory_dir.glob("*.md")}
    mirror_files = {p.name: p for p in mirror_dir.glob("*.md")}

    missing_from_mirror = sorted(set(live_files) - set(mirror_files))
    mirror_only = sorted(set(mirror_files) - set(live_files))
    common = sorted(set(live_files) & set(mirror_files))

    ignore = MIRROR_ONLY_IGNORE if ignore_mirror_only is None else ignore_mirror_only

    for name in missing_from_mirror:
        section.flag(f"{name}: exists in live memory but not in docs/auto-memory-backup/ (mirror is behind)")
    for name in mirror_only:
        if name in ignore:
            section.note(f"{name}: mirror-only file ignored (expected -- not part of the live memory namespace)")
            continue
        section.flag(f"{name}: exists in docs/auto-memory-backup/ but not in the live memory dir (mirror has a stale/extra file)")

    for name in common:
        live_text = (live_files[name].read_text(encoding="utf-8", errors="replace")).replace("\r\n", "\n")
        mirror_text = (mirror_files[name].read_text(encoding="utf-8", errors="replace")).replace("\r\n", "\n")
        if live_text != mirror_text:
            section.flag(f"{name}: content differs between live memory and docs/auto-memory-backup/ (mirror is stale)")

    section.note(f"{len(common)} files compared; {len(missing_from_mirror)} missing from mirror; {len(mirror_only)} mirror-only")
    return section


# ---------------------------------------------------------------------------
# Check 6: handoff freshness
# ---------------------------------------------------------------------------


def check_handoff_freshness(repo_root: Path) -> Section:
    section = Section("6. Handoff freshness (SESSION_HANDOFF.md vs tracker dates)")

    handoff_path = repo_root / "docs" / "SESSION_HANDOFF.md"
    handoff_text = _read_text(handoff_path)
    if handoff_text is None:
        section.flag(f"can't read {handoff_path}")
        return section

    start_here_dates = []
    for line in handoff_text.splitlines():
        if "START HERE" in line:
            start_here_dates += DATE_RE.findall(line)
    if not start_here_dates:
        section.flag(f"no 'START HERE' line with a date found in {handoff_path}")
        return section
    newest_start_here = max(start_here_dates)
    section.note(f"newest START HERE date: {newest_start_here}")

    tracker_path = repo_root / "tracker" / "word-count-log.md"
    tracker_text = _read_text(tracker_path)
    if tracker_text is None:
        section.flag(f"can't read {tracker_path}")
        return section

    entries = split_tracker_entries(tracker_text)
    entry_dates = []
    for line_no, entry in entries:
        first_line = entry.split("\n", 1)[0]
        m = DATE_RE.search(first_line)
        if m:
            entry_dates.append((m.group(1), line_no))
    if not entry_dates:
        section.note("no dated tracker entries found")
        return section

    newest_entry_date, newest_entry_line = max(entry_dates, key=lambda t: t[0])
    section.note(f"newest tracker entry date: {newest_entry_date} (line {newest_entry_line})")

    if newest_entry_date > newest_start_here:
        section.flag(
            f"work logged after the last handoff note -- tracker/word-count-log.md line "
            f"{newest_entry_line} is dated {newest_entry_date}, newer than the last "
            f"START HERE note ({newest_start_here}) in docs/SESSION_HANDOFF.md"
        )

    return section


# ---------------------------------------------------------------------------
# Runner / CLI
# ---------------------------------------------------------------------------


def run_all_checks(repo_root: Path, memory_dir: Path | None = None) -> list[Section]:
    return [
        check_tracker_snapshots(repo_root),
        check_pass_claims(repo_root),
        check_current_state_freshness(repo_root),
        check_git_state(repo_root),
        check_memory_mirror(repo_root, memory_dir),
        check_handoff_freshness(repo_root),
    ]


def render_report(sections: list[Section]) -> str:
    lines = ["Repo health check", "=================", ""]
    for s in sections:
        lines.append(s.render())
        lines.append("")
    any_flag = any(s.status == "FLAG" for s in sections)
    lines.append("RESULT: " + ("FLAGS FOUND -- see above" if any_flag else "all checks passed"))
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="writing_tools.repo_health",
        description="Read-only repo health check for the manuscript-tracking repo. Reports only -- never modifies files.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="path to the repo root (default: current directory)",
    )
    parser.add_argument(
        "--memory-dir",
        default=None,
        help="override the live auto-memory directory (default: $WRITING_MEMORY_DIR or %%USERPROFILE%%\\.claude\\projects\\D--Claude-Writing\\memory)",
    )
    parser.add_argument("--json", action="store_true", help="output JSON instead of plain text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    memory_dir = Path(args.memory_dir) if args.memory_dir else None

    sections = run_all_checks(repo_root, memory_dir)
    any_flag = any(s.status == "FLAG" for s in sections)

    if args.json:
        print(json.dumps({"sections": [s.to_dict() for s in sections], "ok": not any_flag}, indent=2))
    else:
        print(render_report(sections))

    return 1 if any_flag else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
