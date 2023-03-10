from flask_login import current_user
from flask import render_template, redirect, url_for, Blueprint, flash
from marshmallow import ValidationError

from app import db
from app.models import Bookmark

bookmark = Blueprint("bookmark", __name__)


@bookmark.route('/bookmark_book', methods=['GET', 'POST'])
def books():  # main page bookmarks
    if current_user:
        owner_id = current_user.id
        bookmarks = db.session.query(Bookmark).filter_by(
            owner=owner_id, book=Bookmark.book).all()
        return render_template('public/bookmark_book.html', bookmarks=bookmarks)


@bookmark.route('/bookmark_games', methods=['GET', 'POST'])
def games():
    if current_user:
        owner_id = current_user.id
        bookmarks = db.session.query(Bookmark).filter_by(
            owner=owner_id, game=Bookmark.game).all()
        return render_template('public/bookmark_game.html', bookmarks=bookmarks)


@bookmark.route('/bookmark_films', methods=['GET', 'POST'])
def films():
    if current_user:
        owner_id = current_user.id
        bookmarks = db.session.query(Bookmark).filter_by(
            owner=owner_id, film=Bookmark.film).all()
        return render_template('public/bookmark_film.html', bookmarks=bookmarks)


@bookmark.route('/bookmark_book/<int:id>/<int:book_id>/', methods=['GET', 'POST'])
def delete_book(id, book_id):
    bookmark_del = db.session.query(Bookmark).filter_by(owner=id,
                                                        book=book_id).first()  # if owner == current owner id and book == book on page
    db.session.delete(bookmark_del)
    db.session.commit()
    return redirect(url_for('bookmark.books', owner=id, book=book_id))


@bookmark.route('/bookmark_game/<int:id>/<int:game_id>/', methods=['GET', 'POST'])
def delete_game(id, game_id):
    bookmark_del = db.session.query(Bookmark).filter_by(
        owner=id, game=game_id).first()
    db.session.delete(bookmark_del)
    db.session.commit()
    return redirect(url_for('bookmark.games', owner=id, game=game_id))


@bookmark.route('/bookmark_film/<int:id>/<int:film_id>/', methods=['GET', 'POST'])
def delete_film(id, film_id):
    bookmark_del = db.session.query(Bookmark).filter_by(
        owner=id, film=film_id).first()
    db.session.delete(bookmark_del)
    db.session.commit()
    return redirect(url_for('bookmark.films', owner=id, film=film_id))


@bookmark.route('/bookmark_book/<int:id>/<string:title>/<string:author>/', methods=['GET', 'POST'])
def add_book(id, title, author):
    book = db.session.query(Bookmark).filter_by(book=id).first()
    if not book:
        bookmark = Bookmark(title=title, author=author,
                            owner=current_user.id, book=id)
        db.session.add(bookmark)
        db.session.commit()
        flash(f'Bookmark create!', category='success')
        return redirect(url_for('bookmark.books'))
    flash(f'Bookmark is  already exist', category='danger')
    return redirect(url_for('main.films_page'))


@bookmark.route('/bookmark_film/<int:id>/<string:title>/<string:author>/', methods=['GET', 'POST'])
def add_film(id, title, author):
    film = db.session.query(Bookmark).filter_by(film=id).first()
    if not film:
        bookmark = Bookmark(title=title, author=author,
                            owner=current_user.id, film=id)
        db.session.add(bookmark)
        db.session.commit()
        flash(f'Bookmark create!', category='success')
        return redirect(url_for('bookmark.books'))
    flash(f'Bookmark is  already exist', category='danger')
    return redirect(url_for('main.films_page'))


@bookmark.route('/bookmark_game/<int:id>/<string:title>/<string:author>/', methods=['GET', 'POST'])
def add_game(id, title, author):
    game = db.session.query(Bookmark).filter_by(game=id).first()
    if not game:
        bookmark = Bookmark(title=title, author=author,
                            owner=current_user.id, game=id)
        db.session.add(bookmark)
        db.session.commit()
        flash(f'Bookmark create!', category='success')
        return redirect(url_for('bookmark.books'))
    flash(f'Bookmark is  already exist', category='danger')
    return redirect(url_for('main.games_page'))
