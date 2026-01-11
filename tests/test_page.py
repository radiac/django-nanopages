from pathlib import Path
from unittest.mock import MagicMock

import pytest

from django_nanopages.page import Page


@pytest.fixture
def pages_mock(tmp_path):
    pages = MagicMock()
    pages.path = tmp_path
    pages.context = None
    return pages


def test_find_src_valid_md(pages_mock):
    md_file = pages_mock.path / "test.md"
    md_file.write_text("# Test Markdown")

    page = Page(request_path="test", pages=pages_mock)
    assert page.exists is True
    assert page.src == md_file


def test_find_src_valid_html(pages_mock):
    html_file = pages_mock.path / "test.html"
    html_file.write_text("<h1>Test HTML</h1>")

    page = Page(request_path="test", pages=pages_mock)
    assert page.exists is True
    assert page.src == html_file


def test_find_src_prefers_html_over_md(pages_mock):
    html_file = pages_mock.path / "test.html"
    html_file.write_text("<h1>Test HTML</h1>")
    md_file = pages_mock.path / "test.md"
    md_file.write_text("# Test Markdown")

    page = Page(request_path="test", pages=pages_mock)
    # HTML is checked first in the search order
    assert page.exists is True
    assert page.src == html_file


def test_find_src_index_html(pages_mock):
    index_file = pages_mock.path / "index.html"
    index_file.write_text("<h1>Index</h1>")

    page = Page(request_path="", pages=pages_mock)
    assert page.exists is True
    assert page.src == index_file


def test_find_src_index_md(pages_mock):
    index_file = pages_mock.path / "index.md"
    index_file.write_text("# Index")

    page = Page(request_path="", pages=pages_mock)
    assert page.exists is True
    assert page.src == index_file


def test_find_src_subdirectory(pages_mock):
    subdir = pages_mock.path / "subdir"
    subdir.mkdir()
    md_file = subdir / "page.md"
    md_file.write_text("# Subdir Page")

    page = Page(request_path="subdir/page", pages=pages_mock)
    assert page.exists is True
    assert page.src == md_file


def test_find_src_not_found(pages_mock):
    page = Page(request_path="non_existent", pages=pages_mock)
    assert page.exists is False
    assert page.src == Path("")


def test_find_src_outside_root(pages_mock):
    page = Page(request_path="../outside", pages=pages_mock)
    assert page.exists is False
    assert page.src == Path("")


def test_read_no_frontmatter(pages_mock):
    test_file = pages_mock.path / "test.md"
    test_file.write_text("This is a test.")

    page = Page(request_path="test", pages=pages_mock)
    body, context = page.read()

    assert body == "This is a test."
    assert context == {"base": "base.html"}


def test_read_with_key_value_frontmatter(pages_mock):
    test_file = pages_mock.path / "test.md"
    test_file.write_text("---\nkey: value\n---\nThis is a test.")

    page = Page(request_path="test", pages=pages_mock)
    body, context = page.read()

    assert body == "This is a test."
    assert context == {"base": "base.html", "key": "value"}


def test_read_with_extra_context(pages_mock):
    test_file = pages_mock.path / "test.md"
    test_file.write_text("---\nkey: value\n---\nThis is a test.")

    page = Page(request_path="test", pages=pages_mock, extra_context={"extra": "context"})
    body, context = page.read()

    assert body == "This is a test."
    assert context == {"base": "base.html", "extra": "context", "key": "value"}


def test_read_with_yaml_frontmatter(pages_mock):
    test_file = pages_mock.path / "test.md"
    test_file.write_text("---yaml\nkey: value\n---\nThis is a test.")

    page = Page(request_path="test", pages=pages_mock)
    body, context = page.read()

    assert body == "This is a test."
    assert context == {"base": "base.html", "key": "value"}


def test_read_with_json_frontmatter(pages_mock):
    test_file = pages_mock.path / "test.md"
    test_file.write_text('---json\n{"key": "value"}\n---\nThis is a test.')

    page = Page(request_path="test", pages=pages_mock)
    body, context = page.read()

    assert body == "This is a test."
    assert context == {"base": "base.html", "key": "value"}


def test_as_html_md(pages_mock):
    md_file = pages_mock.path / "test.md"
    md_file.write_text("---\nkey: value\n---\n# Test Markdown")

    page = Page(request_path="test", pages=pages_mock)
    content = page.as_html()

    assert content == "<h1>Test Markdown</h1>"
    assert page.context["key"] == "value"
    assert page.context["base"] == "base.html"


def test_as_html_html(pages_mock):
    html_file = pages_mock.path / "test.html"
    html_file.write_text("---\nkey: value\n---\n<h1>Test HTML</h1>")

    page = Page(request_path="test", pages=pages_mock)
    content = page.as_html()

    assert content == "<h1>Test HTML</h1>"
    assert page.context["key"] == "value"
    assert page.context["base"] == "base.html"


def test_as_html_with_extra_context(pages_mock):
    md_file = pages_mock.path / "test.md"
    md_file.write_text("# Test")

    page = Page(request_path="test", pages=pages_mock, extra_context={"extra": "value"})
    content = page.as_html()

    assert content == "<h1>Test</h1>"
    assert page.context["extra"] == "value"
    assert page.context["base"] == "base.html"


def test_read_caching(pages_mock):
    test_file = pages_mock.path / "test.md"
    test_file.write_text("# Test")

    page = Page(request_path="test", pages=pages_mock)

    # First read should populate cache
    body1, context1 = page.read()
    assert page._body is not None
    assert page._context is not None

    # Second read should return cached values
    body2, context2 = page.read()
    assert body1 is body2
    assert context1 is context2

    # Reload should fetch new data
    test_file.write_text("# Updated")
    body3, context3 = page.read(reload=True)
    assert body3 != body1
    assert body3 == "# Updated"


def test_body_property(pages_mock):
    test_file = pages_mock.path / "test.md"
    test_file.write_text("---\nkey: value\n---\n# Test")

    page = Page(request_path="test", pages=pages_mock)

    # Access body property should trigger read
    body = page.body
    assert body == "# Test"
    assert page._body is not None


def test_context_property(pages_mock):
    test_file = pages_mock.path / "test.md"
    test_file.write_text("---\nkey: value\n---\n# Test")

    page = Page(request_path="test", pages=pages_mock)

    # Access context property should trigger read
    context = page.context
    assert context["key"] == "value"
    assert page._context is not None


def test_name_simple_page(pages_mock):
    test_file = pages_mock.path / "about.md"
    test_file.write_text("# About")

    page = Page(request_path="about", pages=pages_mock)
    assert page.name == "about"


def test_name_nested_page(pages_mock):
    subdir = pages_mock.path / "blog"
    subdir.mkdir()
    post_file = subdir / "first-post.md"
    post_file.write_text("# First Post")

    page = Page(request_path="blog/first-post", pages=pages_mock)
    assert page.name == "first-post"


def test_name_deeply_nested_page(pages_mock):
    dir1 = pages_mock.path / "docs"
    dir1.mkdir()
    dir2 = dir1 / "guide"
    dir2.mkdir()
    page_file = dir2 / "getting-started.md"
    page_file.write_text("# Getting Started")

    page = Page(request_path="docs/guide/getting-started", pages=pages_mock)
    assert page.name == "getting-started"


def test_name_index_page(pages_mock):
    index_file = pages_mock.path / "index.md"
    index_file.write_text("# Home")

    page = Page(request_path="", pages=pages_mock)
    assert page.name == ""


def test_name_nested_index_page(pages_mock):
    subdir = pages_mock.path / "blog"
    subdir.mkdir()
    index_file = subdir / "index.md"
    index_file.write_text("# Blog")

    page = Page(request_path="blog", pages=pages_mock)
    assert page.name == "blog"
