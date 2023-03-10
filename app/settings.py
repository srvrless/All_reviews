import os

import dotenv

dotenv.load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'FesC9cBSuxakv9yN0vBY'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    ADMIN_PASSWD_SALT = ''


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
