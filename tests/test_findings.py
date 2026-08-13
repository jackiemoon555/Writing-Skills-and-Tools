from writing_tools.findings import LineIndex, iter_words, normalize_word, snippet


def test_line_index_positions():
    idx = LineIndex("abc\ndef\nghi")
    assert idx.position(0) == (1, 1)
    assert idx.position(2) == (1, 3)
    assert idx.position(4) == (2, 1)  # 'd' on line 2
    assert idx.position(8) == (3, 1)  # 'g' on line 3


def test_line_index_line_text():
    idx = LineIndex("first line\nsecond line")
    assert idx.line_text(1) == "first line"
    assert idx.line_text(2) == "second line"
    assert idx.line_text(99) == ""


def test_iter_words_offsets():
    tokens = list(iter_words("Hello world\nagain"))
    assert [t.text for t in tokens] == ["Hello", "world", "again"]
    assert tokens[0].line == 1 and tokens[0].column == 1
    assert tokens[2].line == 2 and tokens[2].column == 1


def test_normalize_word():
    assert normalize_word("Don’t") == "don't"
    assert normalize_word("HELLO") == "hello"


def test_snippet_truncates():
    text = "x" * 200
    snip = snippet(text, 100, width=10)
    assert snip.startswith("…") and snip.endswith("…")
