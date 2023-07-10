import uuid

from fastapi import APIRouter

from controllers import message_service as service
from routers.swagger_models.post import PostsData, PostsDataIn, RatePostsDataIn

# from ..dependencies import get_token_header

posts_router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@posts_router.post("/{owner_id}", response_model=PostsData)
async def send_message(post_data: PostsDataIn):
    result = await service.send_post(
        text_post=post_data.text_message, owner_id=post_data.owner_id,
    )
    return result


@posts_router.get("/{owner_id}", response_model=PostsData)
async def get_all_messages(owner_id: str):
    result = await service.get_all_messages(received_id=owner_id, sender_id='')  # todo after add auth
    return result


@posts_router.patch("/{message_id}", response_model=PostsData)
async def rate_message(post_id: str, rate_data: RatePostsDataIn):
    result = await service.rate_message(
        like=rate_data.like, dislike=rate_data.dislike, post_id=post_id,
    )
    return result
