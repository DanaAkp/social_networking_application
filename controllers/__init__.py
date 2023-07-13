from controllers.post import PostService
from controllers.auth import AuthService

post_service = PostService()
auth_service = AuthService()

from controllers.user import UserService  # noqa circular import

user_service = UserService()
