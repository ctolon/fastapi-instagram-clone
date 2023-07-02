from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.base import GenericCrudRepository
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate

class CommentRepository(GenericCrudRepository[Comment, CommentCreate, CommentUpdate]):
    
    def __init__(self, model: Comment):
        super().__init__(model=model)
    
    
    async def get_all_comments_by_post_id(self, post_id: int, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Comment]:
        query = select(self.model) \
            .offset(skip) \
            .limit(limit) \
            .filter(self.model.post_id == post_id)
        result = await db.execute(query)
        return result.scalars().all()
    
    """
    async def create(self, obj_in: CommentCreate) -> Comment:
        db_obj = Comment(
            post_id = obj_in.post_id,
            user_id = obj_in.user_id,
            comment = obj_in.comment,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
    """
    
    
