from flask import request, render_template, Blueprint, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app.forms import RegisterForm, AddBookForm, LoginForm
from app.models import User, Book, bcrypt
from app import db

main = Blueprint("main", __name__)


@main.route('/')
@main.route("/home", methods=['GET', 'POST'])
@login_required
def home_page():
    return render_template('public/Base.html')


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


@main.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash(f'You are logged in', category='success')
                return redirect(url_for('main.home_page'))
        flash(f'There was an error with login a user: Wrong username or password', category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with login a user: {err_msg}', category='danger')
    return render_template('public/login.html', form=form)


@main.route("/games")
def games_page():
    return render_template('public/games.html')


@main.route("/books")
def books_page():
    return render_template('public/books.html')


@main.route("/films")
def films_page():
    return render_template('public/films.html')


@main.route('/create/', methods=['GET', 'POST'])
def add_book():
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
            flash(f'There was an error with creating a book: {err_msg}', category='danger')

    return render_template('admin/create_book.html', form=form)


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login_page'))
