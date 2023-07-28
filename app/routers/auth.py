from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.dependencies import Container
from app.routers.swagger_models.auth import LoginDataIn, LoginData

login_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    responses={
        401: {'description': 'Unauthorized'},
        400: {'description': 'Bad request'},
    }
)


@login_router.post('/login', response_model=LoginData)
@inject
async def login_user(login_data: LoginDataIn, auth_service=Depends(Provide[Container.auth_service])):
    result = await auth_service.login(login_data.email, login_data.password)
    return result


@login_router.get('/refresh_token')
@inject
async def get_access_token_by_refresh_token(refresh_token: str,
                                            auth_service=Depends(Provide[Container.auth_service])) -> LoginData:
    result = await auth_service.refresh(refresh_token)
    return result
