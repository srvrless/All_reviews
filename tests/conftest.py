import pytest
import sys

sys.path.append('..')

from app import create_app, engine
from app.database import db_session
from app.models import User

pytest_plugins = ['db_fixtures']

# ПРИ ТЕСТИРОВАНИЕ УКАЗЫВАЙТЕ СВОЮ БД
@pytest.fixture(scope='function', autouse=True)
def testapp():
    app_ = create_app
    from app import models
    models.Base.metadata.create_all(bind=engine)
    app_.connection = engine.connect()

    yield create_app

    models.Base.metadata.drop_all(bind=engine)
    app_.connection.close()


@pytest.fixture(scope='function')
def session(testapp):
    ctx = create_app().app_context()
    ctx.push()
    yield db_session
    db_session.close_all()
    ctx.pop()


@pytest.fixture(scope='function')
def user(session):
    user = User(
        username='neverless',
        email_address='maijor18@mail.ru',
        password_hash='password_hash'
    )
    session.add(user)
    session.commit()

    return user


# @pytest.fixture
# def client(testapp):
#     return testapp.test_client()


@pytest.fixture
def user_token(user, testapp):
    res = testapp.post('/login', json={'email_address': user.email_address,
                                      'password': user.password_hash})
    return res.get_json()['access_token']

@pytest.fixture
def user_headers(user_token):
    headers={
        'Authorization': f'Bearer {user_token}'
    }
    return headers