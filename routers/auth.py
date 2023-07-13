from fastapi import APIRouter
from controllers import auth_service
from routers.swagger_models.auth import LoginDataIn, LoginData

login_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    responses={
        401: {'description': 'Unauthorized'},
        400: {'description': 'Bad request'},
    }
)


@login_router.post('/login', response_model=LoginData)
async def login_user(login_data: LoginDataIn):
    result = await auth_service.login(login_data.email, login_data.password)
    return result


@login_router.get('/refresh_token')
async def get_access_token_by_refresh_token(refresh_token: str) -> LoginData:
    result = await auth_service.refresh(refresh_token)
    return result
