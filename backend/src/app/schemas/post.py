from typing import Optional, List
from datetime import datetime
from app.schemas.user import User
from app.schemas.comment import Comment

from pydantic import BaseModel

# ==================== Base Schema Start ====================

# Shared properties
class PostBase(BaseModel):
    image_url: Optional[str] = None
    image_url_type: Optional[str] = None
    caption: Optional[str] = None
    timestamp: Optional[datetime] = None
    user_id: Optional[int] = None
    
# Properties to receive via API on creation
class PostCreate(PostBase):
    image_url: str
    image_url_type: str
    caption: str
    #timestamp: datetime
    user_id: int

# Properties to receive via API on update
class PostUpdate(PostBase):
    pass


class PostInDBBase(PostBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Post(PostInDBBase):
    pass


# Additional properties stored in DB
class PostInDB(PostInDBBase):
    pass

# ==================== Base Schema Start ====================

# Schema for Post Display on Post UI with releationships
class PostDisplay(BaseModel):
  id: int
  image_url: str
  image_url_type: str
  caption: str
  timestamp: datetime
  user: User
  comments: List[Comment]
  class Config():
    orm_mode = True


