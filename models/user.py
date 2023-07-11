import uuid

import sqlalchemy as db
from sqlalchemy.orm import relationship

from models import metadata, Base
from models.post import Post, posts_users


class User(Base):
    __tablename__ = 'users'
    metadata = metadata
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # relationships
    posts = relationship(Post, secondary=posts_users, back_populates='users')
