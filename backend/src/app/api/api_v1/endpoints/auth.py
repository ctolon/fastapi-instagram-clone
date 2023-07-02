from typing import Any, List
import pathlib

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services
from app.deps.auth import get_auth_service
from app.deps.base import get_db

router = APIRouter()

@router.post(
    '/login',
    summary="Login user endpoint",
    response_model=schemas.AuthLogin
    )
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    auth_service: services.AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db)
    ):

    return await auth_service.login(db=db ,oauth_in=request)