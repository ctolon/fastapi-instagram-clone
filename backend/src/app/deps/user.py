"""User dependencies"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, models, services
from app.deps.base import get_db

from app.core.config import settings


SECRET_KEY = '333809dfe79d55fc49216952965632e7cc0b46b1d27ce34792581014a6cef1b1'
ALGORITHM = settings.HASH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> repo.UserRepository:
    return repo.UserRepository(model=models.User)

async def get_user_service(user_repo: repo.UserRepository = Depends(get_user_repo)) -> services.UserService:
    return services.UserService(repo=user_repo)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    user_service: services.UserService = Depends(get_user_service)
    ) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_service.get_user_by_username(db=db, username=username)
    if user is None:
        raise credentials_exception
    return user
