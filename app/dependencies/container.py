from dependency_injector import containers, providers
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.controllers import PostService, AuthService, UserService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    post_service = providers.Singleton(PostService)
    auth_service = providers.Singleton(AuthService)
    user_service = providers.Singleton(UserService, auth_service=auth_service)
    security: HTTPAuthorizationCredentials = Security(HTTPBearer())
