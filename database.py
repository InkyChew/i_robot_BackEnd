from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()
ma = Marshmallow()

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

# db.create_all()
# def initialize_sql():
# engine = "mysql+pymysql://"
engine = db.create_engine('mysql+pymysql://root@localhost/stockai', {})
DBSession.configure(bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)
