import zipfile

import pytest

from writing_tools.loaders import Document, load_document, iter_manuscript_files

DOCX_XML = (
    '<?xml version="1.0"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    "<w:body>"
    "<w:p><w:r><w:t>Chapter One</w:t></w:r></w:p>"
    "<w:p><w:r><w:t>The wind </w:t></w:r><w:r><w:t>rose.</w:t></w:r></w:p>"
    "</w:body></w:document>"
)


def _make_docx(path):
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", DOCX_XML)


def test_load_txt(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("Hello world.", encoding="utf-8")
    doc = load_document(p)
    assert isinstance(doc, Document)
    assert doc.text == "Hello world."
    assert doc.name == "a.txt"


def test_load_markdown_strips_syntax(tmp_path):
    p = tmp_path / "a.md"
    p.write_text("# Heading\n\nSome **bold** and `code` text.", encoding="utf-8")
    doc = load_document(p)
    assert "#" not in doc.text
    assert "**" not in doc.text
    assert "bold" in doc.text and "code" in doc.text


def test_load_docx_builtin_reader(tmp_path):
    p = tmp_path / "chapter.docx"
    _make_docx(p)
    doc = load_document(p)
    assert "Chapter One" in doc.text
    assert "The wind rose." in doc.text


def test_unsupported_type_raises(tmp_path):
    p = tmp_path / "a.pdf"
    p.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError):
        load_document(p)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_document(tmp_path / "nope.txt")


def test_iter_manuscript_files_sorted(tmp_path):
    (tmp_path / "02.txt").write_text("b", encoding="utf-8")
    (tmp_path / "01.md").write_text("a", encoding="utf-8")
    (tmp_path / "notes.pdf").write_text("skip", encoding="utf-8")
    files = iter_manuscript_files(tmp_path)
    names = [f.name for f in files]
    assert names == ["01.md", "02.txt"]
