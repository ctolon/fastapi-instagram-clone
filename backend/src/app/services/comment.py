
from typing import Any, List, Type

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.repo_comment import CommentRepository
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.base import GenericCrudService

        
class CommentService(GenericCrudService[Comment, CommentCreate, CommentUpdate, CommentRepository]):
    
    
    def __init__(self, repo):
        super().__init__(repo=repo)
        
        
    async def get_all_comments_by_post_id(
        self,
        db: AsyncSession,
        post_id: int,
        skip: int = 0,
        limit: int = 100
        ) -> List[Comment]:
        all_comments = await self.repo.get_all_comments_by_post_id(db=db, post_id=post_id, skip=skip, limit=limit)
        return all_comments

        
