from flask import render_template, Blueprint, flash, send_from_directory, request
from flask_login import current_user, login_required

from app import db
from app.forms import SearchForm, ReviewFieldForm, RegisterForm
from app.models import Book, Film, Game, User, RatingBook, RatingFilm, RatingGame

main = Blueprint("main", __name__)


@main.route('/')
@main.route("/welcome")
def welcome_page():
    return render_template('public/welcome.html')


@main.route("/all_reviews", methods=['GET', 'POST'])
def home_page():
    return render_template('public/all_reviews.html')

# main screen page category


@main.route("/games")
def games_page():
    games = db.session.query(Game).all()
    return render_template('public/game.html', games=games)

# main screen page category


@main.route("/books")
def books_page():
    books = db.session.query(Book).all()
    return render_template('public/book.html', books=books)

# main screen page category


@main.route("/films")
def films_page():
    films = db.session.query(Film).all()
    return render_template('public/film.html', films=films)

# More about the book


@main.route('/book/<int:book_id>/', methods=['GET', 'POST'])
def book(book_id):
    book = db.session.query(Book).get_or_404(book_id)
    # get all book reviews
    ratingbooks = db.session.query(RatingBook).all()
    form = ReviewFieldForm()
    if form.validate_on_submit():
        review = RatingBook(review=form.description_review.data,
                            rating=form.rating.data)
        db.session.add(review)
        db.session.commit()
        flash(f"Review created!", category='success')
    return render_template('public/includes/book_include.html', book=book, form=form, ratingbooks=ratingbooks)

# More about the film


@main.route('/film/<int:film_id>/')
def film(film_id):
    film = db.session.query(Film).get_or_404(film_id)
    # get all film reviews
    ratingfilms = db.session.query(RatingFilm).all()
    form = ReviewFieldForm()
    if form.validate_on_submit():
        review = RatingFilm(review=form.description_review.data,
                            rating=form.rating.data)
        db.session.add(review)
        db.session.commit()
        flash(f"Review created!", category='success')
    return render_template('public/includes/film_include.html', film=film, form=form, ratingfilms=ratingfilms)

# More about the game


@main.route('/game/<int:game_id>/')
def game(game_id):
    game = db.session.query(Game).get_or_404(game_id)
    # get all game reviews
    ratinggames = db.session.query(RatingFilm).all()
    form = ReviewFieldForm()
    if form.validate_on_submit():
        review = RatingGame(review=form.description_review.data,
                            rating=form.rating.data)
        db.session.add(review)
        db.session.commit()
        flash(f"Review created!", category='success')
    return render_template('public/includes/game_include.html', game=game, form=form, ratinggames=ratinggames)


# idk
@main.route('/uploads/<filename>')
def send_file(filename):
    from app import create_app
    return send_from_directory(create_app().config['UPLOAD_FOLDER'], filename)


# idk
@main.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched = form.searched.data
        books = db.session.query(Book).filter(
            Book.title.like('%' + searched + '%'))
        books = books.order_by(Book.title).all()
        return render_template("public/search.html", form=form, searched=searched, books=books)


@main.route('/profile', methods=['GET', 'POST'])
def profile_page():
    profile = db.session.query(User).all()
    return render_template('public/profile.html', profile=profile)


# Invalid Url
@main.errorhandler(404)
def page_not_found(error):
    return render_template('public/404.html'), 404


# Update username and email
@main.route('/profile_update', methods=['GET', 'POST'])
def profile_update_page():
    form = RegisterForm()
    name_to_update = db.session.query(User).get_or_404(id)
    if form.validate_on_submit():
        db.session.merge(name_to_update)
    return render_template("public/update_profile.html", form=form)
