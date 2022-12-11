from flask import request, render_template, Blueprint, redirect, url_for, flash
from flask_login import login_user
from app.forms import RegisterForm, AddBookForm
from app.models import User, Book
from app import db

main = Blueprint("main", __name__)


@main.route('/')
@main.route("/home")
def home_page():
    return render_template('public/home.html')


@main.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('main.home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('public/register.html', form=form)


@main.route("/games")
def games_reviews():
    return "<p>Games, coming soon...</p>"


@main.route("/films")
def films_reviews():
    return "<p>Films, coming soon...</p>"


@main.route('/create/', methods=('GET', 'POST'))
def create():
    form = AddBookForm()
    if form.validate_on_submit():
        Book_create = Book(title=form.title.data,
                           description=form.description.data,
                           author=form.author.data,
                           created_at=form.created_at.data)

        db.session.add(Book_create)
        db.session.commit()

        flash('Successfully create a Book!')
        return redirect(url_for('main.home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('public/create_book.html', form=form)
