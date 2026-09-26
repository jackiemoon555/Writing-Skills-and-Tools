"""Unit tests for writing_tools.repo_health (checks 1-3 and 6), using temp repo trees.

Each test builds a minimal fake repo under ``tmp_path`` (tracker/, manuscripts/,
reports/, docs/ as needed) so the checks can be exercised without touching the
real repo. Nothing here writes to the real project.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

from writing_tools.repo_health import (
    check_current_state_freshness,
    check_git_state,
    check_handoff_freshness,
    check_memory_mirror,
    check_pass_claims,
    check_tracker_snapshots,
    extract_manuscript_refs,
)


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


# ---------------------------------------------------------------------------
# Check 1: tracker <-> snapshot files
# ---------------------------------------------------------------------------


def test_check1_flags_missing_cited_path(tmp_path):
    _write(tmp_path / "manuscripts" / ".keep", "")
    tracker = (
        "- **2026-09-01 — ENTRY.** Snapshot `manuscripts/book_ch1_2026-09-01.txt`. "
        "MD5 00000000000000000000000000000000.\n"
    )
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_tracker_snapshots(tmp_path)
    assert section.status == "FLAG"
    assert any("does not exist in manuscripts/" in f for f in section.flags)


def test_check1_flags_md5_matching_no_cited_file(tmp_path):
    content = b"Some chapter text.\n"
    _write(tmp_path / "manuscripts" / "book_ch1_2026-09-01.txt", "")
    (tmp_path / "manuscripts" / "book_ch1_2026-09-01.txt").write_bytes(content)
    wrong_md5 = _md5(b"totally different bytes")
    tracker = (
        "- **2026-09-01 — ENTRY.** Snapshot `manuscripts/book_ch1_2026-09-01.txt`. "
        f"MD5 {wrong_md5}.\n"
    )
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_tracker_snapshots(tmp_path)
    assert section.status == "FLAG"
    assert any("matches none of this entry's cited files" in f for f in section.flags)


def test_check1_accepts_lf_normalized_md5_for_crlf_file(tmp_path):
    lf_bytes = b"line one\nline two\n"
    crlf_bytes = lf_bytes.replace(b"\n", b"\r\n")
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "book_ch1_2026-09-01.txt").write_bytes(crlf_bytes)

    lf_md5 = _md5(lf_bytes)  # logged MD5 computed on the LF bytes seen in the Doc
    tracker = (
        "- **2026-09-01 — ENTRY.** Snapshot `manuscripts/book_ch1_2026-09-01.txt`. "
        f"MD5 {lf_md5}.\n"
    )
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_tracker_snapshots(tmp_path)
    assert section.status == "PASS"


def test_check1_skips_entries_without_manuscripts_path(tmp_path):
    (tmp_path / "manuscripts").mkdir(parents=True)
    tracker = "- **2026-08-01 — OLD ENTRY, no snapshot convention yet.** Just prose notes.\n"
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_tracker_snapshots(tmp_path)
    assert section.status == "PASS"
    assert any("1 entries checked" not in n and "0 entries checked" in n for n in section.notes)


def test_check1_multiple_entries_only_flags_the_bad_one(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    good_bytes = b"good chapter\n"
    (manuscripts_dir / "book_ch1_2026-09-01.txt").write_bytes(good_bytes)
    (manuscripts_dir / "book_ch2_2026-09-02.txt").write_bytes(b"bad chapter, wrong md5 logged\n")
    good_md5 = _md5(good_bytes)

    tracker = (
        f"- **2026-09-01 — GOOD.** Snapshot `manuscripts/book_ch1_2026-09-01.txt`. MD5 {good_md5}.\n"
        "- **2026-09-02 — BAD.** Snapshot `manuscripts/book_ch2_2026-09-02.txt`. "
        "MD5 11111111111111111111111111111111.\n"
    )
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_tracker_snapshots(tmp_path)
    assert section.status == "FLAG"
    assert len(section.flags) == 1
    assert "ch2" in section.flags[0]


# ---------------------------------------------------------------------------
# Check 2: tracker "Pass logged" claims <-> room ledgers
# ---------------------------------------------------------------------------


def test_check2_explicit_ledger_reference_resolves_and_passes(tmp_path):
    _write(
        tmp_path / "reports" / "some-series.room.md",
        "# ledger\n\n## Pass 1 — the opening (2026-09-01)\nfindings...\n",
    )
    tracker = (
        "- **2026-09-01 — PIECE.** Snapshot `manuscripts/piece_1_2026-09-01.txt`. "
        "Room Pass 1 logged in `reports/some-series.room.md`.\n"
    )
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_pass_claims(tmp_path)
    assert section.status == "PASS"


def test_check2_flags_pass_with_no_matching_heading(tmp_path):
    _write(
        tmp_path / "reports" / "some-series.room.md",
        "# ledger\n\n## Pass 1 — the opening (2026-09-01)\nfindings...\n",
    )
    tracker = (
        "- **2026-09-02 — PIECE.** Snapshot `manuscripts/piece_2_2026-09-02.txt`. "
        "Room Pass 2 logged in `reports/some-series.room.md`.\n"
    )
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_pass_claims(tmp_path)
    assert section.status == "FLAG"
    assert any("Pass 2" in f and "no heading" in f for f in section.flags)


def test_check2_resolves_ledger_via_mapping_when_not_named_explicitly(tmp_path):
    _write(
        tmp_path / "reports" / "task-force-cryptid.room.md",
        "# ledger\n\n## Pass 3a — some pages (2026-09-01)\n",
    )
    tracker = (
        "- **2026-09-01 — CH1.** Snapshot `manuscripts/task-force-cryptid_ch1_2026-09-01.txt`. "
        "Room Pass 3a logged.\n"
    )
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_pass_claims(tmp_path)
    assert section.status == "PASS"


def test_check2_flags_unresolvable_ledger(tmp_path):
    tracker = "- **2026-09-01 — MYSTERY ENTRY.** Room Pass 1 logged, no idea what this is about.\n"
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_pass_claims(tmp_path)
    assert section.status == "FLAG"
    assert any("can't tell which ledger" in f for f in section.flags)


# ---------------------------------------------------------------------------
# Check 3: current-state head block freshness
# ---------------------------------------------------------------------------


def test_check3_flags_missing_table_file(tmp_path):
    _write(
        tmp_path / "reports" / "book.room.md",
        "## CURRENT STATE\n"
        "| Section | Snapshot |\n"
        "| --- | --- |\n"
        "| Ch1 | `manuscripts/book_ch1_2026-09-01.txt` |\n",
    )
    (tmp_path / "manuscripts").mkdir(parents=True)

    section = check_current_state_freshness(tmp_path)
    assert section.status == "FLAG"
    assert any("missing from manuscripts/" in f for f in section.flags)


def test_check3_flags_stale_row_when_newer_snapshot_exists(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "book_ch1_2026-09-01.txt").write_text("old", encoding="utf-8")
    (manuscripts_dir / "book_ch1-revised_2026-09-05.txt").write_text("new", encoding="utf-8")
    _write(
        tmp_path / "reports" / "book.room.md",
        "## CURRENT STATE\n"
        "| Section | Snapshot |\n"
        "| --- | --- |\n"
        "| Ch1 | `manuscripts/book_ch1_2026-09-01.txt` |\n",
    )

    section = check_current_state_freshness(tmp_path)
    assert section.status == "FLAG"
    assert any("stale" in f and "ch1" in f for f in section.flags)


def test_check3_flags_section_with_snapshots_but_no_table_row(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "book_ch1_2026-09-01.txt").write_text("ch1", encoding="utf-8")
    (manuscripts_dir / "book_ch2_2026-09-02.txt").write_text("ch2", encoding="utf-8")
    _write(
        tmp_path / "reports" / "book.room.md",
        "## CURRENT STATE\n"
        "| Section | Snapshot |\n"
        "| --- | --- |\n"
        "| Ch1 | `manuscripts/book_ch1_2026-09-01.txt` |\n",
    )

    section = check_current_state_freshness(tmp_path)
    assert section.status == "FLAG"
    assert any("no row for it" in f and "ch2" in f for f in section.flags)


def test_check3_passes_when_table_is_fully_current(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "book_ch1_2026-09-01.txt").write_text("ch1", encoding="utf-8")
    _write(
        tmp_path / "reports" / "book.room.md",
        "## CURRENT STATE\n"
        "| Section | Snapshot |\n"
        "| --- | --- |\n"
        "| Ch1 | `manuscripts/book_ch1_2026-09-01.txt` |\n",
    )

    section = check_current_state_freshness(tmp_path)
    assert section.status == "PASS"


# ---------------------------------------------------------------------------
# Check 6: handoff freshness
# ---------------------------------------------------------------------------


def test_check6_flags_work_logged_after_last_handoff(tmp_path):
    _write(
        tmp_path / "docs" / "SESSION_HANDOFF.md",
        "> ## NEXT SESSION — START HERE (2026-09-01)\nstuff\n",
    )
    _write(
        tmp_path / "tracker" / "word-count-log.md",
        "- **2026-09-05 — NEW WORK.** Snapshot stuff.\n",
    )

    section = check_handoff_freshness(tmp_path)
    assert section.status == "FLAG"
    assert any("after the last handoff note" in f for f in section.flags)


def test_check6_passes_when_tracker_not_newer_than_handoff(tmp_path):
    _write(
        tmp_path / "docs" / "SESSION_HANDOFF.md",
        "> ## NEXT SESSION — START HERE (2026-09-05)\nstuff\n",
    )
    _write(
        tmp_path / "tracker" / "word-count-log.md",
        "- **2026-09-01 — OLD WORK.** Snapshot stuff.\n"
        "- **2026-09-05 — SAME DAY WORK.** Snapshot stuff.\n",
    )

    section = check_handoff_freshness(tmp_path)
    assert section.status == "PASS"


# ---------------------------------------------------------------------------
# extract_manuscript_refs: ellipsis shorthand (a), bare snapshot filenames (b),
# and the negative case that must NOT resolve
# ---------------------------------------------------------------------------


def test_extract_refs_resolves_ellipsis_suffix_when_exactly_one_match(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "task-force-cryptid_ch2_docpull_2026-09-21.txt").write_text("x", encoding="utf-8")
    (manuscripts_dir / "task-force-cryptid_prologue-v4_docpull_2026-09-21.txt").write_text("x", encoding="utf-8")

    text = (
        "Snapshot `manuscripts/task-force-cryptid_ch3.2-frank_docpull_2026-09-21.txt`. "
        "Same pull: prologue snapshot `…_prologue-v4_docpull_2026-09-21.txt` and "
        "Ch2 snapshot `…_ch2_docpull_2026-09-21.txt`."
    )
    refs = extract_manuscript_refs(text, manuscripts_dir)
    assert "task-force-cryptid_prologue-v4_docpull_2026-09-21.txt" in refs
    assert "task-force-cryptid_ch2_docpull_2026-09-21.txt" in refs


def test_extract_refs_ellipsis_ascii_dots_also_resolves(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "book_ch5_docpull_2026-09-24.txt").write_text("x", encoding="utf-8")

    refs = extract_manuscript_refs("Snapshot `..._ch5_docpull_2026-09-24.txt`.", manuscripts_dir)
    assert refs == ["book_ch5_docpull_2026-09-24.txt"]


def test_extract_refs_ellipsis_suffix_ambiguous_does_not_resolve(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "book_ch5_docpull_2026-09-24.txt").write_text("x", encoding="utf-8")
    (manuscripts_dir / "other-book_ch5_docpull_2026-09-24.txt").write_text("x", encoding="utf-8")

    # both files end with this suffix -- ambiguous, must not resolve to either
    refs = extract_manuscript_refs("Snapshot `…_ch5_docpull_2026-09-24.txt`.", manuscripts_dir)
    assert refs == []


def test_extract_refs_resolves_bare_filename_with_date(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "the-champ_export_2026-08-23.txt").write_text("x", encoding="utf-8")
    (manuscripts_dir / "the-champ_export_2026-08-23.docx").write_text("x", encoding="utf-8")

    text = (
        "archived as `manuscripts/the-champ_export_2026-08-23.docx`; text extract "
        "`the-champ_export_2026-08-23.txt`, MD5 of text `15db9d41a771fa9ce43f24cff78f29df`"
    )
    refs = extract_manuscript_refs(text, manuscripts_dir)
    assert "the-champ_export_2026-08-23.txt" in refs
    assert "the-champ_export_2026-08-23.docx" in refs


def test_extract_refs_negative_case_bare_extension_mention_does_not_resolve(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "the-champ_export_2026-08-23.docx").write_text("x", encoding="utf-8")

    # a generic mention of the file type, not an actual filename -- must NOT resolve
    refs = extract_manuscript_refs("Google Docs (exported from Reedsy as `.docx`)", manuscripts_dir)
    assert refs == []


def test_extract_refs_negative_case_no_date_does_not_resolve(tmp_path):
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)
    (manuscripts_dir / "book_notes.txt").write_text("x", encoding="utf-8")

    # bare filename with no date in the stem -- too generic to trust, must NOT resolve
    refs = extract_manuscript_refs("See `book_notes.txt` for details.", manuscripts_dir)
    assert refs == []


def test_check1_passes_on_real_repo_style_ellipsis_and_bare_filename_entries(tmp_path):
    """Regression test for the two real-repo false positives the coordinator verified by hand."""
    manuscripts_dir = tmp_path / "manuscripts"
    manuscripts_dir.mkdir(parents=True)

    ch3_bytes = b"ch3.2 text\n"
    prologue_bytes = b"prologue text\n"
    ch2_bytes = b"ch2 text\n"
    (manuscripts_dir / "task-force-cryptid_ch3.2-frank_docpull_2026-09-21.txt").write_bytes(ch3_bytes)
    (manuscripts_dir / "task-force-cryptid_prologue-v4_docpull_2026-09-21.txt").write_bytes(prologue_bytes)
    (manuscripts_dir / "task-force-cryptid_ch2_docpull_2026-09-21.txt").write_bytes(ch2_bytes)

    tracker = (
        "- **2026-09-21 — CH3.2 ENTRY.** Snapshot "
        "`manuscripts/task-force-cryptid_ch3.2-frank_docpull_2026-09-21.txt`. "
        f"MD5 {hashlib.md5(ch3_bytes).hexdigest()}. "
        "Same pull: prologue snapshot `…_prologue-v4_docpull_2026-09-21.txt`, MD5 "
        f"{hashlib.md5(prologue_bytes).hexdigest()} and Ch2 snapshot "
        f"`…_ch2_docpull_2026-09-21.txt`, MD5 {hashlib.md5(ch2_bytes).hexdigest()}.\n"
    )
    _write(tmp_path / "tracker" / "word-count-log.md", tracker)

    section = check_tracker_snapshots(tmp_path)
    assert section.status == "PASS"


# ---------------------------------------------------------------------------
# Check 4: git state -- squash/cherry-pick workflow tree comparison
# ---------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()


def _init_repo(repo: Path) -> None:
    repo.mkdir(parents=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")


def test_check4_passes_when_tree_matches_origin_main_despite_different_shas(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    (repo / "file.txt").write_text("hello", encoding="utf-8")
    _git(repo, "add", "file.txt")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "branch", "-m", "main")
    _git(repo, "update-ref", "refs/remotes/origin/main", "main")

    _git(repo, "checkout", "-q", "-b", "feature")
    (repo / "file.txt").write_text("changed", encoding="utf-8")
    _git(repo, "commit", "-q", "-a", "-m", "feature change")
    # simulate a squash-merge of the SAME content onto main, under a NEW sha
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--squash", "feature")
    _git(repo, "commit", "-q", "-m", "squashed feature onto main")
    _git(repo, "update-ref", "refs/remotes/origin/main", "main")
    _git(repo, "checkout", "-q", "feature")

    section = check_git_state(repo)
    assert not any("not merged to main yet" in f for f in section.flags)
    assert any("content is identical to origin/main" in n for n in section.notes)


def test_check4_flags_and_lists_changed_files_when_trees_differ(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    (repo / "file.txt").write_text("hello", encoding="utf-8")
    _git(repo, "add", "file.txt")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "branch", "-m", "main")
    _git(repo, "update-ref", "refs/remotes/origin/main", "main")

    _git(repo, "checkout", "-q", "-b", "feature")
    (repo / "file.txt").write_text("changed but never merged", encoding="utf-8")
    _git(repo, "commit", "-q", "-a", "-m", "unmerged change")

    section = check_git_state(repo)
    assert any("not merged to main yet" in f for f in section.flags)
    assert any("file.txt" in f for f in section.flags)


# ---------------------------------------------------------------------------
# Check 5: memory mirror -- ignore list for expected mirror-only files
# ---------------------------------------------------------------------------


def test_check5_ignores_default_mirror_only_readme(tmp_path):
    live_dir = tmp_path / "live-memory"
    live_dir.mkdir(parents=True)
    (live_dir / "note.md").write_text("hello", encoding="utf-8")

    mirror_dir = tmp_path / "docs" / "auto-memory-backup"
    mirror_dir.mkdir(parents=True)
    (mirror_dir / "note.md").write_text("hello", encoding="utf-8")
    (mirror_dir / "README.md").write_text("this mirror's own explainer", encoding="utf-8")

    section = check_memory_mirror(tmp_path, live_dir)
    assert section.status == "PASS"
    assert any("README.md" in n and "ignored" in n for n in section.notes)


def test_check5_still_flags_unignored_mirror_only_file(tmp_path):
    live_dir = tmp_path / "live-memory"
    live_dir.mkdir(parents=True)
    (live_dir / "note.md").write_text("hello", encoding="utf-8")

    mirror_dir = tmp_path / "docs" / "auto-memory-backup"
    mirror_dir.mkdir(parents=True)
    (mirror_dir / "note.md").write_text("hello", encoding="utf-8")
    (mirror_dir / "stale-extra.md").write_text("nobody asked for this", encoding="utf-8")

    section = check_memory_mirror(tmp_path, live_dir)
    assert section.status == "FLAG"
    assert any("stale-extra.md" in f for f in section.flags)
