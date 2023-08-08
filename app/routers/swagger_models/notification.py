import datetime
import uuid

from app.routers.swagger_models import DataBaseModel


class NotificationData(DataBaseModel):
    id: uuid.UUID
    create_time: datetime.datetime
    is_read: bool

    subscription_id: uuid.UUID
    subscriber_id: uuid.UUID
    post_id: uuid.UUID
