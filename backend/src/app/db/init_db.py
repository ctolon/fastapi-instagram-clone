"""Initialize database with default roles and user."""""
import asyncio

from fastapi import Depends

from app import schemas
from app import services, deps
from app.deps.user import get_user_service
from app.core.config import settings
from app.db import base  # noqa: F401


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/batuhan/full-stack-fastapi-postgresql/issues/28


async def init_db(
    user_service: services.UserService = Depends(get_user_service),
    ):

    #return None
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    
    # You can add your data initialization here
        
    return {"status": "OK"}
