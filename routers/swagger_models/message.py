from pydantic import BaseModel, Field, Required


class MessageDataIn(BaseModel):
    receiver_id: Required[str] = Field()
    sender_id: Required[str]
    like: bool
    dislike: bool


class MessageData(BaseModel):
    id: str
    receiver_id: str
    sender_id: str
    like: bool
    dislike: bool
