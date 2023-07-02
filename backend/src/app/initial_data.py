import logging

import asyncio

from app.db.init_db import init_db
from app.db.session import SessionAsyncPostgres
from app import models, deps, services

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:

    try:
        db = SessionAsyncPostgres()
        #post_repo = repo.UserRepository(model=models.Post, db=db)        
        # Try to create session to check if DB is awake
        await init_db()
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        await db.close()  # Close the session
    

async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
