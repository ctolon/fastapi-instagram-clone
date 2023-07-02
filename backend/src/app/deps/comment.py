"""Comment dependencies."""""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, models, services
from app.deps.base import get_db


async def get_comment_repo(db: AsyncSession = Depends(get_db)) -> repo.CommentRepository:
    return repo.CommentRepository(model=models.Comment)

async def get_comment_service(comment_repo: repo.CommentRepository = Depends(get_comment_repo)) -> services.CommentService:
    return services.CommentService(repo=comment_repo)