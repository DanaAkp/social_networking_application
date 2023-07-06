import uuid

import sqlalchemy as db
from models import metadata

roles = db.Table(
    'roles',
    metadata,
    db.Column('id', db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    db.Column('name', db.String)
)
