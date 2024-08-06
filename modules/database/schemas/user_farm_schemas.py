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
    location: str
    size: float


class FarmCreateRequest(BaseModel):
    name: str
    latitude: Optional[float]
    longitude: Optional[float]
    size: Optional[float]


class FarmUpdateRequest(BaseModel):
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    size: Optional[float]


class FarmResponse(BaseModel):
    id: int
    name: str
    latitude: Optional[float]
    longitude: Optional[float]
    size: Optional[float]
    created_at: datetime
    updated_at: datetime
