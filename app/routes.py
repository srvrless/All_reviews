from flask import render_template, Blueprint, redirect, url_for, flash, send_from_directory, request
from flask_login import current_user
from flask_peewee.utils import get_object_or_404

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


@main.route('/bookmark_books', methods=['GET', 'POST'])
def bookmark_books():
    if current_user:
        owner_id = current_user.id
        bookmarks = db.session.query(Bookmark).filter_by(owner=owner_id, book=Bookmark.book).all()
        return render_template('public/bookmark_book.html', bookmarks=bookmarks)


@main.route('/bookmark_games', methods=['GET', 'POST'])
def bookmark_games():
    if current_user:
        owner_id = current_user.id
        bookmarks = db.session.query(Bookmark).filter_by(owner=owner_id, game=Bookmark.game).all()
        return render_template('public/bookmark_game.html', bookmarks=bookmarks)


@main.route('/bookmark_films', methods=['GET', 'POST'])
def bookmark_films():
    if current_user:
        owner_id = current_user.id
        bookmarks = db.session.query(Bookmark).filter_by(owner=owner_id, film=Bookmark.film).all()
        return render_template('public/bookmark_film.html', bookmarks=bookmarks)


@main.route('/bookmark/<int:id>/', methods=['GET', 'POST'])
def bookmark_delete(id):
    bookmark_del = db.session.query(Bookmark).filter_by(owner=id).first()
    db.session.delete(bookmark_del)
    db.session.commit()
    return redirect(url_for('main.bookmark_books', owner=id))


@main.route('/bookmark_book/<int:id>/<string:title>/<string:author>/', methods=['GET', 'POST'])
def bookmark_add_book(id, title, author):
    bookmark = Bookmark(title=title, author=author, owner=current_user.id, book=id)
    db.session.add(bookmark)
    db.session.commit()
    return redirect(url_for('main.bookmark_books'))


@main.route('/bookmark_film/<int:id>/<string:title>/<string:author>/', methods=['GET', 'POST'])
def bookmark_add_film(id, title, author):
    bookmark = Bookmark(title=title, author=author, owner=current_user.id, film=id)
    db.session.add(bookmark)
    db.session.commit()
    return redirect(url_for('main.bookmark_books'))


@main.route('/bookmark_game/<int:id>/<string:title>/<string:author>/', methods=['GET', 'POST'])
def bookmark_add_game(id, title, author):
    bookmark = Bookmark(title=title, author=author, owner=current_user.id, game=id)
    db.session.add(bookmark)
    db.session.commit()
    return redirect(url_for('main.bookmark_books'))


@main.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        posts = Book.query
        if form.validate_on_submit():
            # Get data from submitted form
            book.searched = form.searched.data
            # Query the Database
            posts = posts.filter(Book.content.like('%' + Book.searched + '%'))
            posts = posts.order_by(Book.title).all()

            return render_template("public/search.html",
                                   form=form,
                                   searched=book.searched,
                                   posts=posts)
