from fastapi import FastAPI

from app.routers.user import user_router
from app.routers.auth import login_router
from app.routers.post import posts_router
from app.models import metadata, engine, session

app = FastAPI(title='SocialNetworkingApp')
metadata.create_all(engine)


@app.on_event('shutdown')
async def shutdown():
    session.close()


app.include_router(user_router)
app.include_router(login_router)
app.include_router(posts_router)
