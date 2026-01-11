from pathlib import Path
from unittest.mock import MagicMock

import pytest
from django.http import Http404, HttpResponse
from django.test import RequestFactory

from django_nanopages.page import Page
from django_nanopages.pages import Pages
from django_nanopages.views import PageView


@pytest.fixture
def page_view(tmp_path):
    page_view = PageView()
    page_view.pages = MagicMock()
    page_view.pages.path = tmp_path
    page_view.request = RequestFactory().get("/")
    return page_view


def test_render_md(page_view):
    md_file = page_view.pages.path / "test.md"
    md_file.write_text("---\nkey: value\n---\n# Test Markdown")

    page = Page(request_path="test", pages=page_view.pages)
    response = page_view.render_md(page)
    assert isinstance(response, HttpResponse)
    assert page.context["key"] == "value"
    assert page.as_html() == "<h1>Test Markdown</h1>"


def test_render_html(page_view):
    html_file = page_view.pages.path / "test.html"
    html_file.write_text("---\nkey: value\n---\n<h1>Test HTML</h1>")

    page = Page(request_path="test", pages=page_view.pages)
    response = page_view.render_html(page)
    assert isinstance(response, HttpResponse)
    assert page.context["key"] == "value"
    assert b"<h1>Test HTML</h1>" in response.content


def test_view_raises_404_for_missing_page(tmp_path, settings):
    settings.BASE_DIR = tmp_path
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()

    page_view = PageView()
    page_view.pages = Pages(pages_dir)
    page_view.request = RequestFactory().get("/non_existent/")

    with pytest.raises(Http404):
        page_view.get(page_view.request, request_path="non_existent")
