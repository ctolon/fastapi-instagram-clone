
from typing import Any, List, Type
from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.repo.repo_post import PostRepository
from app.services.base import GenericCrudService

image_url_types = ['absolute', 'relative']

class PostService(GenericCrudService[Post, PostCreate, PostUpdate, PostRepository]):
    
    def __init__(self, repo: PostRepository):
        super().__init__(repo=repo)
            
    async def remove_post_by_current_user(
        self,
        db: AsyncSession,
        current_user: Depends(),
        id: str,
        ) -> Post:
        post = await self.repo.get(db=db, id=id)
        if post is None:
            raise HTTPException(status_code=404, detail=f"Post not found with id: {id}")
        if post.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
             detail='Only post creator can delete post')
        return await self.repo.remove(db=db, id=id)
    
    async def create(
        self,
        db: AsyncSession,
        obj_in: PostCreate,
        current_user: Depends()
        ) -> Post:
        if not obj_in.image_url_type in image_url_types:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="Parameter image_url_type can only take values 'absolute' or 'relative'.")
            
        obj_in = PostCreate(
            image_url = obj_in.image_url,
            image_url_type = obj_in.image_url_type,
            caption = obj_in.caption,
            user_id = current_user.id,
        )
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Post(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
        
