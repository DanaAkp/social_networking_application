from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from dependency_injector.wiring import Provide, inject

from app.dependencies import Container
from app.routers.swagger_models.notification import NotificationData

notification_router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
    responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized'},
        400: {'description': 'Bad request'},
        404: {'description': 'Not found'},
    },
)


@notification_router.get('', response_model=NotificationData)
@inject
async def get_all_notifications(
        is_read: bool = None,
        credentials: HTTPAuthorizationCredentials = Container.security,
        service=Depends(Provide[Container.notification_service]),
        auth_service=Depends(Provide[Container.auth_service])
):
    if (token := credentials.credentials) and (curr_user_id := await auth_service.get_current_user_id(token)):
        result = await service.get_notifications(user_id=curr_user_id, is_read=is_read)
        return result
