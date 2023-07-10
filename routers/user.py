from typing import List

from fastapi import APIRouter, HTTPException
from controllers import user_service as service
from routers.swagger_models.user import UserData, UserDataIn

# from ..dependencies import get_token_header

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Not found'},
    }
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}


@user_router.post(
    "",
    response_model=UserData,
    responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Not found'},
    })
async def user_registration(user_data: UserDataIn):
    res = await service.registration(
        login=user_data.login, password=user_data.password, name=user_data.name, full_name=user_data.full_name,
        email=user_data.email
    )
    return res
