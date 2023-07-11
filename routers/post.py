from fastapi import APIRouter

from controllers import message_service as service
from routers.swagger_models.post import PostsData, PostsDataIn, RatePostsDataIn

# from ..dependencies import get_token_header

posts_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    # dependencies=[Depends(get_token_header)],
    responses={
        200: {"description": "Success"},
        201: {"description": "Created"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        400: {"description": "Bad request"},
        404: {"description": "Not found"},
    },
)


@posts_router.post("", response_model=PostsData)
async def create_post(post_data: PostsDataIn):
    result = await service.send_post(
        title=post_data.title, owner_id='',  # todo after auth
        body=post_data.body
    )
    return result


@posts_router.get("", response_model=PostsData)
async def get_all_posts():
    result = await service.get_all_posts(user_id='')  # todo after add auth
    return result


@posts_router.patch("/{post_id}", response_model=PostsData)
async def rate_post(post_id: str, rate_data: RatePostsDataIn):
    result = await service.rate_post(
        like=rate_data.like, dislike=rate_data.dislike,
        post_id=post_id, user_id=''  # todo after add auth
    )
    return result


@posts_router.put("/{post_id}", response_model=PostsData)
async def edit_post(post_id: str, post_data: PostsDataIn):
    result = await service.edit_post(post_id=post_id, title=post_data.title, body=post_data.body)
    return result


@posts_router.delete("/{post_id}", response_model=PostsData)
async def delete_post(post_id: str):
    result = await service.delete_post(post_id=post_id, owner_id='')  # todo after add auth
    return result
