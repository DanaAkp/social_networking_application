from app.controllers.post import PostService
from app.controllers.auth import AuthService

post_service = PostService()
auth_service = AuthService()

from app.controllers.user import UserService  # noqa circular import

user_service = UserService()
