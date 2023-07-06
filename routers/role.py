from fastapi import APIRouter

# from ..dependencies import get_token_header

role_router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
