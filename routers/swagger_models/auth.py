from typing import Optional

from routers.swagger_models import DataBaseModel


class LoginDataIn(DataBaseModel):
    email: str
    password: str


class LoginData(DataBaseModel):
    access_token: str
    refresh_token: Optional[str]
