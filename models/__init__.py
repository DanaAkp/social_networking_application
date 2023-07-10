from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase
from config import DB_URL

engine = create_engine(DB_URL)
connection = engine.connect()
metadata = MetaData()


class Base(DeclarativeBase):
    pass
