from fastapi import APIRouter, HTTPException
from controllers import user_service as service
from routers.swagger_models.user import UserData, UserDataIn

# from ..dependencies import get_token_header

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@user_router.get("")
async def read_items():
    all_items = await service.get_all_items()
    return all_items


@user_router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@user_router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}


@user_router.post(
    "",
    tags=["custom"],
    response_model=UserData,
    responses={403: {"description": "Operation forbidden"}},
)
async def user_registration(user_data: UserDataIn):
    res = await service.registration(
        login=user_data.login, password=user_data.password, name=user_data.name, full_name=user_data.full_name,
        email=user_data.email
    )
    return res
