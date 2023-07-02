"""Post dependencies."""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, models, services
from app.deps.base import get_db

async def get_post_repo(db: AsyncSession = Depends(get_db)) -> repo.PostRepository:
    return repo.PostRepository(model=models.Post)

async def get_post_service(post_repo: repo.PostRepository = Depends(get_post_repo)) -> services.PostService:
    return services.PostService(repo=post_repo)