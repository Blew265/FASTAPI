from pydantic  import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# Request Models
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserCreate(BaseModel):
    name : str
    username: str
    email: EmailStr
    password: str    
    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    class Config:
        from_attributes = True

class PostCreate(PostBase):
    pass
    
class PostUpdate(PostBase):
    pass

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    
class PostResponse(PostBase):
    title: str
    content: str
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True







