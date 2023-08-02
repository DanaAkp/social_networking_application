import pytest
from app.models.user import User

from .conftest import user_json


@pytest.mark.asyncio
async def test_create_user(session):
    result = await pytest.user_service.registration(
        name=user_json.get('name'),
        full_name=user_json.get('full_name'),
        email=user_json.get('email'),
        password=user_json.get('password'),
    )

    assert (user := session.query(User).filter(User.email == user_json.get('email')).one_or_none())
    assert user.name == result.name
    assert user.full_name == result.full_name
    assert user.email == result.email
