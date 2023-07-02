
from typing import Any, List, Dict, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repo.repo_user import UserRepository
from app.services.base import GenericCrudService
from app.core.security import get_password_hash

        
class UserService(GenericCrudService[User, UserCreate, UserUpdate, UserRepository]):
    
    def __init__(self, repo):
        super().__init__(repo=repo)
        
        
    async def create(self, db: AsyncSession, obj_in: User) -> User:
        user_email = await self.repo.get_user_by_email(db=db, email=obj_in.email)
        if user_email:
            raise HTTPException(
                status_code=400,
                detail=f"The user with this email: {user_email} already exists in the system.",
            )
        user_username = await self.repo.get_user_by_username(db=db, username=obj_in.username)
        if user_username:
            raise HTTPException(
                status_code=400,
                detail=f"The user with this username: {user_username} already exists in the system.",
            )
        user = User(
            username=obj_in.username,
            email=obj_in.email,
            password=get_password_hash(obj_in.password)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    
    async def update_current_user(self, db: AsyncSession, current_user: Depends(...), obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        result = await self.repo.update(db=db, id=current_user.id, obj_in=obj_in)
        return result
    
    async def get_user_by_username(self, db: AsyncSession, username: str) -> User:
        user = await self.repo.get_user_by_username(db=db, username=username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
              detail=f'User with username {username} not found')
        return user
    
    async def get_user_by_oauth2_password_request_form(self, db: AsyncSession, request: OAuth2PasswordRequestForm) -> Optional[User]:
        user = await self.repo.get_user_by_oauth2_password_request_form(db=db, request=request)
        return user