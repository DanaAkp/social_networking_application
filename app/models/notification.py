import uuid
import sqlalchemy as db
from datetime import datetime

from sqlalchemy.orm import relationship

from app.models import metadata, Base


class Notification(Base):
    """
    Уведомления пользователя о новых постах пользователей, на которых он подписан.
    """
    __tablename__ = 'notifications'
    metadata = metadata
    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    subscription_id = db.Column(db.Uuid, db.ForeignKey('users.id'), nullable=False)
    subscriber_id = db.Column(db.Uuid, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Uuid, db.ForeignKey('posts.id'), nullable=False)

    subscriber = relationship('')
