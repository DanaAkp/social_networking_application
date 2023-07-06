from fastapi import FastAPI

from routers.user import user_router
from routers.role import role_router
from routers.message import message_router
from models import metadata, engine, connection

app = FastAPI()
metadata.create_all(engine)


@app.on_event("shutdown")
async def shutdown():
    await connection.close()


app.include_router(user_router)
app.include_router(role_router)
app.include_router(message_router)
