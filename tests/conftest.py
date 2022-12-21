import pytest

from app import create_app
from app.models import User

pytest_plugins = ['db_fixtures']


@pytest.fixture(scope='session')
def flask_app():
    app = create_app()

    client = app.test_client()
    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()
