import logging
import traceback

from fastapi import HTTPException
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.controllers.auth import AuthService


class UserService:
    FORBIDDEN_UPDATE = 'User can updating only self account.'
    ERROR_CREATE = 'Error with creating new user.'
    ERROR_UPDATE = 'Error with updating user.'
    ERROR_NOT_FOUND = 'Not found user by id {}.'

    def __init__(self, auth_service: AuthService, session: Session):
        self.auth_service = auth_service
        self.session = session

    async def registration(self, name: str, password: str, full_name: str, email: str) -> User:
        password = await self.auth_service.get_password_hash(password)
        new_user = User(
            name=name, password=password, full_name=full_name, email=email
        )
        try:
            self.session.add(new_user)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(status_code=400, detail=self.ERROR_CREATE)
        return new_user

    async def get_item_by_id(self, user_id: str) -> Optional[User]:
        query = self.session.query(User).filter(User.id == user_id)
        if result := query.one_or_none():
            return result
        raise HTTPException(404, self.ERROR_NOT_FOUND.format(user_id))

    async def get_item_by_name(self, user_name: str = None) -> List[Optional[User]]:
        query = self.session.query(User)
        if user_name:
            query = query.filter(User.name.ilike(f'%{user_name}%'))
        return query.all()

    async def get_all_items(self) -> List[Optional[User]]:
        return self.session.query(User).all()

    async def edit_user(self, user_id: str, name: str, password: str, full_name: str, email: str) -> Optional[User]:
        query = self.session.query(User).filter(User.id == user_id)
        try:
            if user := query.one_or_none():
                user.name = name
                user.full_name = full_name
                user.email = email
                user.password = await self.auth_service.get_password_hash(password)
                self.session.commit()
                return user
        except Exception as error:
            self.session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_UPDATE)
        raise HTTPException(404, self.ERROR_NOT_FOUND.format(user_id))
