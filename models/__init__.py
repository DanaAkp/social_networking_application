from sqlalchemy import create_engine, MetaData
from config import DB_URL

engine = create_engine(DB_URL)
connection = engine.connect()
metadata = MetaData()
