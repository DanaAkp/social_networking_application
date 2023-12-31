import re
import uuid
from typing import Optional

from pydantic import BaseModel, validator, Field
from app.constants import len_of_full_user_name, len_of_user_name, min_len_of_password
from app.routers.swagger_models import DataBaseModel


class UserDataIn(BaseModel):
    name: str = Field(max_length=len_of_user_name)
    full_name: str = Field(max_length=len_of_full_user_name)
    email: str
    password: str = Field(min_length=min_len_of_password)

    @validator('email')
    def check_email(cls, v):
        pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if not re.search(pattern, v):
            raise ValueError('Invalid email.')
        return v

    @validator('password')
    def check_password(cls, v):
        pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
        if not re.search(pattern, v):
            raise ValueError('Weak password.')
        return v


class UserData(DataBaseModel):
    id: uuid.UUID
    name: str
    full_name: Optional[str]
    email: str
