import uuid

import sqlalchemy as db
from models import metadata

users = db.Table(
    'users',
    metadata,
    db.Column('id', db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    db.Column('name', db.String),
    db.Column('full_name', db.String),
    db.Column('email', db.String),
    db.Column('password', db.String),
    db.Column('role_id', db.UUID(as_uuid=True), db.ForeignKey(roles.c.id)),
    db.UniqueConstraint('email'),

)
