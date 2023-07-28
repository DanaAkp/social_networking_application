from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from dependency_injector.wiring import Provide, inject

from app.dependencies import Container
from app.routers.swagger_models.post import PostsData, PostsDataIn, RatePostsDataIn, SuccessData

posts_router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
    responses={
        200: {'description': 'Success'},
        201: {'description': 'Created'},
        401: {'description': 'Unauthorized'},
        403: {'description': 'Forbidden'},
        400: {'description': 'Bad request'},
        404: {'description': 'Not found'},
    },
)


@posts_router.post('', response_model=PostsData)
@inject
async def create_post(
        post_data: PostsDataIn,
        credentials: HTTPAuthorizationCredentials = Container.security,
        service=Depends(Provide[Container.post_service]),
        auth_service=Depends(Provide[Container.auth_service])
):
    if (token := credentials.credentials) and (curr_user_id := await auth_service.get_current_user_id(token)):
        result = await service.send_post(
            title=post_data.title, owner_id=curr_user_id,
            body=post_data.body
        )
        return result


@posts_router.get('', response_model=List[PostsData])
@inject
async def get_all_posts(
        search_text: str = None,
        credentials: HTTPAuthorizationCredentials = Container.security,
        service=Depends(Provide[Container.post_service]),
        auth_service=Depends(Provide[Container.auth_service])
):
    if (token := credentials.credentials) and (curr_user_id := await auth_service.get_current_user_id(token)):
        result = await service.get_all_posts(user_id=curr_user_id, search_text=search_text)
        return result


@posts_router.get('/{post_id}', response_model=PostsData)
@inject
async def get_post_by_id(
        post_id: str,
        credentials: HTTPAuthorizationCredentials = Container.security,
        service=Depends(Provide[Container.post_service]),
        auth_service=Depends(Provide[Container.auth_service])
):
    if (token := credentials.credentials) and await auth_service.get_current_user_id(token):
        result = await service.get_post_by_id(post_id=post_id)
        return result


@posts_router.patch('/{post_id}', response_model=SuccessData)
@inject
async def rate_post(
        post_id: str,
        rate_data: RatePostsDataIn,
        credentials: HTTPAuthorizationCredentials = Container.security,
        service=Depends(Provide[Container.post_service]),
        auth_service=Depends(Provide[Container.auth_service])
):
    if (token := credentials.credentials) and (curr_user_id := await auth_service.get_current_user_id(token)):
        result = await service.rate_post(
            is_like=rate_data.like,
            post_id=post_id, user_id=curr_user_id
        )
        return result


@posts_router.put('/{post_id}', response_model=PostsData)
@inject
async def edit_post(
        post_id: str,
        post_data: PostsDataIn,
        credentials: HTTPAuthorizationCredentials = Container.security,
        service=Depends(Provide[Container.post_service]),
        auth_service=Depends(Provide[Container.auth_service])
):
    if (token := credentials.credentials) and (curr_user_id := await auth_service.get_current_user_id(token)):
        result = await service.edit_post(post_id=post_id, user_id=curr_user_id,
                                         title=post_data.title, body=post_data.body)
        return result


@posts_router.delete('/{post_id}', response_model=SuccessData)
@inject
async def delete_post(
        post_id: str,
        credentials: HTTPAuthorizationCredentials = Container.security,
        service=Depends(Provide[Container.post_service]),
        auth_service=Depends(Provide[Container.auth_service])
):
    if (token := credentials.credentials) and (curr_user_id := await auth_service.get_current_user_id(token)):
        result = await service.delete_post(post_id=post_id, owner_id=curr_user_id)
        return result
