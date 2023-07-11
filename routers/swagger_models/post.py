import datetime
import uuid
from typing import List

from routers.swagger_models import DataBaseModel


class PostsDataIn(DataBaseModel):
    title: str
    body: str


class RatePostsDataIn(DataBaseModel):
    like: bool
    dislike: bool


class UserRatePostData(DataBaseModel):
    user_id: uuid.UUID
    like: bool
    dislike: bool


class PostsData(DataBaseModel):
    id: uuid.UUID
    title: str
    body: str
    owner_id: uuid.UUID
    create_time: datetime.datetime
    modify_time: datetime.datetime
    users: List[UserRatePostData]
