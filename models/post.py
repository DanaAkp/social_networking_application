import uuid

import sqlalchemy as db
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from models import metadata, Base
from models.user import users


# association_table = db.Table(
#     "post_users",
#     Base.metadata,
#     db.Column("left_id", db.ForeignKey("left_table.id"), primary_key=True),
#     db.Column("right_id", db.ForeignKey("right_table.id"), primary_key=True),
# )

class Post(Base):
    __tablename__ = 'posts'
    metadata = metadata
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text_post = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(users.c.id), nullable=False)
    date_dispatch = db.Column(db.Date, nullable=False)
    time_dispatch = db.Column(db.Time, nullable=False)

    # relationships
    # likes = relationship(back_populates='post')
    # dislikes = relationship(back_populates='post')
