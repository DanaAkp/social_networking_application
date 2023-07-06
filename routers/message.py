from fastapi import APIRouter

# from ..dependencies import get_token_header

message_router = APIRouter(
    prefix="/messages",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
