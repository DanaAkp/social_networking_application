import uuid

import sqlalchemy as db
from models import metadata
from models.user import users

messages = db.Table(
    'messages',
    metadata,
    db.Column('id', db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    db.Column('receiver_id', db.UUID(as_uuid=True), db.ForeignKey(users.c.id)),
    db.Column('sender_id', db.UUID(as_uuid=True), db.ForeignKey(users.c.id)),
    db.Column('like', db.Boolean),
    db.Column('dislike', db.Boolean),
)
