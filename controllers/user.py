import logging
import traceback

from sqlalchemy import select, insert, update
from typing import List

from models import connection
from models.user import users
from hashlib import sha256


class UserService:
    async def registration(self, name: str, password: str, full_name: str, email: str):
        await self._check_unique_email(email)
        new_user = insert(users).values(
            name=name, password=await self._get_hash_password(password), full_name=full_name, email=email
        )
        try:
            connection.execute(new_user)
            connection.commit()
        except Exception as error:
            connection.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise ValueError('Error with creating new user.')

    async def get_item_by_id(self, user_id: str):
        s = select(users).where(users.c.id == user_id)
        if result := connection.execute(s).one_or_none():
            return result
        raise ValueError(f'Not found user by id {user_id}.')

    async def get_item_by_name(self, user_name: str):
        s = select(users).where(users.c.name.ilike(f'%{user_name}%'))
        result = connection.execute(s).fetchall()
        return result

    async def get_all_items(self) -> List[users]:
        s = select(users)
        result = connection.execute(s).fetchall()
        return result

    async def _check_unique_email(self, email: str):
        s = select(users).where(users.c.email == email)
        if connection.execute(s).one_or_none():
            return False
        return True

    async def edit_user(self, user_id: str, name: str, password: str, full_name: str, email: str):
        await self._check_unique_email(email)
        update_user = update(users).where(users.c.id == user_id) \
            .values(name=name, password=password, full_name=full_name, email=email)
        try:
            if result := connection.execute(update_user).one_or_none():
                connection.commit()
                return result
        except Exception as error:
            connection.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise ValueError('Error with updating user.')
        raise ValueError(f'Not found user by id {user_id}.')

    async def _get_hash_password(self, password):
        return sha256(password.encode()).hexdigest()
