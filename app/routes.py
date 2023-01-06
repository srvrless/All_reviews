from flask import render_template, Blueprint, redirect, url_for, flash, send_from_directory, request
from flask_login import current_user


from app import db
from app.forms import AddBookForm, AddFilmForm, AddGameForm, AddBookmark, SearchForm
from app.models import Book, Film, Game, Bookmark, User

main = Blueprint("main", __name__)


@main.route('/')
@main.route("/welcome")
def welcome_page():
    return render_template('public/welcome.html')


@main.route("/all_reviews", methods=['GET', 'POST'])
# @login_required
def home_page():
    return render_template('public/all_reviews.html')


@main.route("/games")
def games_page():
    games = db.session.query(Game).all()
    return render_template('public/game.html', games=games)


@main.route("/books")
def books_page():
    books = db.session.query(Book).all()
    return render_template('public/book.html', books=books)


@main.route("/films")
def films_page():
    films = db.session.query(Film).all()
    return render_template('public/film.html', films=films)


@main.route('/book/<int:book_id>/')
def book(book_id):
    book = db.session.query(Book).get_or_404(book_id)
    return render_template('public/includes/book_include.html', book=book)


@main.route('/film/<int:film_id>/')
def film(film_id):
    film = db.session.query(Film).get_or_404(film_id)
    return render_template('public/includes/film_include.html', film=film)


@main.route('/game/<int:game_id>/')
def game(game_id):
    game = db.session.query(Game).get_or_404(game_id)
    return render_template('public/includes/game_include.html', game=game)


@main.route('/uploads/<filename>')
def send_file(filename):
    from app import create_app
    return send_from_directory(create_app().config['UPLOAD_FOLDER'], filename)

@main.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    posts = db.session.query(Book)
    if form.validate_on_submit():
        # Get data from submitted form
        book_searched = form.searched.data
        # Query the Database
        posts = posts.filter(Book.title.like('%' + book_searched + '%')).all()
        # posts = posts.order_by(Book.title).all()

        return render_template("public/search.html",
                               form=form,
                               searched=book_searched,
                               posts=posts)
