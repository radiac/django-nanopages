from pathlib import Path

import pytest

from django_nanopages.page import Page
from django_nanopages.pages import Pages


@pytest.fixture
def pages_dir(tmp_path, settings):
    settings.BASE_DIR = tmp_path
    pages_path = tmp_path / "pages"
    pages_path.mkdir()
    return pages_path


def test_get_page_returns_page_instance(pages_dir):
    md_file = pages_dir / "test.md"
    md_file.write_text("# Test")

    pages = Pages(pages_dir)
    page = pages.get_page("test")

    assert isinstance(page, Page)
    assert page.request_path == "test"
    assert page.pages == pages


def test_get_page_with_context(pages_dir):
    md_file = pages_dir / "test.md"
    md_file.write_text("# Test")

    pages = Pages(pages_dir, context={"site_name": "Test Site"})
    page = pages.get_page("test")

    assert page is not None
    assert page.extra_context == {"site_name": "Test Site"}


def test_get_page_finds_correct_file(pages_dir):
    md_file = pages_dir / "test.md"
    md_file.write_text("# Test Content")

    pages = Pages(pages_dir)
    page = pages.get_page("test")

    assert page is not None
    assert page.src == md_file


def test_get_page_returns_none_for_missing_file(pages_dir):
    pages = Pages(pages_dir)
    page = pages.get_page("non_existent")
    assert page is None


def test_get_page_with_subdirectory(pages_dir):
    subdir = pages_dir / "subdir"
    subdir.mkdir()
    md_file = subdir / "page.md"
    md_file.write_text("# Subdir Page")

    pages = Pages(pages_dir)
    page = pages.get_page("subdir/page")

    assert page is not None
    assert page.src == md_file
