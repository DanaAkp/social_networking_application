import datetime
import uuid

from routers.swagger_models import DataBaseModel


class PostsDataIn(DataBaseModel):
    owner_id: uuid.UUID
    text_message: str


class RatePostsDataIn(DataBaseModel):
    owner_id: uuid.UUID
    like: bool
    dislike: bool


class PostsData(DataBaseModel):
    id: uuid.UUID
    text: str = None
    owner_id: uuid.UUID
    date_dispatch: datetime.date = None
    time_dispatch: datetime.time = None
