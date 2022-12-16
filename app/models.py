from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

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

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items


class Book(Base):
    __tablename__ = 'Book'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(1024), nullable=False)
    author = Column(String(30), nullable=False)
    created_at = Column(Integer(), nullable=False)


class Game(Base):
    __tablename__ = 'Game'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(1024), nullable=False)
    studio = Column(String(30), nullable=False)
    created_at = Column(Integer(), nullable=False)


class Films(Base):
    __tablename__ = 'Films'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(1024), nullable=False)
    producer = Column(String(30), nullable=False)
    created_at = Column(Integer(), nullable=False)
