import logging

from dependency_injector.wiring import Provide, inject

from app.main import app
from app.models import session
from app.dependencies import Container


@app.on_event("startup")
@inject
async def startup_event(service=Provide[Container.user_service]):
    if not await service.get_all_items():
        await service.registration(
            name='Default user',
            password='default_password',
            email='default@default.com',
            full_name='Default user'
        )
    logging.info('Default user was created.')


@app.on_event('shutdown')
async def shutdown():
    session.close()
