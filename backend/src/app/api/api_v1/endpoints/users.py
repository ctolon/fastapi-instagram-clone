from typing import Any, List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi_utils.cbv import cbv
# from fastapi_utils.inferring_router import InferringRouter

from app import schemas, services
from app.deps.user import get_user_service, get_current_user
from app.deps.base import get_db

router = APIRouter()


@router.post(
    '/add',
    response_model=schemas.UserDisplayOnPostUI,
    summary="Create new user"
    )
async def create_user(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    user_service: services.UserService = Depends(get_user_service)):
    return await user_service.create(db=db, obj_in=user_in)

@router.get(
    '/get-current-user',
    response_model=schemas.User,
    summary="Get current user"
)
async def current_user(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    user_service: services.UserService = Depends(get_user_service)
):
    
    return await user_service.get(db=db, id=current_user.id)


@router.get(
    '/get-all',
    response_model=List[schemas.User],
    summary="Get all users"
)
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user_service: services.UserService = Depends(get_user_service)
):
    
    return await user_service.get_all(db=db, skip=skip, limit=limit)


@router.put(
    '/edit',
    response_model=schemas.UserDisplayOnPostUI,
    summary="Current Update User"
)
async def update_current_user(
    user_in: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    user_service: services.UserService = Depends(get_user_service)
):

    return await user_service.update_current_user(db=db, id=current_user.id, obj_in=user_in)

# ==================================================
# Admin APIs
# ==================================================

@router.delete(
    '/delete/{id}',
    response_model=schemas.UserDisplayOnPostUI,
    summary="Delete user By Id"
)
async def delete_user_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    user_service: services.UserService = Depends(get_user_service)
    ):
    
    return await user_service.remove(db=db, id=id)

@router.get(
    '/get/{id}',
    response_model=schemas.UserDisplayOnPostUI,
    summary="Get user by id"
)
async def get_user_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    user_service: services.UserService = Depends(get_user_service)
    ):
    return await user_service.get(db=db, id=id)

@router.put(
    '/edit/{id}',
    response_model=schemas.UserDisplayOnPostUI,
    summary="Update user by id"
)
async def update_user_by_id(
    id: int,
    user_in: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    user_service: services.UserService = Depends(get_user_service)
    ):
    return await user_service.update(db=db, id=id, obj_in=user_in)