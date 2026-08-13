from writing_tools import grammar, literary


def test_word_count():
    assert grammar.word_count("The wild wind whipped the waves.") == 6


def test_sentence_count():
    text = "The wild wind whipped the waves. It was as loud as thunder."
    assert grammar.sentence_count(text) == 2


def test_average_sentence_length():
    text = "One two three. Four five six."
    assert grammar.average_sentence_length(text) == 3.0


def test_average_sentence_length_empty():
    assert grammar.average_sentence_length("") == 0.0


def test_find_uncapitalized_sentences():
    text = "This is fine. this is not."
    assert grammar.find_uncapitalized_sentences(text) == ["this is not."]


def test_find_alliteration():
    runs = literary.find_alliteration("The wild wind whipped the waves.")
    assert ["wild", "wind", "whipped"] in runs


def test_find_similes():
    assert literary.find_similes("It was as loud as thunder.") == ["as loud as thunder"]


def test_find_repeated_words():
    counts = literary.find_repeated_words("go go go home home", min_count=2)
    assert counts == {"go": 3, "home": 2}
