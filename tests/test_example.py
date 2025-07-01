import urllib.request
from urllib.error import HTTPError, URLError

import pytest
from nanodjango.testing.utils import cmd, nanodjango_process, runserver

TEST_APP = "website"
TEST_SCRIPT = f"../example/{TEST_APP}.py"
TEST_BIND = "127.0.0.1:8042"


@pytest.fixture(scope="module")  # or 'session' for session-wide setup
def example():
    with (
        nanodjango_process(
            "--plugin=django_nanopages.nanodjango",
            "manage",
            TEST_SCRIPT,
            "runserver",
            TEST_BIND,
        ) as handle,
        runserver(handle),
    ):
        yield handle


def get(url: str) -> tuple[int, str]:
    try:
        response = urllib.request.urlopen(url, timeout=10)
    except HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except URLError as e:
        return 0, str(e)
    return response.getcode(), response.read().decode("utf-8")


def test_example__index(example):
    status, html = get(f"http://{TEST_BIND}/")
    assert status == 200
    assert "<p>Welcome to the example site.</p>" in html


def test_example__about(example):
    status, html = get(f"http://{TEST_BIND}/about/")
    assert status == 200
    assert '<a href="/">Return to home</a>' in html


def test_example__blog_index(example):
    status, html = get(f"http://{TEST_BIND}/blog/")
    assert status == 200
    assert "<h1>django-nanopages example blog</h1>" in html


def test_example__blog_cookies(example):
    status, html = get(f"http://{TEST_BIND}/blog/cookies/")
    assert status == 200
    assert "<li>Allow them to cool on a wire rack.</li>" in html


def test_example__blog_work(example):
    status, html = get(f"http://{TEST_BIND}/blog/work/")
    assert status == 200
    assert "<p>All work and no play makes Jack a dull boy. All work and no play" in html
