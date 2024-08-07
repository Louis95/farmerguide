"""User farm schema module."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    WORKER = "worker"
    CONSULTANT = "consultant"


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserFarmBase(BaseModel):
    role: UserRole


class UserFarmCreate(UserFarmBase):
    farm_id: int


class UserFarmUpdate(BaseModel):
    role: Optional[UserRole] = None


class UserFarmInDB(UserFarmBase):
    user_id: int
    farm_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    farms: List[UserFarmInDB] = []

    class Config:
        from_attributes = True


class FarmBase(BaseModel):
    name: str
    size: float
    latitude: float
    longitude:float


class FarmCreate(FarmBase):
    pass


class FarmUpdate(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    size: Optional[float] = None


class FarmInDB(FarmBase):
    id: int
    created_at: datetime
    updated_at: datetime
    users: List[UserFarmInDB] = []

    class Config:
        from_attributes = True
