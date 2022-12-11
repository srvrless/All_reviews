import os
import dotenv

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

dotenv.load_dotenv()
db = SQLAlchemy()
path = os.environ['DATABASE_URL']
engine = create_engine(path, echo=True)


def create_app():
    from .models import Base
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = path
    app.config["SECRET_KEY"] = "FesC9cBSuxakv9yN0vBY"

    db.init_app(app)
    from .database import db_session, init_db
    init_db()

    db_session.commit()
    from .routes import main

    app.register_blueprint(main)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/'
    bcrypt = Bcrypt(app)
    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return db.session.query(User).all()

    return app


from app import models
