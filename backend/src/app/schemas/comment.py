from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

# ==================== Base Schema Start ====================

# Shared properties
class CommentBase(BaseModel):
    username: Optional[str] = None
    text: Optional[str] = None
    post_id: Optional[int] = None
    
# Properties to receive via API on creation
class CommentCreate(CommentBase):
    username: str
    text: str
    post_id: int
    
# Properties to receive via API on update
class CommentUpdate(CommentBase):
    text: str


class CommentInDBBase(CommentBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Comment(CommentInDBBase):
    pass


# Additional properties stored in DB
class CommentInDB(CommentInDBBase):
    pass

# ==================== Base Schema End ====================

# Schema for Comment Display on Post UI
class CommentDisplayOnPostUI(BaseModel):
  text: str
  username: str
  timestamp: datetime
  class Config():
    orm_mode = True