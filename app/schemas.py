from pydantic import BaseModel,EmailStr
from datetime import datetime
import secrets


class File(BaseModel):
    id: int
    user_id: int
    ivent_id: int
    type: str
    path: str
    datetime: str

    class Config:
        orm_mode = True

        
class UserBase(BaseModel):
    email: EmailStr
      

class UserCreate(UserBase):
    pass
  

class User(UserBase):
    id: int
    files: list[File] = []

    class Config:
        orm_mode = True

        
class UserToken(BaseModel):
    token: str
