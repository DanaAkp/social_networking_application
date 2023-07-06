from typing import Annotated

from fastapi import Header, HTTPException


class AuthService:
    async def get_token_header(self, x_token: Annotated[str, Header()]):
        if x_token != "fake-super-secret-token":  # todo
            raise HTTPException(status_code=400, detail="X-Token header invalid")

    async def get_query_token(self, token: str):
        if token != "jessica":  # todo
            raise HTTPException(status_code=400, detail="No Jessica token provided")

    async def login(self, login: str, password: str):  # todo return token
        pass
