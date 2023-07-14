import logging
import traceback

from fastapi import HTTPException
from typing import List

from app.models import session
from app.models.user import User
from app.controllers import auth_service


class UserService:
    FORBIDDEN_UPDATE = 'User can updating only self account.'
    ERROR_CREATE = 'Error with creating new user.'
    ERROR_UPDATE = 'Error with updating user.'
    ERROR_NOT_FOUND = 'Not found user by id {}.'

    async def registration(self, name: str, password: str, full_name: str, email: str) -> User:
        password = await auth_service.get_password_hash(password)
        new_user = User(
            name=name, password=password, full_name=full_name, email=email
        )
        try:
            session.add(new_user)
            session.commit()
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(status_code=400, detail=self.ERROR_CREATE)
        return new_user

    async def get_item_by_id(self, user_id: str) -> User:
        query = session.query(User).filter(User.id == user_id)
        if result := query.one_or_none():
            return result
        raise HTTPException(404, self.ERROR_NOT_FOUND.format(user_id))

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
                user.password = await auth_service.get_password_hash(password)
                session.commit()
                return user
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_UPDATE)
        raise HTTPException(404, self.ERROR_NOT_FOUND.format(user_id))
