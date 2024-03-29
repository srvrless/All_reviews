from app.models import User


def test_new_user():
    user = User('maijor18@mail.ru', 'xxxxx')
    assert user.email_address == 'maijor18@mail.ru'
    assert user.password_hash != 'xxxxx'


def test_new_user_with_fixture(new_user):
    assert new_user.email == 'maijor18@mail.ru'
    assert new_user.hashed_password != 'xxxxx'
