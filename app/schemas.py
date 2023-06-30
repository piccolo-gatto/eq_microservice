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

        
class User(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(User):
    pass


class UserToken(BaseModel):
    token: str
