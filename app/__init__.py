import logging
import os
import dotenv

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from app.models import Game, Book, Film

dotenv.load_dotenv()
db = SQLAlchemy()
path = os.environ['DATABASE_URL']
engine = create_engine(path, echo=True)


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()


def create_app():
    from .models import Base
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = path
    app.config["SECRET_KEY"] = "FesC9cBSuxakv9yN0vBY"
    migrate = Migrate(app, db)
    db.init_app(app)

    from .database import db_session, init_db
    init_db()
    db_session.commit()

    from .routes import main
    from .authentication import auth
    from .bookmarks import bookmark

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(bookmark)
    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    # Admin Dashboard
    admin = Admin(app, name='All reviews', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session, name='User'))
    admin.add_view(ModelView(Book, db.session, name='Book'))
    admin.add_view(ModelView(Game, db.session, name='Game'))
    admin.add_view(ModelView(Film, db.session, name='Film'))

    return app
