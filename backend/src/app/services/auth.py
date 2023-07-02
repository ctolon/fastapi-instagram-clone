
from typing import Any, List, Type

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.services.user import UserService
from app.core.security import verify_password, create_access_token


class AuthService:
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    async def login(self, db: AsyncSession, oauth_in: OAuth2PasswordRequestForm):
        user = await self.user_service.get_user_by_oauth2_password_request_form(db=db, request=oauth_in)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail='Invalid credentials')
        print("User pass:", user.password)
        print("ouath pass:", oauth_in.password)
        if not verify_password(user.password, oauth_in.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail='Incorrect password')
        
        access_token = create_access_token(data={'username': user.username})
        
        return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
        }
    
    

