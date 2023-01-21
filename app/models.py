from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func, Table
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from wtforms import DateTimeField

from app.settings import Config

app = Flask(__name__)
bcrypt = Bcrypt(app)
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'User'
    id = Column(Integer(), primary_key=True)
    username = Column(String(length=30), nullable=False, unique=True)
    email_address = Column(String(length=50), nullable=False, unique=True)
    date_added = Column(DateTime(timezone=True),
                        server_default=func.now())
    password_hash = Column(String(length=60), nullable=False)
    profile_pic = Column(String(50), nullable=False, default='default.png')
    bookmark = relationship('Bookmark', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Book(Base):
    __tablename__ = 'Book'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(Text(), nullable=False)
    author = Column(String(30), nullable=False)
    cover = Column(String(50), nullable=False, default='default.png')
    rating = Column(Integer(), nullable=False, default=0)
    created_at = Column(Integer(), nullable=False)
    recently_edit = Column(DateTime(timezone=True),
                           server_default=func.now())
    bookmark = relationship('Bookmark', backref='owned_book', lazy=True)
    book_rating = relationship('RatingBook', backref='book_rating', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'


class Game(Base):
    __tablename__ = 'Game'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(Text(), nullable=False)
    studio = Column(String(30), nullable=False)
    cover = Column(String(50), nullable=False, default='default.png')
    rating = Column(Integer(), nullable=False, default=0)
    created_at = Column(Integer(), nullable=False)
    recently_edit = Column(DateTime(timezone=True),
                           server_default=func.now())
    bookmark = relationship('Bookmark', backref='owned_game', lazy=True)
    game_rating = relationship('RatingGame', backref='game_rating', lazy=True)


class Film(Base):
    __tablename__ = 'Film'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(Text(), nullable=False)
    producer = Column(String(30), nullable=False)
    cover = Column(String(50), nullable=False, default='default.png')
    rating = Column(Integer(), nullable=False, default=0)
    created_at = Column(Integer(), nullable=False)
    recently_edit = Column(DateTime(timezone=True),
                           server_default=func.now())
    bookmark = relationship('Bookmark', backref='owned_film', lazy=True)
    film_rating = relationship('RatingFilm', backref='film_rating', lazy=True)


class Bookmark(Base):
    __tablename__ = 'Bookmark'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(Text(), nullable=False)
    created_date = DateTimeField(default=datetime.now)
    owner = Column(Integer(), ForeignKey('User.id'))
    book = Column(Integer(), ForeignKey('Book.id'))
    game = Column(Integer(), ForeignKey('Game.id'))
    film = Column(Integer(), ForeignKey('Film.id'))


class RatingGame(Base):
    __tablename__ = 'RatingGame'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    rating = Column(Integer(), nullable=False)
    created_date = DateTimeField(default=datetime.now)
    review = Column(String(5000), nullable=True)
    owner = Column(Integer(), ForeignKey('User.id'))
    game_id = Column(Integer(), ForeignKey('Game.id'))


class RatingFilm(Base):
    __tablename__ = 'RatingFilm'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    review = Column(String(5000), nullable=True)
    rating = Column(Integer(), nullable=False)
    recently_edit = Column(DateTime(timezone=True),
                           server_default=func.now())
    owner = Column(Integer(), ForeignKey('User.id'))
    film_id = Column(Integer(), ForeignKey('Film.id'))


class RatingBook(Base):
    __tablename__ = 'RatingBook'
    id = Column(Integer(), primary_key=True)
    review = Column(String(5000), nullable=True)
    rating = Column(Integer(), nullable=False)
    recently_edit = Column(DateTime(timezone=True),
                           server_default=func.now())
    owner = Column(String(), ForeignKey('User.username'))
    book_id = Column(Integer(), ForeignKey('Book.id'))


association = Table('association', Base.metadata,
                    Column('admin_id', Integer,
                           ForeignKey('admins.id')),
                    Column('role_id', Integer,
                           ForeignKey('roles.id'))
                    )


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    roles = relationship('Role', secondary=association,
                         back_populates='admins', lazy=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(
            kwargs.get('password'),
            salt=Config.ADMIN_PASSWD_SALT
        )

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500), nullable=False)
    admins = relationship('Admin', secondary=association,
                          back_populates='roles', lazy=True)
