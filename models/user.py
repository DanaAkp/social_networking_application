import uuid
import sqlalchemy as db

from models import metadata, Base


class User(Base):
    __tablename__ = 'users'
    metadata = metadata
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
