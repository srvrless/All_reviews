from flask import render_template, Blueprint, redirect, url_for, flash, send_from_directory, request

from app import db
from app.forms import AddBookForm, AddFilmForm, AddGameForm, AddBookmark
from app.models import Book, Film, Game, Bookmark

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


@main.route("/film")
def films_page():
    film = db.session.query(Film).all()
    return render_template('public/film.html', film=film)


@main.route('/book/<int:book_id>/')
def book(book_id):
    book = db.session.query(Book).get_or_404(book_id)
    url = request.args.get('url')
    if url:
        bookmark = Bookmark(url=url)
        bookmark.fetch_image()
        db.session.add(bookmark)
        db.session.commit()
        return redirect(url)
    return render_template('public/includes/book_include.html', book=book)


@main.route('/add/Book', methods=['GET', 'POST'])
def add_Book():
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
            flash(f'There was an error with creating a Book: {err_msg}', category='danger')

    return render_template('admin/add_Book.html', form=form)


@main.route('/add/film', methods=['GET', 'POST'])
def add_film():
    form = AddFilmForm()
    if form.validate_on_submit():
        add_films = Film(title=form.title.data,
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

    return render_template('admin/create_Book.html', form=form)


@main.route('/uploads/<filename>')
def send_file(filename):
    from app import create_app
    return send_from_directory(create_app().config['UPLOAD_FOLDER'], filename)


@main.route('/bookmark', methods=['GET', 'POST'])
def bookmark_page():
    bookmarks = db.session.query(Bookmark).all()
    return render_template('public/bookmark.html', bookmarks=bookmarks)


@main.route('/bookmark/<id>/delete', methods=['GET', 'POST'])
def bookmark_delete_page(id):
    bookmark = get_object_or_404(Bookmark, id=id)
    bookmark.delete_instance()
    return redirect(url_for('bookmarks.list'))

@main.route('/bookmark/add', methods=['GET', 'POST'])
def bookmark_delete():
    form = AddBookmark()
    if form.validate_on_submit():
        bookmark = Bookmark(title=form.title.data,
                            author=form.author.data)
        db.session.add(bookmark)
        db.session.commit()
    return