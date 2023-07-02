"""Authentication Dependencies."""
from fastapi import Depends

from app import repo, models, services
from app.deps.user import get_user_service


async def get_auth_service(user_service: services.UserService = Depends(get_user_service)) -> services.AuthService:
    return services.AuthService(user_service=user_service)