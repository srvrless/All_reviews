# import pytest
# from marshmallow import ValidationError
# from app.models import User
#
#
# @pytest.mark.parametrize(
#     "password_hash,valid",
#     [
#         ("poxiton", True),
#         ("poxiton", True),
#         ("poxiton", True),
#         ("abcde12345", False),
#         ("ABCDE12345", False),
#         ("12345678", False),
#         ("Abc123", False),
#     ]
# )
# def test_validate_password(password, valid):
#     # given
#     schema = User()
#     data = {
#         "username": "poxiton",
#         "password_hash": password,
#         "email_address": "maijor18@mail.ru"
#     }
#
#     # when
#     try:
#         user = schema.load(data)
#         assert valid
#
#         # then
#         assert user is not None
#         assert user.username == data["username"]
#         assert user.password_hash == password
#         assert user.email_address == data["email"]
#     except ValidationError:
#         assert not valid
#
#
# @pytest.mark.parametrize(
#     "email,valid",
#     [
#         ("sergio@sergio.com", True),
#         ("sergio@mail.fr", True),
#         ("sergio.lema@mail.fr", True),
#         ("sergio.lema@mail.mail.fr", True),
#         ("sergio@mail", False),
#         ("sergio.mail.com", False),
#         ("sergio@mail@com", False),
#     ]
# )
# def test_validate_email(email, valid):
#     # given
#     schema = User()
#     data = {
#         "username": "sergio",
#         "password_hash": "Abcde12345",
#         "email": email
#     }
#
#     # when
#     try:
#         user = schema.load(data)
#         assert valid
#
#         # then
#         assert user is not None
#         assert user.username == data["username"]
#         assert user.password_hash == data["password_hash"]
#         assert user.email_address == email
#     except ValidationError:
#         assert not valid
#
#
# def test_missing_fields():
#     # given
#     schema = User()
#     data = {
#         "username": "poxiton",
#         "password_hash": "poxiton",
#     }
#
#     # when / then
#     import pytest
#     with pytest.raises(ValidationError):
#         schema.load(data)
#
#
# @pytest.mark.parametrize(
#     "password_hash,valid",
#     [
#         ("poxiton", True),
#         ("poxiton", True),
#         ("poxiton", True),
#         ("abcde12345", False),
#         ("ABCDE12345", False),
#         ("12345678", False),
#         ("Abc123", False),
#     ]
# )
# def test_validate_password(password, valid):
#     # given
#     schema = User()
#     data = {
#         "username": "poxiton",
#         "password": password,
#         "email": "maijor18@mail.ru"
#     }
#
#     # when
#     try:
#         user = schema.load(data)
#         assert valid
#
#         # then
#         assert user is not None
#         assert user.username == data["username"]
#         assert user.password == password
#         assert user.email_address == data["email"]
#     except ValidationError:
#         assert not valid
#
#
# @pytest.mark.parametrize(
#     "email,valid",
#     [
#         ("maijor18@sergio.com", True),
#         ("maijor18@mail.fr", True),
#         ("maijor18.lema@mail.fr", True),
#         ("maijor18.lema@mail.mail.fr", True),
#         ("maijor18@mail", False),
#         ("maijor18.mail.com", False),
#         ("maijor18@mail@com", False),
#     ]
# )
# def test_validate_email(email, valid):
#     # given
#     schema = User()
#     data = {
#         "username": "poxiton",
#         "password_hash": "poxiton",
#         "email": email
#     }
#
#     # when
#     try:
#         user = schema.load(data)
#         assert valid
#
#         # then
#         assert user is not None
#         assert user.username == data["username"]
#         assert user.password_hash == data["password_hash"]
#         assert user.email == email
#     except ValidationError:
#         assert not valid
#
#
# def test_missing_field():
#     # given
#     schema = User()
#     data = {
#         "username": "poxiton",
#         "password_hash": "poxiton",
#     }
#
#     # when / then
#     with pytest.raises(ValidationError):
#         schema.load(data)
