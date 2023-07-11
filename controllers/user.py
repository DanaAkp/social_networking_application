import logging
import traceback

from typing import List

from models import session
from models.user import User
from hashlib import sha256
from fastapi import HTTPException


class UserService:
    async def registration(self, name: str, password: str, full_name: str, email: str) -> User:
        password = await self._get_hash_password(password)
        new_user = User(
            name=name, password=password, full_name=full_name, email=email
        )
        try:
            session.add(new_user)
            session.commit()
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(status_code=400, detail='Error with creating new user.')
        return new_user

    async def get_item_by_id(self, user_id: str) -> User:
        query = session.query(User).filter(User.id == user_id)
        if result := query.one_or_none():
            return result
        raise HTTPException(404, f'Not found user by id {user_id}.')

    async def get_item_by_name(self, user_name: str = None) -> List[User]:
        query = session.query(User)
        if user_name:
            query = query.filter(User.name.ilike(f'%{user_name}%'))
        return query.all()

    async def get_all_items(self) -> List[User]:
        return session.query(User).all()

    async def edit_user(self, user_id: str, name: str, password: str, full_name: str, email: str) -> User:
        query = session.query(User).filter(User.id == user_id)
        try:
            if user := query.one_or_none():
                user.name = name
                user.full_name = full_name
                user.email = email
                user.password = await self._get_hash_password(password)
                session.commit()
                return user
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, 'Error with updating user.')
        raise HTTPException(404, f'Not found user by id {user_id}.')

    async def _get_hash_password(self, password) -> str:
        return sha256(password.encode()).hexdigest()
