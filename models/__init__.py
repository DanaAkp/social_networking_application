from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import DB_URL

engine = create_engine(DB_URL)
connection = engine.connect()
metadata = MetaData()

Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass
