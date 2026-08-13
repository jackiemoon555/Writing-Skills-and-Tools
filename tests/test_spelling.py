from writing_tools.spelling import SpellChecker, load_custom_dictionary

KNOWN = {"the", "wizard", "cast", "a", "spell", "over", "castle", "and", "left"}


def test_flags_unknown_word():
    checker = SpellChecker(known_words=KNOWN)
    findings = checker.check("The wizard cast a spelll over the castle.")
    words = [f.message for f in findings]
    assert any("spelll" in m for m in words)
    # correctly spelled words are not flagged
    assert not any("wizard" in m for m in words)


def test_custom_dictionary_suppresses_names():
    # "Zyrelle" is an invented name; adding it to the custom dict clears the flag.
    checker = SpellChecker(custom_words=["Zyrelle"], known_words=KNOWN)
    findings = checker.check("Zyrelle cast a spell.")
    assert not any("Zyrelle" in f.message for f in findings)


def test_unknown_name_is_flagged_without_custom_dict():
    checker = SpellChecker(known_words=KNOWN)
    findings = checker.check("Zyrelle cast a spell.")
    assert any("Zyrelle" in f.message for f in findings)


def test_short_words_and_acronyms_skipped():
    checker = SpellChecker(known_words=KNOWN)
    findings = checker.check("Go FBI xy")  # all too short or acronym
    assert findings == []


def test_load_custom_dictionary(tmp_path):
    p = tmp_path / "names.txt"
    p.write_text("# my names\nZyrelle\nMorrowind\n", encoding="utf-8")
    words = load_custom_dictionary(p)
    assert "zyrelle" in words and "morrowind" in words
    assert "# my names" not in words


def test_unknown_word_summary_counts():
    checker = SpellChecker(known_words=KNOWN)
    summary = checker.unknown_word_summary("Zyrelle met Zyrelle near Morrowind.")
    assert summary.get("zyrelle") == 2
    assert summary.get("morrowind") == 1
