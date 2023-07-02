from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services
from app.deps.comment import get_comment_service
from app.deps.user import get_current_user
from app.deps.base import get_db


router = APIRouter()


@router.post(
    '/add',
    summary="Create a new comment"
    )
async def create(
    request: schemas.CommentCreate,
    db: AsyncSession = Depends(get_db),
    comment_service: services.CommentService = Depends(get_comment_service),
    current_user: schemas.UserAuth = Depends(get_current_user),
    ):
  return await comment_service.create(db=db, obj_in=request)

@router.get(
    '/get-all',
    response_model=List[schemas.Post],
    summary="Get all comments"
)
async def get_all(
    *,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    comment_service: services.CommentService = Depends(get_comment_service),
    ) -> List[schemas.Post]:
    """
    Get all comments.
    """
    
    return await comment_service.get_all(db=db, skip=skip, limit=limit)

@router.get(
    '/get-all/{post_id}',
    response_model=List[schemas.Post],
    summary="Get all comments by post id"
)
async def get_all_by_post_id(
    *,
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    comment_service: services.CommentService = Depends(get_comment_service)
    ) -> List[schemas.Post]:
    """
    Get all comments by post id.
    """
    
    return await comment_service.get_all_comments_by_post_id(db=db, skip=skip, limit=limit, post_id=post_id)