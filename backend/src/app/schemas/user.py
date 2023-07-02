from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

# ==================== Base Schema Start ====================

# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    
# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    email: str
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass

# ==================== Base Schema End ====================

# Schema for User Display on User UI
class UserDisplayOnUserUI(BaseModel):
  username: str
  email: str
  class Config():
    orm_mode = True
    
# Schema for User Display on Post UI
class UserDisplayOnPostUI(BaseModel):
  username: str
  class Config():
    orm_mode = True

# User Authentication Schema
class UserAuth(BaseModel):
    id: int
    username: str
    email: str
    
    
    