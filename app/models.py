from datetime import datetime

from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, DateTime, func
from flask_login import UserMixin
from wtforms import DateTimeField

app = Flask(__name__)
bcrypt = Bcrypt(app)
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'User'
    id = Column(Integer(), primary_key=True)
    username = Column(String(length=30), nullable=False, unique=True)
    email_address = Column(String(length=50), nullable=False, unique=True)
    password_hash = Column(String(length=60), nullable=False)

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


class Bookmark(Base):
    __tablename__ = 'Bookmark'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(Text(), nullable=False)
    created_date = DateTimeField(default=datetime.now)
# class Rating_For_Books(Base):
#     __tablename__ = 'Star_Rating_Books'
#     # product_id = Column(ForeignKey(Film))
#     product_id = Column(Integer(), nullable=False)
#     user_id = Column(Integer(), nullable=False)
#     rating = Column(Integer(), nullable=False, default=1, primary_key=('product_id', 'user_id'))
#
# class Rating_For_Games(Base):
#     __tablename__ = 'Star_Rating_Games'
#     product_id = Column(Integer(), nullable=False)
#     user_id = Column(Integer(), nullable=False)
#     rating = Column(Integer(), nullable=False, default=1, primary_key=('product_id', 'user_id'))
#
#
# class Rating_For_Films(Base):
#     __tablename__ = 'Star_Rating_Films'
#     product_id = Column(Integer(), nullable=False)
#     user_id = Column(Integer(), nullable=False)
#     rating = Column(Integer(), nullable=False, default=1, primary_key=('product_id', 'user_id'))
