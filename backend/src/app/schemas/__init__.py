"""Pydantic Schemas for the application."""
# Import all schemas here
from .user import User, UserCreate, UserInDB, UserUpdate, UserDisplayOnPostUI, UserAuth
from .comment import Comment, CommentCreate, CommentInDB, CommentUpdate
from .post import Post, PostCreate, PostInDB, PostUpdate, PostDisplay
from .auth import AuthLogin