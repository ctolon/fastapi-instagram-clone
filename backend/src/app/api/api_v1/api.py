from fastapi import APIRouter
from app.api.api_v1.endpoints import posts, users, comments, auth



api_v1_router = APIRouter()
api_v1_router.include_router(posts.router, prefix="/post", tags=["post"])
api_v1_router.include_router(comments.router, prefix="/comment", tags=["comment"])
api_v1_router.include_router(users.router, prefix="/user", tags=["user"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
