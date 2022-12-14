import pytest

pytest_plugins = ['db_fixtures']


@pytest.fixture
def fixture_a():
    return 'value'
