"""Base dependencies for FastAPI app mostly for db sessions."""""
from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionAsyncPostgres

async def get_db() -> Generator:      
    try:
        db = SessionAsyncPostgres()
        yield db
    except:
        await db.rollback()
        raise
    finally:
        await db.close()
