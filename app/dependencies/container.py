from dependency_injector import containers, providers
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_socketio import SocketManager

from app.controllers import PostService, AuthService, UserService, NotificationService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # socket_manager = providers.Singleton(SocketManager, app=config.app)

    post_service = providers.Singleton(
        PostService,
        session=config.session
    )
    auth_service = providers.Singleton(
        AuthService,
        session=config.session
    )
    user_service = providers.Singleton(
        UserService,
        auth_service=auth_service,
        session=config.session,
        socket_manager=config.socket_manager
    )
    notification_service = providers.Singleton(
        NotificationService,
        session=config.sessioin,
        socket_manager=config.socket_manager
    )
    security: HTTPAuthorizationCredentials = Security(HTTPBearer())
