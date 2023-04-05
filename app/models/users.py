from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class UserBase(BaseModel):
    _id: Optional[str] = Field(..., alias='_id')
    username: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]
    full_name: Optional[str]
    disabled: Optional[str]
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    _id: str = Field(..., alias='_id')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class UserResponse(BaseModel):
    _id: str = Field(..., alias='_id')
    username: Optional[str]
    email: EmailStr
    full_name: Optional[str]
    disabled: Optional[str]
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
