import json

from flask import render_template, Blueprint, redirect, url_for, flash, send_from_directory, request
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
    if form.validate_on_submit():
        # Get data from submitted form
        # author = request.form["author"]
        searched = form.searched.data
        # search = "%{}%".format(searched)
        # book = db.session.query(Book).filter(Book.author.like(search)).all()
        # # Query the Database
        books = db.session.query(Book).filter(Book.title.like('%' + searched + '%'))
        books = books.order_by(Book.title).all()
        return render_template("public/search.html", form=form, searched=searched, books=books)
@main.route('/modern', methods=['GET', 'POST'])
def modern():
    return render_template('public/modern.html')

@main.route('/rate_movie', methods=['GET', 'POST'])
def rate_movie():

    #
    # if request.method == 'POST':
    #     data = request.get_json(force=True)
    #     rating = data['rating']
    #     id = data['id']
    #
    #     # Execute
    #     # cursor.execute("UPDATE favourites SET rating=5  WHERE id =49") ## Works
    #     # cursor.execute("UPDATE favourites SET rating=%s  WHERE id =%s", (rating, id))
    #     # # ("INSERT INTO favourites(rating)VALUES(%s) WHERE id =%s" ,(rating,id))
    #     # # Commit to DB
    #     # cnx.commit()
    #     #
    #     # # Close connection
    #     # cursor.close()
    with open('ratings_so_far.json') as f:
        ratingstore = json.load(f)
    if request.method == 'POST':
        five_stars = int(ratingstore['five_stars'])
        four_stars = int(ratingstore['four_stars'])
        three_stars = int(ratingstore['three_stars'])
        two_stars = int(ratingstore['two_stars'])
        one_star = int(ratingstore['one_star'])
        count = int(ratingstore['count'])
        rating = float(ratingstore['rating'])
        total = int(ratingstore['total'])
        if 'rating' in request.form:
            content = int(request.form['rating'])
            if content:
                if content == 5:
                    five_stars += 1
                elif content == 4:
                    four_stars += 1
                elif content == 3:
                    three_stars += 1
                elif content == 2:
                    two_stars += 1
                elif content == 1:
                    one_star += 1
                count += 1
                total += content
                rating = float('{0:.1f}'.format(total / count))
        ratingstore['five_stars'] = str(five_stars)
        ratingstore['four_stars'] = str(four_stars)
        ratingstore['three_stars'] = str(three_stars)
        ratingstore['two_stars'] = str(two_stars)
        ratingstore['one_star'] = str(one_star)
        ratingstore['count'] = str(count)
        ratingstore['total'] = str(total)
        ratingstore['rating'] = str(rating)
        with open('ratings_so_far.json', 'w') as f:
            json.dump(ratingstore, f, indent=2)
    return render_template('public/rate.html', five_stars=ratingstore['five_stars'],
                           four_stars=ratingstore['four_stars'], three_stars=ratingstore['three_stars'],
                           two_stars=ratingstore['two_stars'], one_star=ratingstore['one_star'],
                           count=ratingstore['count'], rating=ratingstore['rating'])
