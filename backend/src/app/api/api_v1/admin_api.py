from fastapi import APIRouter
from app.api.api_v1.endpoints.admin import posts

admin_api_v1_router = APIRouter()

admin_api_v1_router.include_router(posts.router, prefix="/post", tags=["admin" ,"post"])