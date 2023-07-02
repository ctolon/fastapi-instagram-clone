from typing import Any, Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.repo.base import GenericCrudRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserRepository(GenericCrudRepository[User, UserCreate, UserUpdate]):
    
    def __init__(self, model: User):
        super().__init__(model=model)
        
    async def create(self, *, db: AsyncSession, obj_in: UserCreate) -> User:
        db_obj = User(
            username = obj_in.username,
            email = obj_in.email,
            password = get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        query = select(self.model).filter(self.model.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    
    async def get_user_by_oauth2_password_request_form(self, db: AsyncSession, request: OAuth2PasswordRequestForm) -> Optional[User]:
        query = select(self.model).filter(self.model.username == request.username)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        query = select(User).filter(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()