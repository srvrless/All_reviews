import json
import os
import uuid as uuid

from flask import render_template, Blueprint, redirect, url_for, flash, send_from_directory, request
from flask_login import current_user
from werkzeug.utils import secure_filename

from app import db
from app.forms import AddBookForm, AddFilmForm, AddGameForm, AddBookmark, SearchForm, ReviewBook, RegisterForm
from app.models import Book, Film, Game, Bookmark, User, RatingBook, app

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


@main.route('/book/<int:book_id>/', methods=['GET', 'POST'])
def book(book_id):
    book = db.session.query(Book).get_or_404(book_id)
    ratingbooks = db.session.query(RatingBook).all()
    form = ReviewBook()
    if form.validate_on_submit():
        review = RatingBook(review=form.description_review.data,
                            rating=form.rating.data)
        db.session.add(review)
        db.session.commit()
        flash(f"Review created!", category='success')
    return render_template('public/includes/book_include.html', book=book, form=form, ratingbooks=ratingbooks)


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


# @main.route('/rate_movie', methods=['GET', 'POST'])
# def rate_movie():
#     with open('ratings_so_far.json') as f:
#         ratingstore = json.load(f)
#     if request.method == 'POST':
#         five_stars = int(ratingstore['five_stars'])
#         four_stars = int(ratingstore['four_stars'])
#         three_stars = int(ratingstore['three_stars'])
#         two_stars = int(ratingstore['two_stars'])
#         one_star = int(ratingstore['one_star'])
#         count = int(ratingstore['count'])
#         rating = float(ratingstore['rating'])
#         total = int(ratingstore['total'])
#         if 'rating' in request.form:
#             content = int(request.form['rating'])
#             if content:
#                 if content == 5:
#                     five_stars += 1
#                 elif content == 4:
#                     four_stars += 1
#                 elif content == 3:
#                     three_stars += 1
#                 elif content == 2:
#                     two_stars += 1
#                 elif content == 1:
#                     one_star += 1
#                 count += 1
#                 total += content
#                 rating = float('{0:.1f}'.format(total / count))
#         ratingstore['five_stars'] = str(five_stars)
#         ratingstore['four_stars'] = str(four_stars)
#         ratingstore['three_stars'] = str(three_stars)
#         ratingstore['two_stars'] = str(two_stars)
#         ratingstore['one_star'] = str(one_star)
#         ratingstore['count'] = str(count)
#         ratingstore['total'] = str(total)
#         ratingstore['rating'] = str(rating)
#         with open('ratings_so_far.json', 'w') as f:
#             json.dump(ratingstore, f, indent=2)
#     return render_template('public/rate.html', five_stars=ratingstore['five_stars'],
#                            four_stars=ratingstore['four_stars'], three_stars=ratingstore['three_stars'],
#                            two_stars=ratingstore['two_stars'], one_star=ratingstore['one_star'],
#                            count=ratingstore['count'], rating=ratingstore['rating'])

@main.route('/profile', methods=['GET', 'POST'])
def profile_page():
    profile = db.session.query(User).all()
    return render_template('public/profile.html', profile=profile)


@main.route('/profile_update', methods=['GET', 'POST'])
def profile_update_page():
    form = RegisterForm()
    id = current_user.id
    name_to_update = db.session.query(User).get_or_404(id)
    if request.method == "POST":
        name_to_update.email_address = request.form['email_address']
        name_to_update.username = request.form['username']

        # Check for profile pic
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']

            # Grab Image Name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save That Image
            saver = request.files['profile_pic']

            # Change it to a string to save to db
            name_to_update.profile_pic = pic_name
            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully!")
                return render_template("public/update_profile.html",
                                       form=form,
                                       name_to_update=name_to_update)
            except:
                flash("Error!  Looks like there was a problem...try again!")
                return render_template("public/update_profile.html",
                                       form=form,
                                       name_to_update=name_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("public/update_profile.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template("public/update_profile.html",
                               form=form,
                               name_to_update=name_to_update,
                               id=id)
