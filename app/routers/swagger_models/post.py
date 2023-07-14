import datetime
import uuid
from typing import Optional

from app.routers.swagger_models import DataBaseModel


class PostsDataIn(DataBaseModel):
    title: str
    body: str


class RatePostsDataIn(DataBaseModel):
    like: bool


class PostsData(DataBaseModel):
    id: uuid.UUID
    title: str
    body: str
    owner_id: uuid.UUID
    create_time: datetime.datetime
    modify_time: Optional[datetime.datetime]
    count_likes: Optional[int]
    count_dislikes: Optional[int]


class SuccessData(DataBaseModel):
    success: str
