from fastapi import FastAPI

from app.dependencies import container
from app.routers.user import user_router
from app.routers.auth import login_router
from app.routers.post import posts_router
from app.models import metadata, engine

app = FastAPI(title='SocialNetworkingApp')
metadata.create_all(engine)

from app import routers, app_events, controllers  # noqa

container.wire(modules=[routers, app_events, controllers])
app.container = container

app.include_router(user_router)
app.include_router(login_router)
app.include_router(posts_router)
