import pytest

pytest_plugins = ['db_fixtures']


@pytest.fixture(scope='session', autouse=True)
def create_moderate_tables():
    from app.database import init_db
    init_db()
