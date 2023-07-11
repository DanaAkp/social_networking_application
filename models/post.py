import uuid

import sqlalchemy as db
from sqlalchemy.orm import relationship

from models import metadata, Base

posts_users = db.Table(
    "posts_users",
    metadata,
    db.Column("user_id", db.ForeignKey("users.id"), primary_key=True),
    db.Column("post_id", db.ForeignKey("posts.id"), primary_key=True),
    db.Column("like", db.Boolean),
    db.Column("dislike", db.Boolean),
)


class Post(Base):
    __tablename__ = 'posts'
    metadata = metadata
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    modify_time = db.Column(db.DateTime)

    # relationships
    users = relationship('User', secondary=posts_users, back_populates='posts')
