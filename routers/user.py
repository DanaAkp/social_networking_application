from typing import List, Optional

from fastapi import APIRouter, HTTPException
from controllers import user_service as service
from routers.swagger_models.user import UserData, UserDataIn

# from ..dependencies import get_token_header

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(get_token_header)],
    responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Not found'},
    }
)


@user_router.post("", response_model=UserData)
async def user_registration(user_data: UserDataIn):
    res = await service.registration(
        password=user_data.password, name=user_data.name, full_name=user_data.full_name,
        email=user_data.email
    )
    return res


@user_router.get("/{user_id}", response_model=UserData)
async def get_user_by_id(user_id: str):
    res = await service.get_item_by_id(user_id)
    return res


@user_router.get("", response_model=List[UserData])
async def get_all_users(user_name: Optional[str] = None):
    res = await service.get_item_by_name(user_name)
    return res


@user_router.put("/{user_id}", response_model=UserData)
async def update_user(user_id: str, user_data: UserDataIn):
    res = await service.edit_user(
        password=user_data.password, name=user_data.name, full_name=user_data.full_name,
        email=user_data.email, user_id=user_id
    )
    return res
