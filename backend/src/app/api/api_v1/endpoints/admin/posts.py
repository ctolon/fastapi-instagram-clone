from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services
from app.deps.base import get_db
from app.deps.post import get_post_service


router = APIRouter()

@router.delete(
    '/delete/{id}',
    response_model=schemas.PostCreate,
    summary="Delete a post by id"
    )
async def delete(    
    *,
    db: AsyncSession = Depends(get_db),
    post_service: services.PostService = Depends(get_post_service),
    id: int,
    ):
    """
    Delete a post.
    """
    
    return await post_service.remove(db=db, id=id)