from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DB_URL
from app.reposiroty import RepositoryPostgres

engine = create_engine(DB_URL)
metadata = MetaData()

Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


from app.models.user import User
from app.models.post import Post

repo = RepositoryPostgres(session=session)
