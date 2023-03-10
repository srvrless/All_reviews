from app import models
from sqlalchemy.orm import scoped_session, sessionmaker

from app import engine

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
models.Base.query = db_session.query_property()


def init_db():
    models.Base.metadata.create_all(bind=engine)
