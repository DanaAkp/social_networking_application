import logging
import traceback

from fastapi import HTTPException
from typing import List

from app.models import repo
from app.models.user import User
from app.controllers import auth_service


class UserService:
    FORBIDDEN_UPDATE = 'User can updating only self account.'
    ERROR_CREATE = 'Error with creating new user.'
    ERROR_UPDATE = 'Error with updating user.'
    ERROR_NOT_FOUND = 'Not found user by id {}.'

    async def registration(self, name: str, password: str, full_name: str, email: str) -> User:
        password = await auth_service.get_password_hash(password)

        try:
            new_user = await repo.create_instance(
                model=User, commit=True,
                name=name, password=password, full_name=full_name, email=email
            )
        except Exception as error:
            await repo.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(status_code=400, detail=self.ERROR_CREATE)
        return new_user

    async def get_item_by_id(self, user_id: str) -> User:
        if result := await repo.get_item_by_id(User, user_id):
            return result
        raise HTTPException(404, self.ERROR_NOT_FOUND.format(user_id))

    async def get_item_by_name(self, user_name: str = None) -> List[User]:
        query = await repo.get_query(User)
        if user_name:
            query = await repo.get_filter_query(User, (User.name.ilike(f'%{user_name}%'),))
        return query.all()

    async def get_all_items(self) -> List[User]:
        return await repo.get_all_by_query(User)

    async def edit_user(self, user_id: str, name: str, password: str, full_name: str, email: str) -> User:
        try:
            if user := await repo.get_item_by_id(User, user_id):
                user.name = name
                user.full_name = full_name
                user.email = email
                user.password = await auth_service.get_password_hash(password)
                await repo.commit()
                return user
        except Exception as error:
            await repo.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_UPDATE)
        raise HTTPException(404, self.ERROR_NOT_FOUND.format(user_id))
