from fastapi import FastAPI
from fastapi_socketio import SocketManager

from app.dependencies import container
from app.routers.user import user_router
from app.routers.auth import login_router
from app.routers.post import posts_router
from app.models import metadata, engine, session

app = FastAPI(title='SocialNetworkingApp')
metadata.create_all(engine)

from app import routers, app_events, controllers  # noqa

s_m = SocketManager(app)
container.config.session.from_value(session)
container.config.socket_manager.from_value(s_m)

container.wire(modules=[routers, app_events, controllers])

app.include_router(user_router)
app.include_router(login_router)
app.include_router(posts_router)
