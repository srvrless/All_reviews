from flask import render_template, Blueprint, redirect, url_for, flash
from app.forms import AddBookForm, AddFilmForm, AddGameForm
from app.models import Book, Films, Game
from app import db

main = Blueprint("main", __name__)


@main.route('/')
@main.route("/home", methods=['GET', 'POST'])
# @login_required
def home_page():
    return render_template('public/Base.html')


@main.route("/games")
def games_page():
    return render_template('public/games.html')


@main.route("/books")
def books_page():
    return render_template('public/books.html')


@main.route("/films")
def films_page():
    return render_template('public/films.html')


@main.route('/add/book', methods=['GET', 'POST'])
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        Book_create = Book(title=form.title.data,
                           description=form.description.data,
                           author=form.author.data,
                           created_at=form.created_at.data)

        db.session.add(Book_create)
        db.session.commit()

        flash('Successfully create a Book!', category='success')
        return redirect(url_for('main.home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a book: {err_msg}', category='danger')

    return render_template('admin/add_book.html', form=form)


@main.route('/add/film', methods=['GET', 'POST'])
def add_film():
    form = AddFilmForm()
    if form.validate_on_submit():
        add_films = Films(title=form.title.data,
                          description=form.description.data,
                          producer=form.producer.data,
                          created_at=form.created_at.data)

        db.session.add(add_films)
        db.session.commit()

        flash('Successfully add a new films!', category='success')
        return redirect(url_for('main.home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a Film: {err_msg}', category='danger')

    return render_template('admin/add_film.html', form=form)


@main.route('/create/', methods=['GET', 'POST'])
def add_game():
    form = AddGameForm()
    if form.validate_on_submit():
        add_game = Game(title=form.title.data,
                        description=form.description.data,
                        studio=form.studio.data,
                        created_at=form.created_at.data)

        db.session.add(add_game)
        db.session.commit()

        flash('Successfully add a new Game!', category='success')
        return redirect(url_for('main.home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a Game: {err_msg}', category='danger')

    return render_template('admin/create_book.html', form=form)
