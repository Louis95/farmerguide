from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CropBase(BaseModel):
    crop_type: str
    notes: str
    planted_on: datetime


class CropUpdate(CropBase):
    harvested_on: Optional[datetime] = None
    is_infected: Optional[bool] = None


class CropCreate(CropBase):
    farm_id: int


class CropInDB(CropBase):
    id: int
    farm_id: int
    created_at: datetime

    class Config:
        from_attributes = True
