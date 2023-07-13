from typing import List, Optional

from fastapi import APIRouter, HTTPException
from controllers import auth_service, user_service as service
from routers.swagger_models.user import UserData, UserDataIn
from fastapi.security import HTTPAuthorizationCredentials

user_router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Not found'},
    }
)


@user_router.post('', response_model=UserData)
async def user_registration(user_data: UserDataIn):
    res = await service.registration(
        password=user_data.password, name=user_data.name, full_name=user_data.full_name,
        email=user_data.email
    )
    return res


@user_router.get('/{user_id}', response_model=UserData)
async def get_user_by_id(user_id: str, credentials: HTTPAuthorizationCredentials = auth_service.security):
    if (token := credentials.credentials) and await auth_service.get_current_user_id(token):
        res = await service.get_item_by_id(user_id)
        return res


@user_router.get('', response_model=List[UserData])
async def get_all_users(user_name: Optional[str] = None,
                        credentials: HTTPAuthorizationCredentials = auth_service.security):
    if (token := credentials.credentials) and await auth_service.get_current_user_id(token):
        res = await service.get_item_by_name(user_name)
        return res


@user_router.put('/{user_id}', response_model=UserData)
async def update_user(
        user_id: str, user_data: UserDataIn,
        credentials: HTTPAuthorizationCredentials = auth_service.security
):
    if not (token := credentials.credentials) or (await auth_service.get_current_user_id(token) != user_id):
        raise HTTPException(403, service.FORBIDDEN_UPDATE)
    res = await service.edit_user(
        password=user_data.password, name=user_data.name, full_name=user_data.full_name,
        email=user_data.email, user_id=user_id
    )
    return res
