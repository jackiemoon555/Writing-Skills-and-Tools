from writing_tools import report
from writing_tools.style import (
    find_adverbs,
    find_echoes,
    find_filler_words,
    find_filter_words,
    run_style_passes,
)


def test_find_echoes_flags_repeats():
    text = "shadow " * 5 + "and light"
    findings = find_echoes(text, min_count=4)
    assert len(findings) == 1
    assert "shadow" in findings[0].message
    assert "5 times" in findings[0].message


def test_find_echoes_ignores_stopwords():
    text = "the the the the the cat"
    assert find_echoes(text, min_count=3) == []


def test_find_filter_words():
    findings = find_filter_words("She saw the door and felt afraid.")
    flagged = {f.message.split("'")[1].lower() for f in findings}
    assert "saw" in flagged and "felt" in flagged


def test_find_filler_words():
    findings = find_filler_words("It was very really just fine.")
    flagged = {f.message.split("'")[1].lower() for f in findings}
    assert {"very", "really", "just"} <= flagged


def test_find_adverbs_skips_non_adverbs():
    findings = find_adverbs("He quietly closed the door with his family.")
    flagged = {f.message.split("'")[1].lower() for f in findings}
    assert "quietly" in flagged
    assert "family" not in flagged  # on the not-adverb allow-list


def test_run_style_passes_combines():
    findings = run_style_passes("She suddenly saw the door.")
    categories = {f.category for f in findings}
    assert "filter-word" in categories
    assert "filler-word" in categories


def test_report_markdown_and_html_roundtrip():
    findings = run_style_passes("She suddenly saw the very dark door.")
    md = report.to_markdown(findings, title="Test")
    html = report.to_html(findings, title="Test")
    assert "# Test" in md
    assert "<title>Test</title>" in html
    assert "items flagged" in md


def test_report_empty_is_clean():
    md = report.to_markdown([], title="Clean")
    assert "No issues flagged" in md
