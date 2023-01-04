from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from app import db
from app.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = db.session.query(User).filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = db.session.query(User).filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Login')


class AddBookForm(FlaskForm):
    title = StringField(label='Title:', validators=[Length(min=4, max=30), DataRequired()])
    description = StringField(label='Description:', validators=[Length(min=1, max=1024), DataRequired()])
    author = StringField(label='Author:', validators=[Length(min=2, max=40), DataRequired()])
    created_at = IntegerField(label='Book release year:', validators=[DataRequired()])
    submit = SubmitField(label='Add Book')


class AddFilmForm(FlaskForm):
    title = StringField(label='Title:', validators=[Length(min=4, max=30), DataRequired()])
    description = StringField(label='Description:', validators=[Length(min=1, max=1024), DataRequired()])
    producer = StringField(label='Producer:', validators=[Length(min=2, max=40), DataRequired()])
    created_at = IntegerField(label='Film release year:', validators=[DataRequired()])
    submit = SubmitField(label='Add Film')


class AddGameForm(FlaskForm):
    title = StringField(label='Title:', validators=[Length(min=4, max=30), DataRequired()])
    description = StringField(label='Description:', validators=[Length(min=1, max=1024), DataRequired()])
    studio = StringField(label='Studio:', validators=[Length(min=2, max=40), DataRequired()])
    created_at = IntegerField(label='Game release year:', validators=[DataRequired()])
    submit = SubmitField(label='Add Game')


class AddBookmark(FlaskForm):
    title = StringField(label='Title:', validators=[Length(min=4, max=30), DataRequired()])
    author = StringField(label='Author:', validators=[Length(min=2, max=40), DataRequired()])


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")
