"""User farm schema module."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


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
    role: Optional[UserRole]


class UserFarmCreate(UserFarmBase):
    farm_id: int


class UserFarmUpdate(BaseModel):
    role: Optional[UserRole] = None


class UserFarmInDB(UserFarmBase):
    user_id: Optional[int]
    farm_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class FarmBase(BaseModel):
    id: Optional[int]
    name: str
    size: Optional[float]
    latitude: Optional[float]
    longitude: Optional[float]


class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    farms: Optional[list]


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
