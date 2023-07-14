import logging

from fastapi import FastAPI

from app.routers.user import user_router
from app.routers.auth import login_router
from app.routers.post import posts_router
from app.models import metadata, engine, session
from app.models.user import User
from app.controllers import user_service

app = FastAPI(title='SocialNetworkingApp')
metadata.create_all(engine)


@app.on_event("startup")
async def startup_event():
    if not session.query(User).all():
        await user_service.registration(
            name='Default user',
            password='default_password',
            email='default@default.com',
            full_name='Default user'
        )
    logging.info('Default user was created.')


@app.on_event('shutdown')
async def shutdown():
    session.close()


app.include_router(user_router)
app.include_router(login_router)
app.include_router(posts_router)
