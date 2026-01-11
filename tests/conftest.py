import pytest

from django_nanopages.pages import registry


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear the Pages registry before each test to ensure test isolation."""
    registry.clear()
