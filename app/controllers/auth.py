import uuid
from datetime import timedelta, datetime
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security

from app import config
from app.models import repo
from app.models.user import User


class AuthService:
    TOKEN_EXPIRED = 'The token is expired.'
    TOKEN_INVALID = 'The token is invalid.'
    REFRESH_TOKEN_EXPIRED = 'The refresh token is expired.'
    REFRESH_TOKEN_INVALID = 'The refresh token is invalid.'
    INVALID_LOGIN_DATA = 'Invalid login data.'

    SECRET_KEY = config.SECRET
    ALGORITHM = config.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_HOURS = config.REFRESH_TOKEN_EXPIRE_HOURS

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
    security = Security(HTTPBearer())

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def login(self, email: str, password: str) -> dict:
        query = await repo.get_filter_query(User, (User.email == email,))
        user = await repo.get_one_or_none_by_query(query)
        if not (user and await self.verify_password(password, user.password)):
            raise HTTPException(400, self.INVALID_LOGIN_DATA)

        access_token = self.create_access_token(user.id)
        refresh_token = self.create_refresh_token(user.id)
        return {'access_token': access_token, 'refresh_token': refresh_token,
                'token_type': 'bearer'}

    def create_access_token(self, user_id: Union[uuid.UUID, str]) -> str:
        to_encode = {
            'user_id': str(user_id),
            'scope': 'access_token',
            'exp': datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, user_id: Union[uuid.UUID, str]) -> str:
        to_encode = {
            'user_id': str(user_id),
            'scope': 'refresh_token',
            'exp': datetime.utcnow() + timedelta(hours=self.REFRESH_TOKEN_EXPIRE_HOURS)
        }
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def get_current_user_id(self, access_token: str) -> str:
        try:
            payload = jwt.decode(access_token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            if payload.get('scope') == 'access_token':
                return payload.get('user_id')
            raise JWTError()
        except jwt.ExpiredSignatureError:
            raise HTTPException(400, self.TOKEN_EXPIRED)
        except JWTError:
            raise HTTPException(401, self.TOKEN_INVALID)

    async def refresh(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            if payload.get('scope') == 'refresh_token':
                access_token = self.create_access_token(payload.get('user_id'))
                return {'access_token': access_token}
            raise JWTError()
        except jwt.ExpiredSignatureError:
            raise HTTPException(400, self.REFRESH_TOKEN_EXPIRED)
        except JWTError:
            raise HTTPException(401, self.REFRESH_TOKEN_INVALID)
