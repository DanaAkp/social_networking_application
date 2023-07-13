import uuid
from datetime import datetime

import sqlalchemy as db

from models import metadata, Base


class RatePosts(Base):
    __tablename__ = "rate_posts"
    metadata = metadata
    user_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    post_id = db.Column(db.ForeignKey("posts.id"), primary_key=True)
    is_like = db.Column(db.Boolean)


class Post(Base):
    __tablename__ = 'posts'
    metadata = metadata
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modify_time = db.Column(db.DateTime)
