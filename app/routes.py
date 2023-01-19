from flask import render_template, Blueprint, flash, send_from_directory

from app import db
from app.forms import SearchForm, ReviewFieldForm
from app.models import Book, Film, Game, User, RatingBook, RatingFilm

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
    form = ReviewFieldForm()
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
    ratingfilms = db.session.query(RatingFilm).all()
    form = ReviewFieldForm()
    if form.validate_on_submit():
        review = RatingFilm(review=form.description_review.data,
                            rating=form.rating.data)
        db.session.add(review)
        db.session.commit()
        flash(f"Review created!", category='success')
    return render_template('public/includes/film_include.html', film=film, form=form, ratingfilms=ratingfilms)


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


@main.route('/profile', methods=['GET', 'POST'])
def profile_page():
    profile = db.session.query(User).all()
    return render_template('public/profile.html', profile=profile)


# Invalid Url
@main.errorhandler(404)
def page_not_found(error):
    return render_template('public/404.html'), 404
# @main.route('/profile_update', methods=['GET', 'POST'])
# def profile_update_page():
#     form = RegisterForm()
#     id = current_user.id
#     name_to_update = db.session.query(User).get_or_404(id)
#     if request.method == "POST":
#         name_to_update.email_address = request.form['email_address']
#         name_to_update.username = request.form['username']
#
#         # Check for profile pic
#         if request.files['profile_pic']:
#             name_to_update.profile_pic = request.files['profile_pic']
#
#             # Grab Image Name
#             pic_filename = secure_filename(name_to_update.profile_pic.filename)
#             # Set UUID
#             pic_name = str(uuid.uuid1()) + "_" + pic_filename
#             # Save That Image
#             saver = request.files['profile_pic']
#
#             # Change it to a string to save to db
#             name_to_update.profile_pic = pic_name
#             try:
#                 db.session.commit()
#                 saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
#                 flash("User Updated Successfully!")
#                 return render_template("public/update_profile.html",
#                                        form=form,
#                                        name_to_update=name_to_update)
#             except:
#                 flash("Error!  Looks like there was a problem...try again!")
#                 return render_template("public/update_profile.html",
#                                        form=form,
#                                        name_to_update=name_to_update)
#         else:
#             db.session.commit()
#             flash("User Updated Successfully!")
#             return render_template("public/update_profile.html",
#                                    form=form,
#                                    name_to_update=name_to_update)
#     else:
#         return render_template("public/update_profile.html",
#                                form=form,
#                                name_to_update=name_to_update,
#                                id=id)
