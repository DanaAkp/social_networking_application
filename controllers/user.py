import logging
import traceback

from sqlalchemy import select, insert
from typing import List

from models import connection
from models.user import users


class UserService:
    async def registration(self, name: str, password, full_name, email):
        await self._check_unique_email(email)
        user = insert(users).values(
            name=name, password=password, full_name=full_name, email=email
        )
        try:
            connection.execute(user)
            connection.commit()
        except Exception as error:
            connection.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')

    async def get_item_by_id(self, user_id: str):
        s = select(users).where(id=user_id)
        if result := connection.execute(s).one_or_none():
            return result
        raise ValueError(f'Not found user by id {user_id}.')

    async def get_item_by_name(self, user_name: str):
        s = select(users).where(name=user_name)  # todo using ilike
        result = connection.execute(s).fetchall()
        return result

    async def get_all_items(self) -> List[users]:
        s = select(users)
        result = connection.execute(s).fetchall()
        return result

    async def _check_unique_email(self, email: str):
        s = select(users).where(email=email)
        if connection.execute(s).one_or_none():
            return False
        return True
