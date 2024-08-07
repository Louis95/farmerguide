from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CropBase(BaseModel):
    crop_type: str
    notes: str
    planted_on: datetime


class CropUpdate(CropBase):
    harvested_on: Optional[datetime] = None


class CropCreate(CropBase):
    farm_id: int


class CropResponse(CropBase):
    id: int
    farm_id: int
    created_at: datetime
    updated_at: datetime
    harvested_on: datetime

    class Config:
        from_attributes = True
