import asyncio
import unittest

import pytest

import sqlalchemy as db
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models import metadata
from app.models.post import Post, RatePosts
from app.models.user import User
from app.controllers import AuthService, UserService, PostService

url = "sqlite:///:memory:"
# url = 'postgresql://postgres:postgres@localhost:5433'

user_json = {
    "id": "",
    "name": "Danagul",
    "full_name": "Akpaeva Danagul",
    "email": "kwndke@md.fd",
    "password": "Password!2"
}

TOKENS = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTY5NTQ4MzEtOTRjYi00ZjVkLTkwY2MtYTg3NGQxZWE3YWFiIiwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJleHAiOjE2OTAzMDYwOTh9.8OGBAnzW6VesUgIRuvnGKE2E4XwbT2-WMTxhgn9sRoE",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTY5NTQ4MzEtOTRjYi00ZjVkLTkwY2MtYTg3NGQxZWE3YWFiIiwic2NvcGUiOiJyZWZyZXNoX3Rva2VuIiwiZXhwIjoxNjkwMzE1MDk4fQ.RBwowpNteV0zOYSQ7QJ9MujiA0xjM3mvRgiU0R4z2Qw"
}


@pytest.fixture
def client():
    test_client = TestClient(app)
    yield test_client


@pytest.fixture(scope='session')
def loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session', autouse=True)
def session(loop):
    engine = db.create_engine(url, echo=True, future=True)
    metadata.create_all(bind=engine)
    session = db.orm.Session(engine)

    pytest.auth_service = AuthService(session)
    pytest.user_service = UserService(pytest.auth_service, session)
    pytest.post_service = PostService(session)

    yield session

    pytest.auth_service = None
    pytest.user_service = None
    pytest.post_service = None

    session.query(RatePosts).delete()
    session.query(Post).delete()
    session.query(User).delete()
    session.commit()
    session.close()
    engine.connect().close()
