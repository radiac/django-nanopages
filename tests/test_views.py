from pathlib import Path
from unittest.mock import MagicMock

import pytest
from django.http import Http404, HttpResponse
from django.test import RequestFactory

from django_nanopages.views import Page


@pytest.fixture
def page(tmp_path):
    page = Page()
    page.pages = MagicMock()
    page.pages.path = tmp_path
    page.request = RequestFactory().get("/")
    return page


def test_view__find_src_valid_md(page):
    md_file = page.pages.path / "test.md"
    md_file.write_text("# Test Markdown")
    result = page.find_src("test")
    assert result == md_file


def test_view__find_src_valid_html(page):
    html_file = page.pages.path / "test.html"
    html_file.write_text("<h1>Test HTML</h1>")
    result = page.find_src("test")
    assert result == html_file


def test_find_src_not_found(page):
    with pytest.raises(Http404):
        page.find_src("non_existent")


def test_parse_context_no_context(page):
    raw = "This is a test."
    result = page.parse_context(raw)
    assert result == (raw, {"base": "base.html"})


def test_parse_context_with_key_value(page):
    raw = "---\nkey: value\n---\nThis is a test."
    result = page.parse_context(raw)
    assert result[1] == {"base": "base.html", "key": "value"}
    assert result[0] == "This is a test."


def test_parse_context_with_yaml(page):
    raw = "---yaml\nkey: value\n---\nThis is a test."
    result = page.parse_context(raw)
    assert result[1] == {"base": "base.html", "key": "value"}
    assert result[0] == "This is a test."


def test_parse_context_with_json(page):
    """Test parsing raw content with JSON context."""
    raw = '---json\n{"key": "value"}\n---\nThis is a test.'
    result = page.parse_context(raw)
    assert result[1] == {"base": "base.html", "key": "value"}
    assert result[0] == "This is a test."


def test_render_md(page):
    md_file = page.pages.path / "test.md"
    md_file.write_text("---\nkey: value\n---\n# Test Markdown")

    response = page.render_md(md_file)
    assert isinstance(response, HttpResponse)
    assert "content" in response.context_data
    assert response.context_data["content"] == "<h1>Test Markdown</h1>"


def test_render_html(page):
    html_file = page.pages.path / "test.html"
    html_file.write_text("---\nkey: value\n---\n<h1>Test HTML</h1>")

    response = page.render_html(html_file)
    assert isinstance(response, HttpResponse)
    assert "key" in response.context_data
    assert response.context_data["key"] == "value"
