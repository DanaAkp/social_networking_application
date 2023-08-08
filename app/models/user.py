import uuid
import sqlalchemy as db
from sqlalchemy.orm import relationship

from app.models import metadata, Base


class User(Base):
    __tablename__ = 'users'
    metadata = metadata
    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Follower(Base):
    __tablename__ = "followers"
    metadata = metadata
    subscriber_id = db.Column(db.ForeignKey("users.id"), primary_key=True)  # подписчик
    subscription_id = db.Column(db.ForeignKey("users.id"), primary_key=True)  # подписка на пользователя

    subscription = relationship(User, backref='followers', foreign_keys=[subscription_id])
    subscriber = relationship(User, backref='followers', foreign_keys=[subscriber_id])
