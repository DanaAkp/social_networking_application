from pydantic import BaseModel


class AddRoleIn(BaseModel):
    role_id: str
    user_id: str


class BlockUserIn(BaseModel):
    user_id: str
    block: bool
